"""Regression tests for the zygote's parent process and sandboxed children."""

import os
import sys
import unittest
from unittest.mock import patch

import vote
import zygote
from client import ADDRESS_SPACE_MB, CAP_MS, MAX_CODE_BYTES, STDOUT_BYTES, ZygoteClient


class GeneratorTests(unittest.TestCase):
    def test_paths_never_reach_the_module_loader(self):
        with patch("zygote.importlib.util.spec_from_file_location") as loader:
            for slug in ("../outside", "/tmp/outside", "a/../../outside", "a\\outside", "", "."):
                with self.assertRaises(ValueError):
                    zygote.generator(slug)
            loader.assert_not_called()

    def test_a_slug_is_resolved_only_in_the_generator_directory(self):
        with patch("zygote.importlib.util.spec_from_file_location", return_value=None) as loader:
            with self.assertRaises(FileNotFoundError):
                zygote.generator("valid-generator")
            loader.assert_called_once_with(
                "gen_valid-generator", zygote.GEN_DIR / "valid-generator.py"
            )


class ClientTests(unittest.TestCase):
    def test_reference_votes_share_the_judge_memory_limit(self):
        self.assertEqual(vote.LIMITS["as_mb"], ADDRESS_SPACE_MB)

    def test_client_enforces_the_shared_code_size_limit(self):
        with self.assertRaises(ValueError):
            ZygoteClient(61_000)._validate_code(" " * (MAX_CODE_BYTES + 1))


@unittest.skipUnless(sys.platform == "linux" and os.geteuid() == 0, "needs the Linux judge")
class ZygoteTests(unittest.TestCase):
    def run_job(
        self, code: str, output_limit: int = 4096, test_count: int = 1, keep_going: bool = False
    ) -> list[dict]:
        job = {
            "spec": {
                "kind": "function",
                "cls": "Solution",
                "method": "answer",
                "params": [],
                "returns": "int",
            },
            "code": code,
            "tests": [{"input": {}}] * test_count,
            "keep_going": keep_going,
            "limits": {
                "cpu_s": min(2, CAP_MS // 1000),
                "as_mb": ADDRESS_SPACE_MB,
                "out_bytes": output_limit,
                "stdout_bytes": STDOUT_BYTES,
            },
        }
        with ZygoteClient(61_000) as client:
            return client.run(job)

    def test_normal_answer(self):
        events = self.run_job("class Solution:\n def answer(self): return 42")
        self.assertEqual(next(e["ev"]["out"] for e in events if "ev" in e), 42)
        self.assertEqual(events[-1]["done"]["code"], 0)

    def test_reference_memory_error_does_not_hide_later_tests(self):
        code = (
            "class Solution:\n"
            " calls = 0\n"
            " def answer(self):\n"
            "  Solution.calls += 1\n"
            "  if Solution.calls == 1: raise MemoryError()\n"
            "  return 42\n"
        )
        events = self.run_job(code, test_count=2, keep_going=True)
        cases = [event["ev"] for event in events if "ev" in event]

        self.assertEqual(cases[0], {"i": 0, "mle": True})
        self.assertEqual(cases[1]["out"], 42)

    def test_unterminated_output_is_bounded(self):
        events = self.run_job(
            "import os\n"
            "for fd in range(3, 64):\n"
            " try:\n"
            "  while True: os.write(fd, b'x' * 8192)\n"
            " except OSError: pass\n"
        )
        self.assertIn({"ole": True}, events)
        self.assertEqual(events[-1]["done"]["signal"], 9)

    def test_exec_cannot_free_a_process_slot(self):
        script = (
            "import os, sys\n"
            "try: pid = os.fork()\n"
            "except OSError: sys.exit(0)\n"
            "if pid == 0: os._exit(0)\n"
            "os.waitpid(pid, 0)\n"
            "sys.exit(73)\n"
        )
        events = self.run_job(
            f"import os, sys\nos.execv(sys.executable, [sys.executable, '-c', {script!r}])"
        )
        self.assertEqual(events[-1]["done"]["code"], 0, "exec allowed a sandbox escape via fork")


if __name__ == "__main__":
    unittest.main()
