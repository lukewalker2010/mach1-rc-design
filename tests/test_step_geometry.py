import unittest

from tools import step_validate


class StepGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = step_validate.validate()
        if cls.results is None:
            raise unittest.SkipTest("OpenCascade (OCP) not installed")

    def test_all_step_files_pass_gate(self):
        failures = [r for r in self.results if not r.passed]
        self.assertFalse(
            failures, "\n".join(f"{r.file}: {r.detail}" for r in failures)
        )

    def test_expected_files_present(self):
        names = {r.file for r in self.results}
        expected = {name for name, *_ in step_validate.EXPECTED}
        self.assertEqual(names, expected)


if __name__ == "__main__":
    unittest.main()
