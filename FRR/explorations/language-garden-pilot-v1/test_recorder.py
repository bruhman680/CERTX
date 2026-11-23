"""Authored fixtures using the same cached tokenizer as the pilot."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from transformers import AutoTokenizer
from recorder import CUE, MAX_OUTPUT, SEED, advance, append, assemble, read, setup, state
from run import DEFAULT_MODEL, audit


class RecorderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL, local_files_only=True)

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.directory = Path(folder.name) / "record"
        setup(self.directory)

    def generator(self, ids, stop="eos"):
        def create(messages, run_id):
            return {
                "messages": messages,
                "input_token_ids": self.tokenizer.apply_chat_template(
                    messages, tokenize=True, add_generation_prompt=True),
                "generated_token_ids": ids,
                "text": self.tokenizer.decode(ids, skip_special_tokens=True),
                "run_id": run_id, "stop": stop, "decoder": "greedy_argmax",
            }
        return create

    def reply(self, text):
        return self.generator(self.tokenizer.encode(text, add_special_tokens=False) + [2])

    def test_exact_history_and_four_turn_bound(self):
        first = "  alfa\nbeta Ω  "
        replies = [first, " ", "A revision.", "Another observation."]
        for turn, expected in enumerate(replies, 1):
            self.assertEqual(advance(self.directory, self.tokenizer, self.reply(expected)),
                             "ready" if turn < 4 else "window_complete")
        status, archived = audit(self.directory, self.tokenizer)
        self.assertEqual(status, "window_complete")
        self.assertEqual([r["text"] for r in archived], replies)
        last = archived[-1]["messages"]
        self.assertEqual([m["content"] for m in last[1:]], [SEED, first, CUE, " ", CUE,
                                                           "A revision.", CUE])
        self.assertEqual(advance(self.directory, self.tokenizer, None), "window_complete")

    def test_fault_is_unknown_and_cannot_replay(self):
        def fail(*_):
            raise InterruptedError("fixture")
        with self.assertRaises(InterruptedError):
            advance(self.directory, self.tokenizer, fail)
        self.assertEqual(state(self.directory), ("interrupted_trace_unknown", []))
        self.assertEqual(advance(self.directory, self.tokenizer, None), "interrupted_trace_unknown")
        self.assertTrue((self.directory / "01/started.json").exists())
        self.assertFalse((self.directory / "01/returned.json").exists())

    def test_post_return_fault_keeps_reply(self):
        def fail():
            raise RuntimeError("fixture")
        with self.assertRaises(RuntimeError):
            advance(self.directory, self.tokenizer, self.reply("kept"), fail)
        status, replies = audit(self.directory, self.tokenizer)
        self.assertEqual((status, replies[0]["text"]), ("returned_integrity_unresolved", "kept"))
        self.assertEqual(advance(self.directory, self.tokenizer, None), status)

    def test_eos_only_has_known_empty_text(self):
        self.assertEqual(advance(self.directory, self.tokenizer, self.generator([2])),
                         "empty_visible_reply")
        self.assertEqual(audit(self.directory, self.tokenizer)[1][0]["generated_token_ids"], [2])

    def test_token_cap_and_last_token_eos_differ(self):
        token = self.tokenizer.encode("A", add_special_tokens=False)[0]
        ids = [token] * (MAX_OUTPUT - 1) + [2]
        self.assertEqual(advance(self.directory, self.tokenizer, self.generator(ids)), "ready")
        ids = [token] * MAX_OUTPUT
        self.assertEqual(advance(self.directory, self.tokenizer, self.generator(ids, "token_limit")),
                         "token_limit")
        self.assertEqual(len(audit(self.directory, self.tokenizer)[1]), 2)

    def test_overflow_records_plan_without_call(self):
        length = len(assemble(self.tokenizer, [])["input_token_ids"])
        with patch("recorder.MAX_INPUT", length), patch("run.MAX_INPUT", length):
            self.assertEqual(advance(self.directory, self.tokenizer, self.reply("visible")), "ready")
            self.assertEqual(advance(self.directory, self.tokenizer, None), "context_capacity")
            self.assertEqual(len(audit(self.directory, self.tokenizer)[1]), 1)
        self.assertFalse((self.directory / "02/started.json").exists())

    def test_retokenized_role_marker_preserved_but_withheld(self):
        ids = [44, 108, 306, 79, 3738, 108, 46, 2]
        self.assertEqual(advance(self.directory, self.tokenizer, self.generator(ids)), "ready")
        self.assertEqual(advance(self.directory, self.tokenizer, None), "native_marker_in_content")
        self.assertEqual(audit(self.directory, self.tokenizer)[1][0]["text"], "<|im_start|>")
        self.assertFalse((self.directory / "02/started.json").exists())

    def test_append_cannot_replace_event(self):
        path = self.directory / "event.json"
        append(path, {"first": True})
        with self.assertRaises(FileExistsError):
            append(path, {"first": False})
        self.assertEqual(read(path), {"first": True})


if __name__ == "__main__":
    unittest.main()
