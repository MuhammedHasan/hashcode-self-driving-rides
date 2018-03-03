import unittest
from grid import Grid
from rider import Rider
from vehicle import Vehicle
from utils import hamming_distance


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.g = Grid()
        with open('../inputs/a_example.in') as f:
            self.g.read(f)

    def test_read(self):
        self.assertEqual(len(self.g.vehicles), 2)
        self.assertEqual(len(self.g.riders), 3)
        self.assertEqual(self.g.bonus, 2)
        self.assertEqual(self.g.riders[0].start_intersection, (0, 0))
        self.assertEqual(self.g.riders[0].ending_intersection, (1, 3))
        self.assertEqual(self.g.riders[0].earliest, 2)
        self.assertEqual(self.g.riders[0].latest, 9)

    def test_solve_greedy(self):
        pass

    def test_solve(self):
        pass

    def test_write(self):
        with open('../outputs/a_example.testing.txt', 'w') as f:
            self.g.solve_greedy()
            self.g.write(f)


class TestVehicle(unittest.TestCase):

    def setUp(self):
        self.rider = Rider(0, 2, 10, (1, 1), (4, 4), 2)
        self.next_rider = Rider(0, 9, 15, (2, 2), (3, 3), 2)
        self.vehicle = Vehicle(0, 2)

    def test_distance_to_rider(self):
        self.assertEqual(self.vehicle.distance_to_rider(self.rider), 2)

    def test_arriving_time_of_rider(self):
        self.assertEqual(self.vehicle.arriving_time_of_rider(self.rider), 2)

    def test_waiting_time(self):
        self.assertEqual(self.vehicle.waiting_time(self.rider), 0)

    def test_starting_time_of_rider(self):
        self.assertEqual(self.vehicle.starting_time_of_rider(self.rider), 2)

    def test_ending_time_of_rider(self):
        self.assertEqual(self.vehicle.ending_time_of_rider(self.rider), 8)

    def test_is_rider_possible(self):
        self.assertTrue(self.vehicle.is_rider_possible(self.rider))

    def test_score_of_rider(self):
        self.assertEqual(self.vehicle.score_of_rider(self.rider), 8)

    def test_assign_rider(self):
        self.vehicle.assign_rider(self.rider)

        self.assertEqual(self.vehicle.current_position, (4, 4))
        self.assertEqual(self.vehicle.current_time, 8)


class TestRider(unittest.TestCase):

    def setUp(self):
        self.rider = Rider(0, 2, 10, (1, 1), (4, 4), 2)
        self.next_rider = Rider(0, 9, 15, (2, 2), (3, 3), 2)
        self.vehicle = Vehicle(0, 2)

    def test_distance_to_vehicle(self):
        self.assertEqual(self.rider.distance_to_vehicle(self.vehicle), 2)


class TestUtils(unittest.TestCase):

    def test_hamming_distance(self):
        p1 = (2, 2)
        p2 = (4, 4)
        self.assertEqual(hamming_distance(p1, p2), 4)


if __name__ == '__main__':
    unittest.main()
