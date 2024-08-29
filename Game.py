from math import atan2, degrees, sqrt
from random import randint

import pygame

from Object import Object


class Game:
    def __init__(self, G, width=2500, height=1300, bg_color=(0, 0, 0), fps=300):
        self.width = width
        self.height = height
        self.bg_color = bg_color

        self.G = G

        self.screen = pygame.display.set_mode((width, height))
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.game_run = True

        self.sun = Object(10000, 0, 0, (255, 255, 0), 30, width // 2, height // 2)
        self.objects = [Object(100, 50, 0, (255, 0, 0), 5, width // 2, 250),
                        Object(2000, 40, 180, (0, 255, 255), 7, 1250, 900)]  # ,
        # Object(2000, 140, 300, (0, 255, 0), 7, 800, 500),
        # Object(2000, 100, 290, (0, 0, 255), 13, 600, 500),
        # Object(2000, 130, 120, (0, 255, 255), 7, 1700, 1000)]
        self.moon = Object(10, 70, 0, (255, 255, 255), 3, width // 2, 225)

        # self.sun = Object(10000, 0, 0, (255, 255, 0), 30, width//2, height//2)
        # self.objects = [Object(100, 50, 0, (255, 0, 0), 5, width//2, 250)]#,
        #                 #Object(2000, 140, 300, (0, 255, 0), 7, 800, 500),
        #                 #Object(2000, 100, 290, (0, 0, 255), 13, 600, 500),
        #                 #Object(2000, 130, 120, (0, 255, 255), 7, 1700, 1000)]
        # self.moon = Object(10, 30, 0, (255, 255, 255), 3, width//2, 225)

        self.run()

    def __del__(self):
        pygame.quit()

    def run(self):
        while self.game_run:
            self.check_events()
            self.game_logic()
            self.draw()

            self.clock.tick(self.fps)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_run = False

    def get_force_of_gravity(self, first_mass, second_mass, radius):
        force_of_gravity = self.G * (first_mass * second_mass / (radius ** 2))

        return force_of_gravity

    @staticmethod
    def get_angle_of_force_of_gravity(first_object, second_object):
        x1, y1 = first_object.x, first_object.y
        x2, y2 = second_object.x, second_object.y

        delta_x = x1 - x2
        delta_y = y1 - y2
        angle = degrees(atan2(delta_y, delta_x))

        return angle + (360 if angle < 0 else 0)

    @staticmethod
    def get_distance_between_objects(first_object, second_object):
        x1, y1 = first_object.x, first_object.y
        x2, y2 = second_object.x, second_object.y

        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)

        distance = sqrt(delta_x ** 2 + delta_y ** 2)

        return distance

    def create_new_planet(self, x, y, mass, speed, angle, radius, color):
        object_ = Object(mass, speed, angle, color, radius, x, y)

        self.objects.append(object_)

    def game_logic(self):
        objects_to_remove = []
        for object_ in self.objects:
            collided_objects = object_.collide_another_object(self.objects + [self.sun])
            for collided_object in collided_objects:
                if collided_object is self.sun:
                    objects_to_remove.append(object_)
                else:
                    if [collided_object, object_] not in objects_to_remove:
                        objects_to_remove.append([object_, collided_object])

        for objects in objects_to_remove:
            try:
                speed, mass, angle = Object.get_data_with_pulse_law(objects[0], objects[1])
                x, y = (objects[0].x + objects[1].x) / 2, (objects[0].y + objects[1].y) / 2
                radius = max(objects[0].radius, objects[1].radius) + min(objects[0].radius, objects[1].radius) / 2
                color = (randint(0, 255), randint(0, 255), randint(0, 255))

                self.objects.remove(objects[0])
                self.objects.remove(objects[1])

                self.create_new_planet(x, y, mass, speed, angle, radius, color)
            except:
                self.objects.remove(objects)

        for object_ in self.objects:
            object_.change_speed(self.get_force_of_gravity(object_.mass, self.sun.mass,
                                                           self.get_distance_between_objects(object_, self.sun)),
                                 self.get_angle_of_force_of_gravity(self.sun, object_), 1 / self.fps)

            """
            for another_object in self.objects:  # Притяжение относительно других планет. Убрать - закомментировать цикл
                if object_ is not another_object:
                    object_.change_speed(self.get_force_of_gravity(object_.mass, another_object.mass, self.get_distance_between_objects(object_, another_object)), self.get_angle_of_force_of_gravity(another_object, object_), 1 / self.fps)
            """

            object_.x += object_.speed_x * 1 / self.fps
            object_.y += object_.speed_y * 1 / self.fps

            object_.get_distance(self.moon)

        self.sun.x += self.sun.speed_x * 1 / self.fps
        self.sun.y += self.sun.speed_y * 1 / self.fps

        self.moon.change_speed(self.get_force_of_gravity(self.moon.mass, self.objects[0].mass,
                                                         self.get_distance_between_objects(self.moon, self.objects[0])),
                               self.get_angle_of_force_of_gravity(self.objects[0], self.moon), 1 / self.fps)
        self.moon.change_speed(self.get_force_of_gravity(self.moon.mass, self.sun.mass,
                                                         self.get_distance_between_objects(self.moon, self.sun)),
                               self.get_angle_of_force_of_gravity(self.sun, self.moon), 1 / self.fps)

        self.moon.x += self.moon.speed_x * 1 / self.fps
        self.moon.y += self.moon.speed_y * 1 / self.fps

    def draw(self):
        self.screen.fill(self.bg_color)

        pygame.draw.circle(self.screen, self.sun.color, (self.sun.x, self.sun.y), self.sun.radius)
        pygame.draw.circle(self.screen, self.moon.color, (self.moon.x, self.moon.y), self.moon.radius)

        for object_ in self.objects:
            pygame.draw.circle(self.screen, object_.color, (object_.x, object_.y), object_.radius)

        pygame.display.flip()


game = Game(100)
