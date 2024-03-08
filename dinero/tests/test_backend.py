# Implementating a pattern test. Use functions in the test.
import unittest
import numpy as np
from backend import technical_indicators

import unittest

class TestEntropy(unittest.TestCase):

    # Smoke test
    def test_back_smoke(self):
        calculate_rsi(pd.DataFrame(), length=14)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()