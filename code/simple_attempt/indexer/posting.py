class Posting:

    def __init__(self, docId, frequency ) -> None:
        self.docId = docId
        self.frequency = frequency

    def __hash__(self) -> int:
        return hash(self.docId)