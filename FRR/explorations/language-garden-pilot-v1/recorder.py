"""Append-only records and native context for one bounded text session."""
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import tempfile

SYSTEM = "You are a helpful AI assistant named SmolLM, trained by Hugging Face"
SEED = "Explore symbols and their relationships. Learn to predict and understand them as best you can."
CUE = "Another turn is available."
MAX_INPUT, MAX_OUTPUT, MAX_TURNS = 7936, 256, 4


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sync_dir(path):
    with open_directory(path) as fd:
        os.fsync(fd)


@contextmanager
def open_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        yield fd
    finally:
        os.close(fd)


def append(path, value):
    """Publish a complete immutable event and refuse replacement."""
    fd, name = tempfile.mkstemp(prefix=".event-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=True, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.link(name, path)
    finally:
        os.unlink(name)
    sync_dir(path.parent)


def setup(path):
    path.mkdir()
    sync_dir(path.parent)


def assemble(tokenizer, replies):
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": SEED}]
    for reply in replies:
        messages.extend((
            {"role": "assistant", "content": reply["text"]},
            {"role": "user", "content": CUE},
        ))
    rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
    return {"messages": messages, "rendered": rendered, "input_token_ids": ids}


def state(directory):
    replies = []
    for turn in range(1, MAX_TURNS + 1):
        path = directory / f"{turn:02d}"
        if not path.exists():
            if (directory / "operator_pause.json").exists():
                return "operator_pause", replies
            return "ready", replies
        if (path / "pause.json").exists():
            return read(path / "pause.json")["reason"], replies
        if not (path / "returned.json").exists():
            reason = "interrupted_trace_unknown" if (path / "started.json").exists() else "preparation_incomplete"
            return reason, replies
        if not (path / "started.json").exists():
            raise ValueError("Return without start record")
        reply = read(path / "returned.json")
        replies.append(reply)
        if not (path / "checked.json").exists():
            return "returned_integrity_unresolved", replies
        if reply["stop"] == "token_limit":
            return "token_limit", replies
        if reply["text"] == "":
            return "empty_visible_reply", replies
        if reply["stop"] != "eos":
            return "unexpected_stop", replies
    return "window_complete", replies


def advance(directory, tokenizer, generate, verify_model=lambda: {}, expected_turn=None):
    """Offer one turn. An unresolved started call blocks replay."""
    with open_directory(directory) as fd:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        status, replies = state(directory)
        if status != "ready":
            return status
        turn = len(replies) + 1
        if expected_turn is not None and turn != expected_turn:
            raise ValueError("Session changed before this opportunity")
        path = directory / f"{turn:02d}"
        setup(path)
        plan = assemble(tokenizer, replies)
        special = [marker for marker in tokenizer.all_special_tokens
                   if any(marker in message["content"] for message in plan["messages"])]
        if special or len(plan["input_token_ids"]) > MAX_INPUT:
            reason = "native_marker_in_content" if special else "context_capacity"
            append(path / "pause.json", {"reason": reason, "plan": plan, "markers": special})
            return reason
        append(path / "started.json", {"turn": turn, "author": "host",
                                       "output_reserve": MAX_OUTPUT, **plan})
        try:
            reply = generate(plan["messages"], f"language-{turn:02d}")
        except BaseException as error:
            append(path / "fault.json", {"error": type(error).__name__,
                                         "detail": str(error), "partial_trace": "unknown"})
            raise
        # Preserve what the generator returned even if the subsequent audit fails.
        append(path / "returned.json", reply)
        verify_reply(tokenizer, plan, reply)
        append(path / "checked.json", verify_model())
        return state(directory)[0]


def verify_reply(tokenizer, plan, reply):
    ids = reply["generated_token_ids"]
    eos = tokenizer.eos_token_id
    if (reply["messages"] != plan["messages"]
            or reply["input_token_ids"] != plan["input_token_ids"]
            or reply["text"] != tokenizer.decode(ids, skip_special_tokens=True)
            or reply["decoder"] != "greedy_argmax"
            or not 1 <= len(ids) <= MAX_OUTPUT
            or eos in ids[:-1]
            or (reply["stop"] == "eos" and ids[-1] != eos)
            or (reply["stop"] == "token_limit" and (len(ids) != MAX_OUTPUT or ids[-1] == eos))
            or reply["stop"] not in ("eos", "token_limit")):
        raise ValueError("Returned reply does not match the pinned generation contract")
