from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_experiment_ledger.py"
SPEC = importlib.util.spec_from_file_location("validate_experiment_ledger", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ExperimentLedgerValidationTests(unittest.TestCase):
    def write(self, root: Path, relative: str, content: str) -> Path:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_accepts_opt_in_valid_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            site = self.write(root, "site.md", "- Maximum active speculative experiments: 1\n")
            ledger = self.write(
                root,
                "experiments.md",
                """# Experiments

### EXP-20260805-01 — title test
- Status: `observing`
""",
            )
            self.assertEqual(MODULE.validate(ledger, site), (1, 1, 1))

    def test_rejects_duplicate_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = self.write(
                Path(directory),
                "experiments.md",
                """# Experiments

### EXP-20260805-01 — first
- Status: `active`

### EXP-20260805-01 — duplicate
- Status: `observing`
""",
            )
            with self.assertRaisesRegex(ValueError, "duplicate experiment ID"):
                MODULE.validate(ledger)

    def test_rejects_invalid_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = self.write(
                Path(directory),
                "experiments.md",
                """# Experiments

### EXP-20260805-01 — invalid
- Status: `running`
""",
            )
            with self.assertRaisesRegex(ValueError, "invalid experiment status"):
                MODULE.validate(ledger)

    def test_rejects_missing_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = self.write(
                Path(directory),
                "experiments.md",
                """# Experiments

### EXP-20260805-01 — incomplete
- Hypothesis: something changes
""",
            )
            with self.assertRaisesRegex(ValueError, "missing status"):
                MODULE.validate(ledger)

    def test_rejects_active_count_above_declared_limit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            site = self.write(root, "site.md", "- Maximum active speculative experiments: 1\n")
            ledger = self.write(
                root,
                "experiments.md",
                """# Experiments

### EXP-20260805-01 — first
- Status: `active`

### EXP-20260805-02 — second
- Status: `evaluating`
""",
            )
            with self.assertRaisesRegex(ValueError, "active experiments exceed limit"):
                MODULE.validate(ledger, site)

    def test_rejects_conflicting_limits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            site = self.write(root, "site.md", "- Maximum active speculative experiments: 1\n")
            ledger = self.write(
                root,
                "experiments.md",
                """# Experiments
- Maximum active speculative experiments: 2
""",
            )
            with self.assertRaisesRegex(ValueError, "conflicting maximum"):
                MODULE.validate(ledger, site)


if __name__ == "__main__":
    unittest.main()
