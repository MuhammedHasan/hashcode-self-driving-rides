import copy
from utils import hamming_distance


class Vehicle:

    def __init__(self, index, bonus, bonus_weigth=1):
        self.index = index
        self.bonus = bonus
        self.bonus_weigth = bonus_weigth
        self.riders = list()
        self.current_time = 0
        self.current_position = (0, 0)
        self.total_score = 0
        self.weighted_total_score = 0

    def distance_to_rider(self, rider):
        return rider.distance_to_vehicle(self)

    def arriving_time_of_rider(self, rider):
        return self.distance_to_rider(rider) + self.current_time

    def waiting_time(self, rider):
        return max(rider.earliest - self.arriving_time_of_rider(rider), 0)

    def starting_time_of_rider(self, rider):
        return self.arriving_time_of_rider(rider) + self.waiting_time(rider)

    def ending_time_of_rider(self, rider):
        return self.starting_time_of_rider(rider) + rider.traveling_distance()

    def is_rider_possible(self, rider):
        return rider.latest >= self.ending_time_of_rider(rider)

    def is_bonus_available(self, rider):
        return rider.earliest >= self.arriving_time_of_rider(rider)

    def score_of_rider(self, rider, weighted=False):
        s = 0

        if self.is_rider_possible(rider):
            s = rider.traveling_distance()

        if self.is_bonus_available(rider):
            s += self.bonus * self.bonus_weigth if weighted else self.bonus

        return s

    def assign_rider(self, rider):
        self.riders.append(rider)
        self.total_score += self.score_of_rider(rider)
        self.weighted_total_score += self.score_of_rider(rider, weighted=True)

        self.current_time = self.ending_time_of_rider(rider)
        self.current_position = rider.ending_intersection

    def write(self, file):
        file.write('%s' % len(self.riders))

        for r in self.riders:
            file.write(' %s' % r.index)
        file.write('\n')

    def clone(self):
        return copy.deepcopy(self)
