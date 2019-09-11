import unittest
from air_conditioner import *
from heat_pump import *

class COPTests(unittest.TestCase):
    
    def test_air_conditioner(self):
        print "\nTesting ACs:"
        seers = [8, 10, 13, 14, 15]
        expected_cops_cooling = [2.47, 3.18, 4.00, 4.38, 4.77]
        for i in range(len(seers)):
            print "SEER = %s..." % seers[i]
            cop_cooling = calc_air_conditioner_COP(seers[i])
            self.assertEqual(expected_cops_cooling[i], round(cop_cooling, 2))

    def test_heat_pump(self):
        print "\nTesting HPs:"
        seers = [8, 10, 13, 14, 15]
        hspfs = [6.0, 6.2, 7.7, 8.2, 8.5]
        expected_cops_cooling = [2.49, 3.22, 4.04, 4.42, 4.81]
        expected_cops_heating = [2.38, 2.47, 3.09, 3.35, 3.51]
        for i in range(len(seers)):
            print "SEER = %s, HSPF=%s..." % (seers[i], hspfs[i])
            cop_cooling, cop_heating = calc_heat_pump_COPs(seers[i], hspfs[i])
            self.assertEqual(expected_cops_cooling[i], round(cop_cooling, 2))
            self.assertEqual(expected_cops_heating[i], round(cop_heating, 2))

if __name__ == '__main__':
    unittest.main()