from Positions import Positions


class Posting:
    def __init__(self, term, doc_uri, url, freq, position):
        self.term = term  # Term
        self.url = url  # Document id or URL
        self.doc_uri = doc_uri  # Local document URI
        self.freq = freq  # Frequency count of the term
        self.positions = Positions()  # Positions: Object => Offset position of term inside the document
