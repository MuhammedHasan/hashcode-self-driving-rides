import copy
import statistics
from collections import defaultdict

from vehicle import Vehicle
from rider import Rider


class Grid:

    def __init__(self):
        self.num_row = 0
        self.num_col = 0
        self.riders = list()
        self.vehicles = list()
        self.bonus = 0
        self.bonus_weight = 1
        self.max_step = 0

    def read(self, file):
        lines = [list(map(int, l.split(' '))) for l in file]
        self.num_row = lines[0][0]
        self.num_col = lines[0][1]
        num_riders = lines[0][3]
        self.bonus = lines[0][4]
        self.max_step = lines[0][5]

        self.vehicles = [Vehicle(i,
                                 bonus=self.bonus,
                                 bonus_weigth=self.bonus_weight)
                         for i in range(lines[0][2])]

        rider_index = 0
        for l in lines[1:]:
            r = Rider(
                index=rider_index,
                start_intersection=(l[0], l[1]),
                ending_intersection=(l[2], l[3]),
                earliest=l[4],
                latest=l[5],
                bonus=self.bonus
            )
            self.riders.append(r)
            rider_index += 1

    def write(self, file):
        for v in self.vehicles:
            v.write(file)

    def total_score(self):
        return sum([v.total_score for v in self.vehicles])

    def solve_greedy(self):

        # Just sort rides by earliest time and assign them to vehicle
        # with highest score with earliest ending_time

        for r in sorted(self.riders, key=lambda x: x.earliest):

            v = max(self.vehicles,
                    key=lambda x: (x.score_of_rider(r),
                                   -x.ending_time_of_rider(r)))

            if v.is_rider_possible(r):
                v.assign_rider(r)

    def solve(self):

        set_riders = set(self.riders)

        print('Number of vehicles:%d' % len(self.vehicles))
        print('Number of riders:%d' % len(self.riders))

        for v_i, _ in enumerate(self.vehicles):

            # Dynamic programming table stores vehicles
            table = defaultdict(lambda: Vehicle(0,
                                                self.bonus,
                                                bonus_weight=self.bonus_weight))
            table[-1] = Vehicle(0, self.bonus, bonus_weigth=self.bonus_weight)

            for i, r in enumerate(sorted(set_riders, key=lambda x: (x.earliest, x.latest))):

                best_vehicle = table[i - 1]
                best_score = table[i - 1].weighted_total_score
                assigned = False

                for j in list(range(-1, i)):
                    v = table[j]

                    new_score = v.score_of_rider(r, weighted=True)
                    new_score += v.weighted_total_score

                    if new_score > best_score:
                        best_vehicle = v
                        best_score = new_score
                        assigned = True

                if assigned:
                    best_vehicle = copy.deepcopy(best_vehicle)
                    best_vehicle.assign_rider(r)

                table[i] = best_vehicle

            self.vehicles[v_i] = table[len(set_riders) - 1]

            for r in self.vehicles[v_i].riders:
                set_riders.remove(r)

            print('Vehicle %d, rider left: %d' % (v_i, len(set_riders)))
