#!/usr/bin/env python

import os
import sys
import random
import unittest

sys.path.insert(0, os.path.abspath('..'))

from ShamirSecretSharing import *

class TestMInt(unittest.TestCase):

    def setUp(self):
        self.unity =  MInt(1, 23)
        self.zero =  MInt(0, 23)
        self.a = MInt(7, 23)
        self.b = MInt(20, 23)
        self.a_inv = self.unity / self.a

    def test_add(self):
        self.assertEqual( (self.a + self.b).n, 4)

    def test_sub(self):
        self.assertEqual( (self.a - self.b).n, 10)
        
    def test_inv(self):
        self.assertEqual( (self.a * self.a_inv).n, 1)

class TestShamir(unittest.TestCase):

    def setUp(self):
        self.bits_per_share = 256
        self.secret = random.getrandbits(1024) # length of secret in bits
        print("secret = " + str(hex(self.secret)))
        self.num_shares = 5
        self.threshold = 3
        self.prime = 950687172821200540428729809153981241192606941085199889710006512529799315561656564788637203101376144614649190146776378362001933636271697777317137481911233025291081331157135314582760768668046936978951230131371278628451555794052066356238840168982528971519323334381994143826200392654688774136120844941887558297071490087973944885778003973836311019785751636542119444349041852180595146239058424861988708991060298944680661305392492285898022705075814390941667822309754536610263449507491311215196067928669134842614154655850281748314529232542980764185554607592605321212081871630106290126123668106453941684604069442637972979374182617204123679546880646955063471680804611387541602675808433185504968764805413712115090234016146947180827040328391684056285942239977920347896230959546196177226139807640271414022569186565510341302134143539867133746492544472279859740722443892721076576952182274117616122050429733446090321598356954337536610713395670667775788540830077914016236382546944507664840405622352934380411525395863579062612404875578114927946272686172750421522119335879522375883064090902859635110578120928185659759792150776022992518497479844711483878613494426215867980856381040745252296584054718251345106582780587533445417441424957999212662923937862802426711722066998062574441680275377501049078991123518677027512513302350533057609106549686502083785061647562269181863107725160293272971931807381453849850066056697913028167183570392948696346480930400320904644898839942228059188904225142187444604612121676565893284697317106343998167640380023972222033520190994951064491572372368101650142992876761420785551386138148283615194775971673577063363049929945959258097086463812469068598955485574579363616634109593903116561526921965491646400040600138481505369027344295330767163087489333402201631708610718911106905154471963379233672543874307197342217544783263700843246351822145605839955798639016346308363889766574606793652730311687899415585873892778899179927359964882217066947566799298173326850382334054179474389651499891117938361854701587568363867264590395711833275763832842002504433841816245069655064326325306033334336469743800464944131049874472540605264250854258280373869113420817955012823462838351481855289027030577957168468047751024562853260494808998446682723835213272609799649864902376137320638444968430858790173696935815430513690803796736064125183005539073920032869713201073105497655763097638587404309062750746064609677994654409535743453776560694719663801069746654445359756195253816544699551

    def test_shamir(self):
    
        shares = split_secret(self.secret,
                              self.num_shares,
                              self.threshold,
                              self.bits_per_share,
                              self.prime)
        self.assertIsNotNone(shares)
        self.assertEqual(len(shares), self.num_shares)
        
        for s in shares:
            self.assertNotEqual(s[0].n, self.secret)
            self.assertNotEqual(s[1].n, self.secret)

        points = shares[0:self.threshold]
        new_secret = reconstruct_secret(points, self.num_shares,
                                        self.threshold, self.prime)
        self.assertIsNotNone(new_secret)
        self.assertEqual(new_secret.n, self.secret)

        points = shares[0:self.threshold+1]
        new_secret = reconstruct_secret(points, self.num_shares,
                                        self.threshold, self.prime)
        self.assertIsNotNone(new_secret)
        self.assertEqual(new_secret.n, self.secret)

        points = shares[0:self.num_shares]
        new_secret = reconstruct_secret(points, self.num_shares,
                                        self.threshold, self.prime)
        self.assertIsNotNone(new_secret)
        self.assertEqual(new_secret.n, self.secret)

        points = shares[0:self.threshold-1]
        new_secret = reconstruct_secret(points, self.num_shares,
                                        self.threshold, self.prime)
        self.assertIsNone(new_secret)

        points = shares[0:self.threshold-2]
        new_secret = reconstruct_secret(points, self.num_shares,
                                        self.threshold, self.prime)
        self.assertIsNone(new_secret)

    
if __name__ == "__main__":
    unittest.main()
