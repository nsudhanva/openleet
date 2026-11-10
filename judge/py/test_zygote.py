"""Regression tests for the zygote's parent process and sandboxed children."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import zygote


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


@unittest.skipUnless(sys.platform == "linux" and os.geteuid() == 0, "needs the Linux judge")
class ZygoteTests(unittest.TestCase):
    def run_job(self, code: str, output_limit: int = 4096) -> list[dict]:
        job = {
            "spec": {
                "kind": "function",
                "cls": "Solution",
                "method": "answer",
                "params": [],
                "returns": "int",
            },
            "code": code,
            "tests": [{"input": {}}],
            "limits": {"cpu_s": 2, "as_mb": 704, "out_bytes": output_limit},
        }
        process = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("zygote.py"))],
            input=json.dumps(job) + "\n",
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        return [json.loads(line) for line in process.stdout.splitlines()]

    def test_normal_answer(self):
        events = self.run_job("class Solution:\n def answer(self): return 42")
        self.assertTrue(events[0]["ready"])
        self.assertEqual(next(e["ev"]["out"] for e in events if "ev" in e), 42)
        self.assertEqual(events[-1]["done"]["code"], 0)

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
