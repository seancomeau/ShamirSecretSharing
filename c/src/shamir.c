#include <stdlib.h>
#include <time.h>
#include <errno.h>
#include <assert.h>

#include <gmp.h>

#include "shamir.h"

#define SUCCESS (EXIT_SUCCESS)

int split_secret(const mpz_t secret,
                 const unsigned int num_shares,
                 const unsigned int threshold,
                 const mpz_t prime,
                 mpz_t * shares_xs,
                 mpz_t * shares_ys)
{
    unsigned int i = 0, j = 0;
    size_t prime_size = 0;
    int retval = SUCCESS;
    mpz_t * coefficients = NULL;
    mpz_t y, tmp, degree;
    gmp_randstate_t rng_state;

    /* Check the inputs */
    if (mpz_cmp(secret, prime) >= 0 ||
        shares_xs == NULL || shares_ys == NULL ||
        threshold > num_shares || threshold < 1 || num_shares < 1) {
        return EINVAL;
    }
    
    coefficients = (mpz_t *) malloc((threshold - 1) * sizeof(mpz_t));
    if (coefficients == NULL) {
        return ENOMEM;
    }

    srand(time(NULL));
    gmp_randinit_default(rng_state);
    gmp_randseed_ui(rng_state, rand());
    prime_size = mpz_sizeinbase(prime, 2);
 
    /* Initialize coefficients and shares_xs */   
    for (i = 0; i < (threshold - 1); i++) {
        mpz_init(coefficients[i]);
        mpz_urandomb(coefficients[i], rng_state, prime_size - 1);
        mpz_add_ui(coefficients[i], coefficients[i], 1);
    }
    
    for (i = 0; i < num_shares; i++) {
        mpz_init(shares_xs[i]);
        mpz_urandomb(shares_xs[i], rng_state, prime_size - 1);
        mpz_add_ui(shares_xs[i], shares_xs[i], 1);
    }

    mpz_init(tmp);
    for (i = 0; i < num_shares; i++) {
        mpz_init_set(y, secret);
        mpz_init_set_ui(degree, 1);
        for (j = 0; j < (threshold - 1); j++) {
            mpz_powm_sec(tmp, shares_xs[i], degree, prime);
            mpz_addmul(y, coefficients[j], tmp);
            mpz_add_ui(degree, degree, 1);
        }
        mpz_clear(degree);
        mpz_init(shares_ys[i]);
        mpz_mod(y, y, prime);
        mpz_set(shares_ys[i], y);
        mpz_clear(y);
        if (mpz_cmp(shares_xs[i], secret) == 0 ||
            mpz_cmp(shares_ys[i], secret) == 0) {
            retval = EINVAL;
            break;
        }

    }
    mpz_clear(tmp);

    if (retval != SUCCESS) {
        for (i = 0; i < num_shares; i++) {
            mpz_init_set_ui(shares_xs[i], 0);
            mpz_init_set_ui(shares_ys[i], 0);
        }
    }

    gmp_randclear(rng_state);
    /* Clear data */
    for (i = 0; i < (threshold - 1); i++) {
        mpz_clear(coefficients[i]);
    }
    free(coefficients);
    coefficients = NULL;

    return retval;
}


int reconstruct_secret(const unsigned int num_shares,
                       const mpz_t * shares_xs,
                       const mpz_t * shares_ys,
                       const mpz_t prime,
                       mpz_t secret)
{
    unsigned int j = 0, m = 0;
    int retval = -1;
    mpz_t product, d, r;
    mpz_t reconstructed;

    if (shares_xs == NULL || shares_ys == NULL) {
        return EINVAL;
    }

    for (j = 0; j < num_shares; j++) {
        if (mpz_cmp(shares_xs[j], prime) >= 0 ||
            mpz_cmp(shares_ys[j], prime) >= 0) {
            return EINVAL;
        }
    }
    
    mpz_init_set_ui(reconstructed, 0);
    
    for (j = 0; j < num_shares; j++) {
        mpz_init_set_ui(product, 1);
        for (m = 0; m < num_shares; m++) {
            mpz_init(d);
            mpz_init(r);
            if (m != j) {
                mpz_sub(d, shares_xs[m], shares_xs[j]);
                retval = mpz_invert(d, d, prime);
                assert(retval != 0);
                mpz_mul(r, shares_xs[m], d);
                mpz_mul(product, product, r);
            }
            mpz_clear(d);
            mpz_clear(r);
        }
        mpz_addmul(reconstructed, shares_ys[j], product);
        mpz_mod(reconstructed, reconstructed, prime);
        mpz_clear(product);
    }
    mpz_init_set(secret, reconstructed);
    mpz_clear(reconstructed);

    return SUCCESS;
}
