import math
from collections.abc import Sequence

type Point = tuple[float, float]
type Points = Sequence[Point]
type AffineMatrix = tuple[float, float, float, float, float, float]


class Transform:
    def __init__(self, params: AffineMatrix) -> None:
        # Public, to allow user access
        self.params: AffineMatrix = params

    def a(self) -> float:
        return self.params[0]

    def b(self) -> float:
        return self.params[1]

    def c(self) -> float:
        return self.params[2]

    def d(self) -> float:
        return self.params[3]

    def p(self) -> float:
        return self.params[4]

    def q(self) -> float:
        return self.params[5]

    def transform(self, points: Points) -> Points:
        """
        Parameter
            p
                point [x, y] or list of points [[x1,y1], [x2,y2], ...]
        """

        def transform_one(point: Point) -> Point:
            return (
                self.params[0] * point[0] + self.params[1] * point[1] + self.params[4],
                self.params[2] * point[0] + self.params[3] * point[1] + self.params[5],
            )

        return list(map(transform_one, points))

    def rotate(self, points: Points) -> Points:
        """
        Parameter
            p
                point [x, y] or list of points [[x1,y1], [x2,y2], ...]
        """

        def rotate_one(point: Point) -> Point:
            return (
                self.params[0] * point[0] + self.params[1] * point[1],
                self.params[2] * point[0] + self.params[3] * point[1],
            )

        return list(map(rotate_one, points))

    def transform_inv(self, points: Points) -> Points:
        """
        Parameter
            p
                point [x, y] or list of points [[x1,y1], [x2,y2], ...]
        """

        def transform_inv_one(point: Point) -> Point:
            det = self.params[0] * self.params[3] - self.params[2] * self.params[1]
            return (
                (
                    self.params[3] * (point[0] - self.params[4])
                    - self.params[1] * (point[1] - self.params[5])
                )
                / det,
                (
                    self.params[2] * (point[0] - self.params[4])
                    - self.params[0] * (point[1] - self.params[5])
                )
                / det
                * -1.0,
            )

        return list(map(transform_inv_one, points))

    def rotate_inv(self, points: Points) -> Points:
        """
        Parameter
            p
                point [x, y] or list of points [[x1,y1], [x2,y2], ...]
        """

        def rotate_inv_one(point: Point) -> Point:
            det = self.params[0] * self.params[3] - self.params[2] * self.params[1]
            return (
                (self.params[3] * point[0] - self.params[1] * point[1]) / det,
                (self.params[2] * point[0] - self.params[0] * point[1]) / det * -1.0,
            )

        return list(map(rotate_inv_one, points))

    def get_matrix(
        self,
    ) -> tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ]:
        return (
            (self.params[0], self.params[1], self.params[4]),
            (self.params[2], self.params[3], self.params[5]),
            (0, 0, 1),
        )

    def get_rotation_x(self) -> float:
        return math.atan2(-self.params[1], self.params[0])

    def get_rotation_y(self) -> float:
        return math.atan2(self.params[2], self.params[3])

    def get_scale_x(self) -> float:
        return math.sqrt(
            self.params[0] * self.params[0] + self.params[1] * self.params[1]
        )

    def get_scale_y(self) -> float:
        return math.sqrt(
            self.params[2] * self.params[2] + self.params[3] * self.params[3]
        )

    def get_scale(self) -> float:
        summed = (
            self.get_scale_x() * self.get_scale_x()
            + self.get_scale_y() * self.get_scale_y()
        )
        return math.sqrt(summed * 0.5)

    def get_translation(self) -> Point:
        return (self.params[4], self.params[5])
