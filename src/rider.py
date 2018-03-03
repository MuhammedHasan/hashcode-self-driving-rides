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

    # def previous_closed_rides(self, vehicle, all_rides, n=1):
    #     return list(sorted(
    #         (r, self.distance_to_next_ride(r, vehicle))
    #         for r in all_rides if vehicle.is_ride_possible(r)
    #     ), key=lambda x: x[1])[:n]
