import statistics
from vehicle import Vehicle
from rider import Rider


class Grid:

    def __init__(self):
        self.num_row = 0
        self.num_col = 0
        self.riders = list()
        self.vehicles = list()
        self.bonus = 0
        self.max_step = 0

    def read(self, file):
        lines = [list(map(int, l.split(' '))) for l in file]
        self.num_row = lines[0][0]
        self.num_col = lines[0][1]
        num_riders = lines[0][3]
        self.bonus = lines[0][4]
        self.max_step = lines[0][5]

        self.vehicles = [Vehicle(i, bonus=self.bonus)
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
        pass
