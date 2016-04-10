import unittest

from ritter.gemextractor import GemExtractor


class GemExtractorTest(unittest.TestCase):
    def test_sentence_reg(self):
        sentences = 'Hej mitt namn är Erik, jag är 18 år. Kolla mitt fräcka hår.'
        tokens = ['erik', '18']
        result = GemExtractor.sentence_reg(tokens).findall(sentences)
        self.assertEquals(['Hej mitt namn är Erik, jag är 18 år'], result)

    def test_extract_gem(self):
        text = 'Hej mitt namn är Erik, jag föddes 18 år gammal. Kolla mitt fräcka hår.'
        patterns = ['född[\D]*(\d+)', '(\d+)[\D]*född']
        tokens = ['Erik', '18']
        gem = {'patterns': patterns, 'name': 'föddes'}
        artifact = {'tokens': tokens}

        result = GemExtractor.extract_gem(text, gem, artifact)
        self.assertEquals({'name': 'föddes', 'result': ['18']}, result)
