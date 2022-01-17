class JobBuffer(object):
    def __init__(self, iterator):
        self.iter = iterator

    def nextN(self, n):
        vals = []
        try:
            for _ in range(n):
                vals.append(next(self.iter))
            return vals, False
        except StopIteration as e:
            return vals, True
