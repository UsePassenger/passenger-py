import unittest

from passenger.schedule.schedule import Schedule


class TestSchedule(unittest.TestCase):
	def test_hello(self):
		s = Schedule()

		expected = 42
		actual = s.schedule()

		self.assertEqual(actual, expected)


if __name__ == '__main__':
	unittest.main()
