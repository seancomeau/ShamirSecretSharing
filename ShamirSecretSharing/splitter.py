#!/usr/bin/env python

import sys
import argparse

from split_secret import *

if sys.version_info > (3,):
    long = int

def main():
    parser = argparse.ArgumentParser(description="Secret Splitter")
    parser.add_argument('--number', type=int, required=True,
           help='Number of shares to which the secret will be split')
    parser.add_argument('--threshold', type=int, required=True,
           help='Minimum number of shares needed to reconstruct the secret')
    parser.add_argument('--secret', type=long, required=True,
           help='The secret to be split (used only in the split mode)')
    parser.add_argument('--bits-per-share', type=int, default=256,
           help='Bits per share')
    parser.add_argument('--prime', type=long,
           default=DEFAULT_PRIME,
           help='Prime used as the basis of Galois field')
    
    args = parser.parse_args()
  
    shares = split_secret(args.secret,
                          args.number,
                          args.threshold,
                          args.bits_per_share,
                          args.prime)
    if shares == None:
        sys.stderr.write("Error: Unable to split secret!\n")
    else:
        print_shares(shares)
        

if __name__ == "__main__":
    main()
    sys.exit(0)
