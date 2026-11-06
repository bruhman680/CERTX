"""Independent host-contract tests; disposable worlds, no model or primary access."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from world_store import World


PROFILE = json.loads((Path(__file__).resolve().parents[1] / "constants.json").read_text())


class WorldContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.temp.name) / "world.sqlite")
        self.profile = copy.deepcopy(PROFILE)
        self.world = World(self.path, self.profile)
        self.sequence = 0

    def tearDown(self):
        self.world.close()
        self.temp.cleanup()

    def submit(self, source, request_id=None, snapshot=None):
        self.sequence += 1
        return self.world.submit(request_id or f"test-{self.sequence}",
                                 snapshot or self.world.snapshot()["id"], source)

    def success(self, source, status="PUBLISHED"):
        receipt = self.submit(source)
        self.assertEqual(receipt["status"], status, receipt)
        self.assertIsNone(receipt.get("error"), receipt)
        return receipt

    def value(self, expression, expected):
        before = self.world.snapshot()
        receipt = self.success(f"(run {expression})", "COMPUTED")
        self.assert_guest_equal(receipt["value"], expected)
        self.assertEqual(self.world.snapshot(), before, "pure run mutated guest state")
        return receipt

    def assert_guest_equal(self, actual, expected):
        # Python bool is an int subclass; equality alone would hide a type bug.
        self.assertIs(type(actual), type(expected))
        if isinstance(expected, list):
            self.assertEqual(len(actual), len(expected))
            for left, right in zip(actual, expected):
                self.assert_guest_equal(left, right)
        else:
            self.assertEqual(actual, expected)

    def failure(self, source, code=None):
        before = self.world.snapshot()
        receipt = self.submit(source)
        self.assertNotIn(receipt["status"], ("COMPUTED", "PUBLISHED", "OBSERVED", "ALIAS_DROPPED"), receipt)
        self.assertIsInstance(receipt.get("error"), dict, receipt)
        if code is not None:
            self.assertEqual(receipt["error"]["code"], code, receipt)
        self.assertEqual(self.world.snapshot(), before, "failure changed guest state")
        return receipt

    def reopen(self, profile=None):
        self.world.close()
        self.world = World(self.path, profile or self.profile)

    def fresh_profile(self, updates):
        self.world.close()
        self.profile = copy.deepcopy(PROFILE)
        self.profile.update(updates)
        self.path = str(Path(self.temp.name) / "condition.sqlite")
        self.world = World(self.path, self.profile)

    def test_arithmetic_and_scheme_truth(self):
        cases = [("(+)", 0), ("(*)", 1), ("(+ 2 3 4)", 9),
                 ("(- 10 3 2)", 5), ("(- 3)", -3),
                 ("(floor-quotient -7 3)", -3), ("(floor-remainder -7 3)", 2),
                 ("(if #f 7 8)", 8), ("(if 0 7 8)", 7),
                 ("(if '() 7 8)", 7), ("(not 0)", False),
                 ("(integer? #t)", False), ("(equal? #t 1)", False),
                 ("(let ((x 2)) (+ x 3))", 5)]
        for expr, expected in cases:
            with self.subTest(expression=expr):
                self.value(expr, expected)

    def test_selected_branch_only_and_left_to_right_failure(self):
        self.value("(if #t 9 (car '()))", 9)
        self.failure("(run (list (car '()) (floor-quotient 1 0)))", "EMPTY_LIST")

    def test_error_domains_and_no_publication(self):
        for source, code in [("(run-save bad (car '()))", "EMPTY_LIST"),
                             ("(run-save bad (floor-quotient 2 0))", "DIVIDE_BY_ZERO"),
                             ("(run (+ #t 1))", "TYPE"),
                             ("(run (substring \"abc\" -1 2))", "INDEX_RANGE"),
                             ("(run (substring \"abc\" 2 1))", "INDEX_RANGE"),
                             ("(run (car))", "ARITY")]:
            with self.subTest(source=source):
                self.failure(source, code)
        self.assertNotIn("bad", self.world.snapshot()["aliases"])

    def test_dependency_pinning_after_helper_alias_change(self):
        self.success("(define (twice x) (+ x x))")
        old = self.world.snapshot()["aliases"]["twice"]["id"]
        self.success("(define (four x) (twice (twice x)))")
        self.success("(define (twice x) (+ x 100))")
        self.assertNotEqual(old, self.world.snapshot()["aliases"]["twice"]["id"])
        self.value("(four 3)", 12)
        self.value("(twice 3)", 103)

    def test_free_data_names_capture_when_definition_published(self):
        self.success("(put amount 2)")
        self.success("(define (read-amount ignored) amount)")
        self.success("(put amount 9)")
        self.value("(read-amount 0)", 2)
        self.value("amount", 9)

    def test_checkpoint_save_reload_and_pinned_continuation(self):
        self.success("(define (step s) (list (- (car s) 1) (+ (car s) (car (cdr s)))))")
        self.success("(define (advance s) (step s))")
        self.success("(run-save checkpoint (advance '(2 0)))")
        self.success("(define (step s) s)")
        before = self.world.snapshot()
        self.reopen()
        self.assertEqual(self.world.snapshot(), before)
        self.value("checkpoint", [1, 2])
        self.success("(run-save checkpoint (advance checkpoint))")
        self.value("checkpoint", [0, 3])

    def test_quotes_strings_are_inert_and_unknown_code_rejected(self):
        self.value("'(1 (2 3) #f)", [1, [2, 3], False])
        self.value('"(+ 1 2)"', "(+ 1 2)")
        self.failure("(run '(+ 1 2))", "SYNTAX")
        self.failure("(run (missing 3))", "UNBOUND_NAME")
        self.failure('(run (eval "(+ 1 2)"))', "UNBOUND_NAME")

    def test_tail_recursion_uses_bounded_frames(self):
        self.fresh_profile({"max_frames": 16})
        self.success("(define (down n) (if (= n 0) 0 (down (- n 1))))")
        self.value("(down 200)", 0)

    def test_nonterminating_tail_recursion_exhausts_budget(self):
        self.success("(define (forever x) (forever x))")
        receipt = self.failure("(run-save nonexistent (forever 0))")
        self.assertIn(receipt["error"]["code"], ("OUT_OF_FUEL", "STEP_LIMIT", "WORK_LIMIT"))
        self.assertNotIn("nonexistent", self.world.snapshot()["aliases"])

    def test_idempotent_retry_and_request_conflict(self):
        snapshot = self.world.snapshot()["id"]
        source = "(put saved 7)"
        first = self.submit(source, "stable-request", snapshot)
        after = self.world.snapshot()
        again = self.submit(source, "stable-request", snapshot)
        self.assertEqual(again, first)
        conflict = self.submit("(put saved 8)", "stable-request", snapshot)
        self.assertEqual(conflict["error"]["code"], "REQUEST_ID_CONFLICT", conflict)
        self.assertEqual(self.world.snapshot(), after)
        self.value("saved", 7)

    def test_snapshot_cas_rejects_stale_mutation_and_observation(self):
        old = self.world.snapshot()["id"]
        self.success("(put a 1)")
        before = self.world.snapshot()
        for source in ("(put a 2)", "(run a)", "(list)"):
            receipt = self.submit(source, snapshot=old)
            self.assertEqual(receipt["error"]["code"], "SNAPSHOT_MISMATCH", receipt)
            self.assertEqual(self.world.snapshot(), before)

    def test_integer_literal_and_result_boundaries(self):
        bits = self.profile["max_int_bits"]
        largest = (1 << bits) - 1
        self.value(str(largest), largest)
        self.value(str(-largest), -largest)
        self.failure(f"(run {1 << bits})", "INTEGER_LIMIT")
        self.failure(f"(run (+ {largest} 1))", "INTEGER_LIMIT")

    def test_unicode_scalar_text_and_boundaries(self):
        self.value('(string-length "A😀é")', 3)
        self.value('(substring "A😀é" 1 2)', "😀")
        self.value('(string-length "e\\x301;")', 2)
        self.value('(equal? "é" "e\\x301;")', False)
        self.value('(substring "A😀é" 3 3)', "")
        self.failure('(run (substring "A😀é" 0 4))', "INDEX_RANGE")
        self.failure('(run "' + 'a' * (self.profile["max_string_chars"] + 1) + '")')

    def test_source_depth_and_trailing_command_limits(self):
        self.failure('(run "' + "x" * self.profile["max_source_bytes"] + '")')
        n = self.profile["max_parse_depth"] + 2
        self.failure("(run " + "(list " * n + "0" + ")" * n + ")")
        self.failure("(put a 1) (put b 2)", "SYNTAX")
        self.assertEqual(self.world.snapshot()["aliases"], {})

    def test_draft_is_data_not_executable_definition(self):
        self.success('(put draft "(define (unfinished x)")')
        self.value("draft", "(define (unfinished x)")
        self.failure("(define (unfinished x)", "SYNTAX")

    def test_pagination_inspection_and_help_are_observations(self):
        for name in ("a", "b", "c", "d", "e"):
            self.success(f"(put {name} 1)")
        before = self.world.snapshot()
        receipt = self.success('(list "" 2)', "OBSERVED")
        names = []
        seen_cursors = set()
        while True:
            page = receipt["value"]
            self.assertLessEqual(len(page["items"]), 2)
            names.extend(item["name"] for item in page["items"])
            cursor = page["next_cursor"]
            if cursor is None:
                break
            self.assertNotIn(cursor, seen_cursors, "pagination cycle")
            seen_cursors.add(cursor)
            receipt = self.success(f"(list {json.dumps(cursor)} 2)", "OBSERVED")
        self.assertEqual(sorted(names), ["a", "b", "c", "d", "e"])
        self.assertEqual(len(names), len(set(names)))
        inspected = self.success("(inspect a)", "OBSERVED")["value"]
        self.assertEqual(inspected["kind"], "data")
        self.assertIn("payload", inspected)
        self.success("(help)", "OBSERVED")
        self.assertEqual(self.world.snapshot(), before)

    def test_dropped_helper_name_does_not_break_pinned_procedure(self):
        self.success("(define (helper x) (+ x 1))")
        self.success("(define (use-helper x) (helper x))")
        helper_id = self.world.snapshot()["aliases"]["helper"]["id"]
        self.success("(drop helper)", "ALIAS_DROPPED")
        self.assertNotIn("helper", self.world.snapshot()["aliases"])
        self.success("(define (helper x) (+ x 100))")
        self.value("(use-helper 3)", 4)
        old = self.success(f'(inspect "{helper_id}")', "OBSERVED")
        self.assertEqual(old["value"]["id"], helper_id)

    def test_retry_is_identical_after_reload(self):
        snapshot = self.world.snapshot()["id"]
        first = self.submit("(put saved 11)", "persistent-request", snapshot)
        self.reopen()
        retry = self.submit("(put saved 11)", "persistent-request", snapshot)
        self.assertEqual(retry, first)
        self.value("saved", 11)

    def test_invalid_and_old_snapshot_cursors_rejected(self):
        self.success("(put a 1)")
        self.success("(put b 2)")
        page = self.success('(list "" 1)', "OBSERVED")["value"]
        cursor = page["next_cursor"]
        self.assertIsNotNone(cursor)
        self.failure('(list "garbage" 1)', "CURSOR")
        self.success("(put c 3)")
        self.failure(f"(list {json.dumps(cursor)} 1)", "CURSOR")

    def test_action_quota_survives_reload(self):
        self.fresh_profile({"max_actions": 2})
        self.success("(put a 1)")
        self.success("(put b 2)")
        self.reopen()
        receipt = self.failure("(put c 3)")
        self.assertEqual(receipt["error"]["code"], "AUDIT_OR_ACTION_LIMIT")

    def test_audit_reserve_blocks_admission_without_mutation(self):
        self.fresh_profile({"max_audit_bytes": self.profile["max_receipt_bytes"] - 1})
        receipt = self.failure("(put cannot-fit 1)")
        self.assertIn(receipt["error"]["code"], ("AUDIT_OR_ACTION_LIMIT", "AUDIT_LIMIT", "AUDIT_RESERVE", "AUDIT_QUOTA", "NOT_ADMITTED"))


if __name__ == "__main__":
    unittest.main()
