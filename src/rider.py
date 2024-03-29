import random
from utils import hamming_distance


class Rider:

    def __init__(self, index, earliest, latest, start_intersection, ending_intersection, bonus):
        self.index = index
        self.earliest = earliest
        self.latest = latest
        self.start_intersection = start_intersection
        self.ending_intersection = ending_intersection
        self.bonus = bonus

    def traveling_distance(self):
        return hamming_distance(self.start_intersection,
                                self.ending_intersection)

    def distance_to_vehicle(self, vehicle):
        return hamming_distance(self.start_intersection,
                                vehicle.current_position)

    def critical_time(self):
        return self.latest - self.traveling_distance()

    def __hash__(self):
        return self.index

    def __eq__(self, other):
        return self.index == other.index

    def __lt__(self, other):
        if self.critical_time() < other.earliest:
            return True
        elif other.critical_time() < self.earliest:
            return False
        else:
            return random.choice([True, False])
