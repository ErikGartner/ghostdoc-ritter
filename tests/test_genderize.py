import unittest

from ritter.analytics.genderize import Genderize


class GenderizeTest(unittest.TestCase):
    def test_extract_gem(self):
        gender = Genderize.guess_from_name('Erik')
        self.assertEquals(gender, 'male')
