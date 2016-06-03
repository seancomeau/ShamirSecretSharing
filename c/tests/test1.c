#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "shamir.h"

static char prime_str[] = "909360333829";
/*
static char prime_str[] = "99841919439086972575966613294336707043187599755217949770531510008839389836622547768737989201532734716581829276354290861030105561174914071295723476589851843080570268095259917196351155871135120258740477256817507765273392027358601370895330743206712568620809026896843546323934476302562679731624877889014673367723";
*/

int main()
{
    int retval = 0;
    unsigned int i  = 0;
    mpz_t secret, prime, xs[5], ys[5];
    mpz_t reconstructed;

    mpz_init_set_str(secret, "1234", 10);
    mpz_init_set_str(prime, prime_str, 10);
    retval = split_secret(secret, 5, 3, prime, xs, ys);
    assert(retval == EXIT_SUCCESS);
    retval = reconstruct_secret(3, (const mpz_t *)xs, (const mpz_t *)ys,
                                prime, reconstructed);
    printf("retval = %d\n", retval);
    assert(mpz_cmp(reconstructed, secret) == 0);
    for (i = 0; i < 5; i++) {
        gmp_printf("Share %d: part 1 = %Zd - part 2 = %Zd\n", i, xs[i], ys[i]);
        mpz_clear(xs[i]);
        mpz_clear(ys[i]);
    }
    gmp_printf("reconstructed secret = %Zd\n", reconstructed);
    mpz_clear(secret);
    mpz_clear(reconstructed);
    mpz_clear(prime);
    return EXIT_SUCCESS;
}
