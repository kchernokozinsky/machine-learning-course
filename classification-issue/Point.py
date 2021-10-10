import math


class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __eq__(self, other: object) -> bool:
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __ne__(self, other):
        return not (self == other)

    def __str__(self) -> str:
        return "[%s, %s]" % (self.__x, self.__y)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val):
        self.__x = val

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, val):
        self.__y = val


def get_distance(p1: Point, p2: Point):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


if __name__ == '__main__':
    p1 = Point(2, 2)
    p2 = Point(0, 0)
    print(get_distance(p1, p2))
