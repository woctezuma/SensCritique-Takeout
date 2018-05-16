import unittest

import senscritique


class TestSensCritiqueMethods(unittest.TestCase):

    def test_main(self):
        self.assertTrue(senscritique.main())


if __name__ == '__main__':
    unittest.main()
