import unittest

from dp.bitsetSubsetSum import BitsetSubsetSum


class TestBitsetSubsetSum(unittest.TestCase):
    def test_add_and_query(self):
        dp = BitsetSubsetSum()
        self.assertTrue(dp.contains(0))
        self.assertFalse(dp.contains(1))
        dp.add(3)
        dp.add(5)
        self.assertEqual([s for s in range(9) if s in dp], [0, 3, 5, 8])
        self.assertEqual(dp.max_leq(7), 5)
        self.assertEqual(dp.min_geq(4), 5)
        self.assertEqual(dp.max_leq(-1), None)
        self.assertEqual(dp.min_geq(9), None)

    def test_bounded(self):
        dp = BitsetSubsetSum(5)
        dp.add(3)
        dp.add(5)
        self.assertEqual(dp.max_leq(100), 5)
        self.assertEqual(dp.min_geq(4), 5)
        self.assertFalse(dp.contains(8))
        self.assertEqual(dp.min_geq(6), None)
        dp.add(0)
        self.assertEqual(dp.max_leq(5), 5)

    def test_empty_and_zero_limit(self):
        dp = BitsetSubsetSum(0)
        dp.add(100)
        self.assertTrue(dp.contains(0))
        self.assertEqual(dp.max_leq(0), 0)
        self.assertEqual(dp.min_geq(1), None)

    def test_partition(self):
        weights = [1, 2, 4]
        total = sum(weights)
        dp = BitsetSubsetSum(total // 2)
        for weight in weights:
            dp.add(weight)
        self.assertEqual(total - 2 * dp.max_leq(total // 2), 1)

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            BitsetSubsetSum(-1)
        dp = BitsetSubsetSum()
        with self.assertRaises(ValueError):
            dp.add(-1)


if __name__ == "__main__":
    unittest.main()
