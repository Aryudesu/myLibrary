import unittest
from fractions import Fraction

from algorithm.weightedMedian import weightedMedian
from algorithm.treeImos import TreeImos


class WeightedMedianTests(unittest.TestCase):
    def test_ordinary(self):
        self.assertEqual(weightedMedian([8, 1, 3], [2, 1, 5]), 3)

    def test_tie_returns_left_endpoint(self):
        self.assertEqual(weightedMedian([10, 1], [1, 1]), 1)

    def test_fraction(self):
        self.assertEqual(
            weightedMedian([Fraction(1, 3), Fraction(2, 3)], [2, 1]),
            Fraction(1, 3),
        )

    def test_zero_weight(self):
        self.assertEqual(weightedMedian([5, 9], [0, 7]), 9)

    def test_invalid(self):
        for vals, weights in [([], []), ([1], [0]), ([1], [-1]), ([1], [])]:
            with self.subTest(vals=vals, weights=weights):
                with self.assertRaises(ValueError):
                    weightedMedian(vals, weights)


class TreeImosTests(unittest.TestCase):
    def test_subtrees_and_complements(self):
        graph = [[1, 2], [0, 3], [0], [1]]
        imos = TreeImos(graph)
        self.assertEqual(imos.subtreeSize, [4, 2, 1, 1])
        imos.addSubtree(1, 5)
        imos.addOutsideSubtree(1, 3)
        imos.addSubtree(0, 2)
        self.assertEqual(imos.build(), [5, 7, 5, 7])
        self.assertEqual(imos.build(), [5, 7, 5, 7])

    def test_root_complement_is_empty(self):
        imos = TreeImos([[1], [0]])
        imos.addOutsideSubtree(0, 9)
        self.assertEqual(imos.build(), [0, 0])

    def test_deep_path(self):
        n = 5000
        graph = [[] for _ in range(n)]
        for i in range(n - 1):
            graph[i].append(i + 1)
            graph[i + 1].append(i)
        imos = TreeImos(graph)
        imos.addSubtree(n - 1, 7)
        self.assertEqual(imos.build()[-2:], [0, 7])


if __name__ == "__main__":
    unittest.main()
