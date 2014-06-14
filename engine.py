import pyglet
import math

class Vector(object):
    def __init__(self, angle, distance):
        self.x = x
        self.y = y

        self.angle = math.radians(angle)
        self.distance = distance

    def add_to_point(self, point_x, point_y):
        """
        Add this vector to a given point (useful to move an object from its x/y)
        """
        new_point_x = point_x + (self.distance * math.cos(self.angle))
        new_point_y = point_y + (self.distance * math.sin(self.angle))

        return new_point_x, new_point_y