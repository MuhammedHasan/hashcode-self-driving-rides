import copy
from collections import defaultdict, namedtuple

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

    def rider_timeline(self):

        Event = namedtuple('Event', ['time', 'rider', 'critical'])

        for r in self.riders:
            yield Event(r.earliest, r, False)
            yield Event(r.critical_time(), r, True)

    def select_best_vehicle(self, rider):
        return max(self.vehicles,
                   key=lambda x: (x.score_of_rider(rider),
                                  -x.ending_time_of_rider(rider)))

    def solve_greedy(self, sort_by='earliest'):

        # Just sort rides by earliest time and assign them to vehicle
        # with highest score with earliest ending_time

        sort_func = {
            'earliest': lambda x: x.earliest,
            'critical': lambda x: x.critical_time(),
            'latest': lambda x: x.latest
        }

        for r in sorted(self.riders, key=sort_func[sort_by]):

            v = self.select_best_vehicle(r)

            if v.is_rider_possible(r):
                v.assign_rider(r)

    def solve_less_greedy(self):

        handled_riders = set()

        for _, r, critical in sorted(self.rider_timeline(), key=lambda x: x.time):

            v = self.select_best_vehicle(r)

            if r in handled_riders:
                continue

            if (v.is_bonus_available(r) or critical) and v.is_rider_possible(r):
                v.assign_rider(r)
                handled_riders.add(r)
                continue

    def solve(self):

        set_riders = set(self.riders)

        print('Number of vehicles:%d' % len(self.vehicles))
        print('Number of riders:%d' % len(self.riders))

        for v_i, _ in enumerate(self.vehicles):

            # Dynamic programming table stores vehicles
            table = defaultdict(lambda: Vehicle(0,
                                                self.bonus,
                                                bonus_weight=self.bonus_weight))
            # -1 is vehicle which is emtpy
            table[-1] = Vehicle(0, self.bonus, bonus_weigth=self.bonus_weight)

            for i, r in enumerate(sorted(set_riders, key=lambda x: x.latest)):

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

                # import pdb
                # pdb.set_trace()

                table[i] = best_vehicle

            self.vehicles[v_i] = table[len(set_riders) - 1]

            # print([table[i].total_score for i in range(-1, len(set_riders))])

            for r in self.vehicles[v_i].riders:
                set_riders.remove(r)

            print('Vehicle %d, rider left: %d. Vehicle Score: %d Total Score: %d' %
                  (v_i, len(set_riders), self.vehicles[v_i].total_score, self.total_score()))
