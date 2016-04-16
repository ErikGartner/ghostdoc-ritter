import langdetect


class LangDetector:

    def detect(text):
        langdetect.DetectorFactory.seed = 0
        return langdetect.detect(text)
