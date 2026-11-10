"""Exercise the updater in an isolated directory with downloads and systemctl replaced."""

import fcntl
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REVISION = "0123456789abcdef"
MOCK = r"""
import hashlib
import os
import sys
from pathlib import Path

root = Path(os.environ["UPDATE_TEST_ROOT"])
command = Path(sys.argv[0]).name
if command == "curl":
    if "-o" not in sys.argv:
        print("0123456789abcdef")
    else:
        output = Path(sys.argv[sys.argv.index("-o") + 1])
        if output.name.endswith(".sha256"):
            output.write_text(hashlib.sha256(b"release").hexdigest() + "  "
                              + output.name.removesuffix(".sha256") + "\n")
        else:
            output.write_bytes(b"release")
elif command == "tar":
    release = Path(sys.argv[sys.argv.index("-C") + 1])
    (release / "data").mkdir()
    (release / "deploy").mkdir()
    installer = release / "deploy/install.sh"
    installer.write_text("#!/bin/sh\nexit 0\n")
    installer.chmod(0o755)
    with (root / "extractions").open("a") as log:
        log.write("extracted\n")
elif command == "systemctl" and (root / "fail-restart").exists():
    (root / "fail-restart").unlink()
    sys.exit(1)
"""


@unittest.skipUnless(sys.platform == "linux", "updater needs Linux flock and mv -T")
class UpdateTests(unittest.TestCase):
    def test_failed_restart_is_retried_without_removing_the_current_release(self):
        with tempfile.TemporaryDirectory(prefix="openleet-update-") as temporary:
            root = Path(temporary)
            commands = root / "commands"
            commands.mkdir()
            (root / "releases").mkdir()
            (root / "request").write_text(REVISION + "\n")
            for name in ("curl", "tar", "systemctl", "chown", "chgrp"):
                command = commands / name
                command.write_text(f"#!{sys.executable}\n{MOCK}")
                command.chmod(0o755)
            source = Path(__file__).with_name("update.sh").read_text()
            source = source.replace("ROOT=/opt/openleet", f"ROOT={shlex.quote(str(root))}")
            source = source.replace(
                "REQUEST=/var/lib/openleet/deploy-request",
                f"REQUEST={shlex.quote(str(root / 'request'))}",
            )
            script = root / "update.sh"
            script.write_text(source)
            env = {
                **os.environ,
                "PATH": f"{commands}:{os.environ['PATH']}",
                "UPDATE_TEST_ROOT": str(root),
            }

            def run():
                return subprocess.run(
                    ["sh", str(script)], env=env, capture_output=True, text=True, timeout=10
                )

            # A manual invocation must respect the same lock as systemd's invocation.
            with (root / "update.lock").open("w") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.assertEqual(run().returncode, 0)
                self.assertFalse((root / "extractions").exists())

            (root / "fail-restart").touch()
            failed = run()
            self.assertNotEqual(failed.returncode, 0)
            self.assertFalse((root / "deployed").exists())
            release = root / "releases" / REVISION
            self.assertTrue((root / "current").is_symlink(), failed.stderr)
            self.assertEqual((root / "current").resolve(), release)
            marker = release / "keep-during-retry"
            marker.touch()
            retried = run()
            self.assertEqual(retried.returncode, 0, retried.stderr)
            self.assertTrue(marker.exists())
            self.assertEqual((root / "deployed").read_text(), REVISION + "\n")
            self.assertEqual((root / "extractions").read_text(), "extracted\n")


if __name__ == "__main__":
    unittest.main()
