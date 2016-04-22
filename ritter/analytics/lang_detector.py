import langdetect


class LangDetector:

    def detect(text):
        # Make the detector deterministic
        langdetect.DetectorFactory.seed = 0
        return langdetect.detect(text)
