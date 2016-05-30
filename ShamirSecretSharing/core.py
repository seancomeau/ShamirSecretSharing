#!/usr/bin/env python

import sys
import time
import random

if sys.version_info > (3,):
    long = int


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


def split_secret(secret, num_shares, threshold, prime):
    """Takes the given secret and splits it using Shamir's Secret Sharing
    Algorithm.

    Args:
        secret: The secret to be split
        num_shares: The number of shares for which the secret will be split
        threshold: The minimum number of shares needed to reconstruct the
                   secret
        prime: A prime number that is used as the basis of the Galois field
               in which all the arithmetic is done

    Returns:
        If successful, a list of tuples (long, long) containing the shares
        of the split secret. Otherwise, None.
    """

    if num_shares < 1 or threshold < 1 or threshold > num_shares:
        return None
    if num_shares >= prime or threshold >= prime or secret >= prime:
        return None

    coefficients = []
    shares_xs = []
    shares = []

    # Get random (k-1) coefficients that define a k-th degree polynomial
    rng = random.SystemRandom(int(time.time()))
    for i in range(threshold - 1):
        coefficients.extend([MInt(rng.randint(1, prime - 1), prime)])

    # Get the x coordinates of the shares
    for i in range(num_shares):
        shares_xs.extend([rng.randint(1, prime - 1)])

    # Evaluate the polynomial for each x to produce the corresponding y
    for x in shares_xs:
        y = MInt(secret, prime)
        degree = 1
        xm = MInt(x, prime)
        for i in coefficients:
            y += i * pow(xm, degree)
            degree += 1
        shares.append((xm.n, y.n))

    # Check if the shares are OK
    assert len(shares) == num_shares
    for s in shares:
        assert s[0] != secret and s[1] != secret
    return shares


def print_shares(shares):
    """Prints the shares given by ShamirSecretSharing.split

    Args:
        shares: A list of tuples (long, long) containing the shares
                in (x, y) form
    """

    assert isinstance(shares, list)

    sys.stdout.write("="  * 80 + "\n")
    sys.stdout.write(" " * 30 + " List of shares " + "\n")
    sys.stdout.write("="  * 80 + "\n")
    i = 1
    for s in shares:
        sys.stdout.write("Share %s: \n" % (i))
        i += 1
        sys.stdout.write("\t" + "Part 1: " + hex(s[0]) + "\n")
        sys.stdout.write("\t" + "Part 2: " + hex(s[1]) + "\n")
    sys.stdout.write("="  * 80 + "\n")


def reconstruct_secret(shares, prime):
    """Reconstructs the secret using the computationally efficient approach
    explained in: https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing

    Args:
        shares: The list of shares used to reconstruct the secret
        prime: The prime used to define the Galois field in which the shares
               were computed

    Returns:
        If given enough shares (i.e., >= threshold), the reconstructed secret.
    """

    assert isinstance(shares, list)
    assert isinstance(prime, long)

    for s in shares:
        assert prime > s[0] and prime > s[1]

    secret = MInt(0, prime)

    for j in range(0, len(shares)):
        x_j = MInt(shares[j][0], prime)
        y_j = MInt(shares[j][1], prime)
        product = MInt(1, prime)
        for m in range(0, len(shares)):
            x_m = MInt(shares[m][0], prime)
            if m != j:
                product *= (x_m / (x_m - x_j))
        secret += (y_j * product)
    return secret.n
