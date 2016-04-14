import json

import gender_guesser.detector as gender


class Genderize():

    detector = gender.Detector(case_sensitive=False)

    def guess_from_name(firstname):
        g = Genderize.detector.get_gender(firstname)
        return g
