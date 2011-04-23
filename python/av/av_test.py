from av import election
from av import round_one
import unittest

class AVTest(unittest.TestCase):

    def setUp(self):
        self.votes = {'FPTP':(28, 0, 21, 51), 'SV':(27, 24, 28, 21), 'AV': (27, 48, 0, 28), 'Borda': (21, 28, 51, 0)}

    def test_round_one(self):
        self.assertEquals('FPTP', round_one(30, self.votes))
        self.assertEquals(None, round_one(100, self.votes))

    def test_bbc(self):
        """ http://www.bbc.co.uk/blogs/opensecrets/2010/02/alternative_voting_systems_for_choosing_a_voting_system.html
        """
        voters = 100
        winner = election(voters, self.votes)
        self.assertEquals(winner, 'AV')

if __name__ == '__main__':
    unittest.main()
