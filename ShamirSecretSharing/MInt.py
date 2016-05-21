#!/usr/bin/env python


class MInt(object):
    """Represents an integer in Galois Field p
    """
    def __init__(self, n, p):
        """Construct a integer n mod p"""
        # TODO: check if p is prime
        self.n = n % p
        self.p = p

    def __repr__(self):
        return "MInt(%s, %s)" % (self.n, self.p)

    def __add__(self, other):
        assert isinstance(other, MInt)
        assert self.p == other.p
        return MInt(self.n + other.n, self.p)

    def __sub__(self, other):
        assert isinstance(other, MInt)
        assert self.p == other.p
        return MInt(self.n - other.n, self.p)

    def __mul__(self, other):
        assert isinstance(other, MInt)
        assert self.p == other.p
        return MInt(self.n * other.n, self.p)

    def __div__(self, other):
        assert isinstance(other, MInt)
        assert self.p == other.p
        return self * other.inverse()

    def __truediv__(self, other):
        assert isinstance(other, MInt)
        assert self.p == other.p
        return self * other.inverse()

    def __pow__(self, other):
        assert isinstance(other, int)
        result = MInt(1, self.p)
        for i in range(0, other):
            result = result * self
        return result

    def inverse(self):
        """Compute the inverse of n modulo p
        Taken from: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
        """
        t = 0; newt = 1
        r = self.p; newr = self.n
        while newr != 0:
            quotient = r // newr
            (t, newt) = (newt, t - quotient * newt)
            (r, newr) = (newr, r - quotient * newr)
        if r > 1: raise Exception(self + " is not invertible!")
        if t < 0: t = t + self.p
        return MInt(t, self.p)

