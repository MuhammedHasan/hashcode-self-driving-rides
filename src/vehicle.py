from utils import hamming_distance


class Vehicle:

    def __init__(self, index, bonus):
        self.index = index
        self.bonus = bonus
        self.rides = list()
        self.current_time = 0
        self.current_position = (0, 0)
        self.total_score = 0

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

    def score_of_rider(self, rider):
        s = 0

        if self.is_rider_possible(rider):
            s = rider.traveling_distance()

        if rider.earliest >= self.arriving_time_of_rider(rider):
            s += self.bonus

        return s

    def assign_rider(self, rider):
        self.rides.append(rider)
        self.total_score += self.score_of_rider(rider)

        self.current_time = self.ending_time_of_rider(rider)
        self.current_position = rider.ending_intersection

    def write(self, file):
        file.write('%s' % len(self.rides))

        for r in self.rides:
            file.write(' %s' % r.index)
        file.write('\n')
