# -*- coding: utf-8 -*-

import re
import unittest


NON_CAPITAL = (
    "De Los",
    "De Las",
    "De La",
    "Del",
    "De",
)

# Put \b around the patterns to only match 'de' and 'de los' surrounded by
# word boundaries
patterns = [r"\b{}\b".format(pattern)
            for pattern in NON_CAPITAL]

# Join them all into one regex to make the search faster
NON_CAPITAL_RE = re.compile(r"|".join(patterns),
                            flags=re.IGNORECASE)


def do_replacement(matchobj):
    return matchobj.group(0).lower()


def fix_spanish_title_case(text):
    """Fixes issues with prepositions in auto-titlecased spanish text. The
    input should already be in title case (first letter of each word is
    capital).

    It is a known limitation that it can not know that a word is a proper noun
    and account for that, for example: "San José de Las Américas" should have a
    capital L, because Las Americas is a proper noun.
    """
    return re.sub(NON_CAPITAL_RE, do_replacement, text)


class Test(unittest.TestCase):

    def test_de(self):
        self.assertEquals(
            fix_spanish_title_case(u"Casa De Nariño"),
            u"Casa de Nariño"
        )

    def test_del(self):
        self.assertEquals(
            fix_spanish_title_case(u"San Jacinto Del Cauca"),
            u"San Jacinto del Cauca"
        )

    def test_de_la(self):
        self.assertEquals(
            fix_spanish_title_case(u"Güicán De La Sierra"),
            u"Güicán de la Sierra"
        )

    def test_de_las(self):
        self.assertEquals(
            fix_spanish_title_case(u"Paso De Las Flores"),
            u"Paso de las Flores"
        )

    def test_de_los(self):
        # Yes, I know there's no "los" in the original version
        self.assertEquals(
            fix_spanish_title_case(u"Día De Los Muertos"),
            u"Día de los Muertos"
        )

    def test_combo(self):
        self.assertEquals(
            fix_spanish_title_case(u"María De Los Llanos De Luna Tobarra"),
            u"María de los Llanos de Luna Tobarra"
        )

    def test_case_sensitivity(self):
        self.assertEquals(
            fix_spanish_title_case(u"VILLA DE LEYVA"),
            u"VILLA de LEYVA"
        )

    def test_multi_space(self):
        self.assertEquals(
            fix_spanish_title_case(u"Paso  De Las	 Flores"),
            u"Paso  de las	 Flores"
        )
