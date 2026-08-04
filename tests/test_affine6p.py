import unittest
from typing import TypedDict

import affine6p
from affine6p.transform import AffineMatrix, Points


class TestSample(TypedDict):
    id: str
    a: Points
    b: Points
    params: AffineMatrix
    error: float


samples: tuple[TestSample, ...] = (
    {
        "id": "N is 1",
        "a": ((0, 0),),
        "b": ((1, 1),),
        "params": (1, 0, 0, 1, 1, 1),
        "error": 0,
    },
    {
        "id": "N is 2",
        "a": ((1, 0), (0, 1)),
        "b": ((0, 2), (-2, 0)),
        "params": (0, -2, 2, 0, 0, 0),
        "error": 0,
    },
    {
        "id": "N is 3",
        "a": ((0, 0), (1, 0), (0, 1)),
        "b": ((0, 0), (1, 0), (0, 1.1)),
        "params": (1, 0, 0, 1.1, 0, 0),
        "error": 0,
    },
    {
        "id": "N is 4",
        "a": ((0, 0), (1, 0), (0, 1), (2, 2)),
        "b": ((0, 0), (1, 0), (0, 1.1), (2, 2)),
        "params": (1, 0, -0.05556, 1.04444, 0, 0.03333),
        "error": 0.02357,
    },
    {
        "id": "N is 5",
        "a": ((0, 0), (1, 0), (0, 1), (2, 2), (5, 87)),
        "b": ((0, 0), (1, 0), (0, 1.1), (2, 2), (3, 4)),
        "params": (1.01448, -0.02390, 0.57171, 0.00951, 0.00694, 0.33402),
        "error": 0.59314,
    },
)


class TestEstimate(unittest.TestCase):
    def test_affine6p(self):
        """
        should affine6p correctly
        """
        for sample in samples:
            # check estimate
            transform = affine6p.estimate(sample["a"], sample["b"])
            print("matrix = {0}".format(transform.get_matrix()))
            for i in range(0, 6):
                self.assertTrue(
                    abs(transform.params[i] - sample["params"][i]) < 0.001,
                    f"{sample['id']}: {i}={transform.params[i]}",
                )

            # check functions
            print(f"{sample['a']} -> {sample['b']}")
            print(f"matrix = {transform.get_matrix()}")
            print(f"rotation_x = {transform.get_rotation_x()}")
            print(f"rotation_y = {transform.get_rotation_y()}")
            print(f"scale_x = {transform.get_scale_x()}")
            print(f"scale_y = {transform.get_scale_y()}")
            print(f"scale = {transform.get_scale()}")
            print(f"translation = {transform.get_translation()}")
            print(" ")

            # check estimate_error
            error = affine6p.estimate_error(transform, sample["a"], sample["b"])
            self.assertTrue(
                abs(error - sample["error"]) < 0.001, f"{sample['id']}: error={error}"
            )

            # check transform_inv
            if len(sample["a"]) == 3:
                points_inv = transform.transform_inv(sample["b"])
                for i in range(0, 3):
                    for j in range(0, 2):
                        self.assertTrue(
                            abs(points_inv[i][j] - sample["a"][i][j]) < 0.001,
                            f"{sample['id']}: a2={points_inv[j]}",
                        )


if __name__ == "__main__":
    unittest.main()
