ShamirSecretSharing
===================

.. image:: https://travis-ci.org/mohamed/ShamirSecretSharing.svg?branch=master
    :target: https://travis-ci.org/mohamed/ShamirSecretSharing

This is a minimalist and yet complete implementation of Shamir's Secret Sharing
Algorithm as described in [JACM1979]_.
The goal is to provide, as much as possible, a generic and efficient
implementation.
There are two ports of the algorithm in two languages: C and Python.
Each port can be used separately from the other.

.. [JACM1979]
   Adi Shamir, "How to share a secret", Communications of the ACM 22(11):612-613
   doi:10.1145/359168.359176

Requirements
------------
To run the C port, you will need a C89 compiler and libgmp_

.. _libgmp: https://gmplib.org/

To run the Python port, you will need Python_ 2.7+

.. _Python: http://www.python.org/

Bugs/Questions
--------------
In case of bugs/questions, please contact me on Github_

.. _Github: https://github.com/mohamed
