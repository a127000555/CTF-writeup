import itertools


class RNG(object):
    def __init__(self, M, iv):
        self.M = M
        for i in itertools.count():
            if (M >> i) == 0:
                break
        self.max = (1 << (i - 1))
        self.entropy_pool = iv

    def mix(self):
        self.entropy_pool *= 2
        if self.entropy_pool >= self.max:
            self.entropy_pool ^= self.M
            return 1
        return 0

    def entropy_from_keyboard(self, x, nbits):
        for _ in range(nbits):
            self.mix()
        self.entropy_pool ^= x

    def extract(self, nbits):
        r = 0
        for _ in range(nbits):
            r = (r << 1) + self.mix()
        return r
