import itertools
import random
import unittest

from algorithm.minCostIntervalCover import minCostIntervalCover
from algorithm.weightedMedian import weightedMedian, weightedMedianCost


class MinCostIntervalCoverTests(unittest.TestCase):
    def test_samples(self):
        self.assertEqual(minCostIntervalCover(5, [
            (1, 3, 10), (2, 4, 10), (3, 5, 20), (4, 5, 15)
        ]), 25)
        self.assertEqual(minCostIntervalCover(5, [
            (1, 2, 5), (4, 5, 10), (1, 1, 2)
        ]), -1)
        self.assertEqual(minCostIntervalCover(1, [(1, 1, 10**9)]), 10**9)
        self.assertEqual(minCostIntervalCover(0, []), 0)

    def test_reconstruction_and_random_bruteforce(self):
        rng = random.Random(197)
        for _ in range(300):
            n = rng.randint(1, 7)
            m = rng.randint(0, 9)
            intervals = []
            for _ in range(m):
                l = rng.randint(1, n)
                r = rng.randint(l, n)
                intervals.append((l, r, rng.randint(0, 15)))
            expected = -1
            for mask in range(1 << m):
                covered = 0
                price = 0
                for i, (l, r, c) in enumerate(intervals):
                    if mask >> i & 1:
                        covered |= ((1 << (r - l + 1)) - 1) << (l - 1)
                        price += c
                if covered == (1 << n) - 1:
                    expected = price if expected == -1 else min(expected, price)
            answer, chosen = minCostIntervalCover(n, intervals, restore=True)
            self.assertEqual(answer, expected, (n, intervals))
            self.assertEqual(minCostIntervalCover(n, intervals), expected)
            if answer != -1:
                covered = 0
                for i in chosen:
                    l, r, _ = intervals[i]
                    covered |= ((1 << (r - l + 1)) - 1) << (l - 1)
                self.assertEqual(covered, (1 << n) - 1)
                self.assertEqual(sum(intervals[i][2] for i in chosen), answer)

    def test_validation(self):
        with self.assertRaises(ValueError):
            minCostIntervalCover(3, [(0, 1, 2)])
        with self.assertRaises(ValueError):
            minCostIntervalCover(3, [(1, 4, 2)])
        with self.assertRaises(ValueError):
            minCostIntervalCover(3, [(1, 3, -1)])


class WeightedMedianCostTests(unittest.TestCase):
    def test_cost(self):
        self.assertEqual(weightedMedianCost([2, 5, 9], [1, 2, 1]), 7)
        self.assertEqual(weightedMedianCost([10, 1], [1, 1]), 9)
        self.assertEqual(weightedMedian([2, 5, 9], [1, 2, 1]), 5)


if __name__ == "__main__":
    unittest.main()
