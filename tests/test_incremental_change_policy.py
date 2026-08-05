from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "change-seo-site" / "SKILL.md"
AGENT = ROOT / "skills" / "change-seo-site" / "agents" / "openai.yaml"


class IncrementalChangePolicyTests(unittest.TestCase):
    def test_change_skill_requires_incremental_reversible_delivery(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        required = [
            "## Incremental change and blast-radius policy",
            "must be incremental, independently reviewable,",
            "reversible, and attributable to one clear problem or hypothesis",
            "must not perform an unphased full-site redesign",
            "When a large migration is genuinely required, split it into independently",
            "reviewable and deployable phases",
            "state the blast radius",
            "representative unaffected routes",
            "rollback path",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_default_prompt_preserves_the_policy(self) -> None:
        text = AGENT.read_text(encoding="utf-8")
        for phrase in [
            "incremental",
            "reversible",
            "Preserve unrelated production behavior",
            "blast radius and rollback",
            "representative unaffected routes",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
