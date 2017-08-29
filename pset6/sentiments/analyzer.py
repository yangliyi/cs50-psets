import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.positive_words = set()
        self.negative_words = set()
        
        file = open(positives, "r")
        for line in file:
            self.positive_words.add(line.rstrip("\n"))
        file.close()
        
        file = open(negatives, "r")
        for line in file:
            self.negative_words.add(line.rstrip("\n"))
        file.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        score = 0
        words = text.split(" ")
        for word in words:
            if word in self.positive_words:
                score += 1
            elif word in self.negative_words:
                score -= 1

        return score
