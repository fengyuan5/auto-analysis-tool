from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class CliTest(unittest.TestCase):
    def run_cli(self, command: str) -> str:
        env = {"PYTHONPATH": str(ROOT / "src")}
        result = subprocess.run(
            [sys.executable, "-m", "auto_analysis_tool", command],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout

    def test_discover(self) -> None:
        output = self.run_cli("discover")
        self.assertIn("Recipe Discovery", output)
        self.assertIn("hunyuan_video", output)

    def test_report(self) -> None:
        output = self.run_cli("report")
        self.assertIn("Auto Analysis Report", output)
        self.assertIn("qwen2_5_rl_demo", output)

    def test_validate(self) -> None:
        output = self.run_cli("validate")
        self.assertIn("hunyuan_video: valid", output)
