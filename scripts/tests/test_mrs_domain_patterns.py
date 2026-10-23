import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "gfwlist_parser.py"
SPEC = importlib.util.spec_from_file_location("gfwlist_parser", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
PARSER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PARSER)


class MrsDomainPatternTests(unittest.TestCase):
    def test_generated_clash_rules_are_preserved_and_mrs_inputs_are_patterns(self):
        domain = "synthetic.example.invalid"
        ip = "192.0.2.1"

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            provider = root / "provider.yaml"
            ruleset = root / "ruleset.list"

            PARSER.generate_clash_provider_yaml([domain], [ip], str(provider))
            PARSER.generate_clash_ruleset_list([domain], [ip], str(ruleset))
            PARSER.split_yaml_file(str(provider))
            PARSER.split_list_file(str(ruleset))

            self.assertIn(f"DOMAIN-SUFFIX,{domain}", provider.read_text(encoding="utf-8"))
            self.assertIn(f"DOMAIN-SUFFIX,{domain}\n", ruleset.read_text(encoding="utf-8"))
            self.assertEqual(
                (root / "provider_domain.yaml").read_text(encoding="utf-8"),
                f"payload:\n  - +.{domain}\n",
            )
            self.assertEqual(
                (root / "ruleset_domain.list").read_text(encoding="utf-8"),
                f"+.{domain}\n",
            )
            self.assertEqual(
                (root / "provider_ip.yaml").read_text(encoding="utf-8"),
                f"payload:\n  - {ip}/32\n",
            )
            self.assertEqual(
                (root / "ruleset_ip.list").read_text(encoding="utf-8"),
                f"{ip}/32\n",
            )

    def test_exact_and_suffix_rule_mappings(self):
        domain = "synthetic.example.invalid"
        self.assertEqual(PARSER.format_mrs_domain_rule("DOMAIN", domain), domain)
        self.assertEqual(
            PARSER.format_mrs_domain_rule("DOMAIN-SUFFIX", domain),
            f"+.{domain}",
        )


if __name__ == "__main__":
    unittest.main()
