#!/usr/bin/env python

import sys
import time
import random

if sys.version_info > (3,):
    long = int


# An 8192 bit prime that is used as a default prime
DEFAULT_PRIME = 950687172821200540428729809153981241192606941085199889710006512529799315561656564788637203101376144614649190146776378362001933636271697777317137481911233025291081331157135314582760768668046936978951230131371278628451555794052066356238840168982528971519323334381994143826200392654688774136120844941887558297071490087973944885778003973836311019785751636542119444349041852180595146239058424861988708991060298944680661305392492285898022705075814390941667822309754536610263449507491311215196067928669134842614154655850281748314529232542980764185554607592605321212081871630106290126123668106453941684604069442637972979374182617204123679546880646955063471680804611387541602675808433185504968764805413712115090234016146947180827040328391684056285942239977920347896230959546196177226139807640271414022569186565510341302134143539867133746492544472279859740722443892721076576952182274117616122050429733446090321598356954337536610713395670667775788540830077914016236382546944507664840405622352934380411525395863579062612404875578114927946272686172750421522119335879522375883064090902859635110578120928185659759792150776022992518497479844711483878613494426215867980856381040745252296584054718251345106582780587533445417441424957999212662923937862802426711722066998062574441680275377501049078991123518677027512513302350533057609106549686502083785061647562269181863107725160293272971931807381453849850066056697913028167183570392948696346480930400320904644898839942228059188904225142187444604612121676565893284697317106343998167640380023972222033520190994951064491572372368101650142992876761420785551386138148283615194775971673577063363049929945959258097086463812469068598955485574579363616634109593903116561526921965491646400040600138481505369027344295330767163087489333402201631708610718911106905154471963379233672543874307197342217544783263700843246351822145605839955798639016346308363889766574606793652730311687899415585873892778899179927359964882217066947566799298173326850382334054179474389651499891117938361854701587568363867264590395711833275763832842002504433841816245069655064326325306033334336469743800464944131049874472540605264250854258280373869113420817955012823462838351481855289027030577957168468047751024562853260494808998446682723835213272609799649864902376137320638444968430858790173696935815430513690803796736064125183005539073920032869713201073105497655763097638587404309062750746064609677994654409535743453776560694719663801069746654445359756195253816544699551


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


def split_secret(secret, num_shares, threshold, bits_per_share, prime):
    """Takes the given secret and splits it using Shamir's Secret Sharing
    Algorithm.

    Args:
        secret: The secret to be split
        num_shares: The number of shares for which the secret will be split
        threshold: The minimum number of shares needed to reconstruct the
                   secret
        bits_per_share: Specifies the number of bits per share. Useful to
                        produce short and easy-to-read shares
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
    if prime.bit_length() <= bits_per_share:
        return None

    coefficients = []
    shares_xs = []
    shares = []

    # Get random (k-1) coefficients that define a k-th degree polynomial
    rng = random.SystemRandom(int(time.time()))
    for i in range(threshold - 1):
        coefficients.extend([MInt(rng.randint(1, 2**bits_per_share-1), prime)])

    # Get the x coordinates of the shares with the specified # of bits
    for i in range(num_shares):
        shares_xs.extend([rng.randint(1, 2**bits_per_share-1)])

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
