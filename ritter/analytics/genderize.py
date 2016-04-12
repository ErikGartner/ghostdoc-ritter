import json

import requests


class Genderize():

    def guess_from_name(firstname):
        r = requests.get('https://api.genderize.io/?name=%s' % firstname)
        j = json.loads(r.text)
        if j['gender'] is None:
            return (None, None)
        return (j['gender'], j['probability'])
