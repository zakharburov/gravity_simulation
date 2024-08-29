from math import sin, cos, radians, sqrt, degrees, atan2
from random import randint


class Object:
    def __init__(self, mass: int, speed: int, speed_angle: int, color: (int, int, int), radius: int, x: int, y: int):
        self.mass = mass
        self.speed_x = round(cos(radians(speed_angle)) * speed, 6)
        self.speed_y = round(sin(radians(speed_angle)) * speed, 6)
        self.speed_angle = speed_angle
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y

    def get_delta_speed(self, force, force_angle, time):
        acceleration = force / self.mass
        acquired_speed_global = acceleration * time
        delta_speed_x = round(cos(radians(force_angle)) * acquired_speed_global, 6)
        delta_speed_y = round(sin(radians(force_angle)) * acquired_speed_global, 6)

        return delta_speed_x, delta_speed_y

    def change_speed(self, force, force_angle, time):
        delta_speed_x, delta_speed_y = self.get_delta_speed(force, force_angle, time)

        self.speed_x = self.speed_x + delta_speed_x
        self.speed_y = self.speed_y + delta_speed_y

    def collide_another_object(self, objects: list):
        collided_objects = []
        for another_object in objects:
            if self is not another_object:
                if another_object.x - another_object.radius - self.radius <= self.x <= another_object.x + another_object.radius + self.radius and another_object.y - another_object.radius - self.radius <= self.y <= another_object.y + another_object.radius + self.radius:
                    collided_objects.append(another_object)

        return collided_objects

    @staticmethod
    def get_data_with_pulse_law(object_, another_object):
        mass1 = object_.mass
        mass2 = another_object.mass
        speed_x1 = object_.speed_x
        speed_x2 = another_object.speed_x
        speed_y1 = object_.speed_y
        speed_y2 = another_object.speed_y

        mass_sum = (mass1 + mass2) * randint(60, 80) / 100

        result_speed_x = (mass1 * speed_x1 + mass2 * speed_x2) / mass_sum
        result_speed_y = (mass1 * speed_y1 + mass2 * speed_y2) / mass_sum
        result_speed = sqrt(result_speed_x ** 2 + result_speed_y ** 2)
        angle = degrees(atan2(result_speed_y, result_speed_x))

        return result_speed, mass_sum, angle + (360 if angle < 0 else 0)

    def get_distance(self, another_object):
        x1, y1 = self.x, self.y
        x2, y2 = another_object.x, another_object.y

        print(sqrt((x2-x1) ** 2 + (y2-y1) ** 2))
