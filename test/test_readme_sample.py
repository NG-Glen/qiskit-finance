# This code is part of Qiskit.
#
# (C) Copyright IBM 2020, 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Code inside the test is the finance sample from the readme.
If this test fails and code changes are needed here to resolve
the issue then ensure changes are made to readme too.
"""

import unittest

import contextlib
import io
from pathlib import Path
import re
from test import QiskitFinanceTestCase


class TestReadmeSample(QiskitFinanceTestCase):
    """Test sample code from readme"""

    def test_readme_sample(self):
        """readme sample test"""
        # pylint: disable=exec-used

        readme_name = "README.md"
        readme_path = Path(__file__).parent.parent.joinpath(readme_name)
        if not readme_path.exists() or not readme_path.is_file():
            self.fail(msg=f"{readme_name} not found at {readme_path}")
            return

        # gets the first matched code sample
        # assumes one code sample to test per readme
        readme_sample = None
        with open(readme_path, encoding="UTF-8") as readme_file:
            match_sample = re.search(
                "```python.*```",
                readme_file.read(),
                flags=re.S,
            )
            if match_sample:
                # gets the matched string stripping the markdown code block
                readme_sample = match_sample.group(0)[9:-3]

        if readme_sample is None:
            self.skipTest(f"No sample found inside {readme_name}.")
            return

        with contextlib.redirect_stdout(io.StringIO()) as out:
            try:
                exec(readme_sample)
            except Exception as ex:  # pylint: disable=broad-except
                self.fail(str(ex))
                return

        estimation = None
        probability = None
        str_ref1 = "Estimated value:"
        str_ref2 = "Probability:"
        texts = out.getvalue().split("\n")
        for text in texts:
            idx = text.find(str_ref1)
            if idx >= 0:
                estimation = float(text[idx + len(str_ref1) :])
                continue
            idx = text.find(str_ref2)
            if idx >= 0:
                probability = float(text[idx + len(str_ref2) :])
            if estimation is not None and probability is not None:
                break

        if estimation is None:
            self.fail(f"Failed to find estimation inside {readme_name}.")
            return
        if probability is None:
            self.fail(f"Failed to find max.probability inside {readme_name}.")
            return

        with self.subTest("test estimation"):
            self.assertAlmostEqual(estimation, 2.46, places=4)
        with self.subTest("test max.probability"):
            self.assertAlmostEqual(probability, 0.8487, places=4)


if __name__ == "__main__":
    unittest.main()
