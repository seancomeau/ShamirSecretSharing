#ifndef SHAMIR_SECRET_SHARING_H_
#define SHAMIR_SECRET_SHARING_H_

#include <gmp.h>

int split_secret(const mpz_t secret,
                 const unsigned int num_shares,
                 const unsigned int threshold,
                 const mpz_t prime,
                 mpz_t * shares_xs,
                 mpz_t * shares_ys);

int reconstruct_secret(const unsigned int num_shares,
                       const mpz_t * shares_xs,
                       const mpz_t * shares_ys,
                       const mpz_t prime,
                       mpz_t secret);

#endif
