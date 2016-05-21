#!/usr/bin/env python

import sys

from .MInt import MInt


if sys.version_info > (3,):
    long = int


def reconstruct_secret(shares, num_shares, threshold, prime):
    """Reconstructs the secret using the computationally efficient approach
    explained in: https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing

    Args:
        shares: The list of shares used to reconstruct the secret
        prime: The prime used to define the Galois field in which the shares
               were computed

    Returns:
        If successful, an MInt(n,p) where n is the original secret.
        Otherwise, None
    """
    
    assert isinstance(shares, list)
    assert isinstance(num_shares, int)
    assert isinstance(threshold, int)
    assert isinstance(prime, long)
    
    if len(shares) < threshold or len(shares) > num_shares:
        return None
    
    secret = MInt(0, prime)
    
    for j in range(0, len(shares)):
        x_j = shares[j][0]
        y_j = shares[j][1]
        product = MInt(1, prime)
        for m in range(0, len(shares)):
            x_m = shares[m][0]
            if m != j:
                product *= (x_m / (x_m - x_j))
        secret += (y_j * product)
    return secret
