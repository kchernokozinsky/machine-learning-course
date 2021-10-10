from Point import Point


class Klass:
    def __init__(self, name, x_min, x_max, y_min, y_max):
        self.name = name
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val):
        self.__name = val

    @property
    def x_min(self):
        return self.__x_min

    @x_min.setter
    def x_min(self, val):
        self.__x_min = val

    @property
    def x_max(self):
        return self.__x_max

    @x_max.setter
    def x_max(self, val):
        self.__x_max = val

    @property
    def y_min(self):
        return self.__y_min

    @y_min.setter
    def y_min(self, val):
        self.__y_min = val

    @property
    def y_max(self):
        return self.__y_max

    @y_max.setter
    def y_max(self, val):
        self.__y_max = val

    def __str__(self):
        return "%s, x1_min = %s, x1_max = %s, x2_min = %s, x2_max = %s" % (
            self.__name, self.__x_min, self.__x_max, self.__y_min, self.__y_max)


def is_inside(point: Point, klass: Klass):
    return klass.x_max >= point.x >= klass.x_min and klass.y_max >= point.y >= klass.y_min


if __name__ == '__main__':
    klass = Klass("asd", 1, 2, 3, 4)
    print(klass)
