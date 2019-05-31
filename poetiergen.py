#! python3.6
import itertools
import json
import os
from typing import List, Tuple, Union

import regex
import requests

import poepy_core as core
import poetiergen_calcs as calcs
import poetiergen_constants as constants
from poefilter import Category, FilterObj, Section, Style


def overwrite_bt(cat: Union[Category, Section], bt: List[str]) -> None:
    assert len(bt) > 0
    if isinstance(cat, Category):
        cat.seta([("BaseType", bt)])


def cat_to_section(section, cat):
    assert isinstance(section, Section)
    section.append(cat)


class PoeTierGenerator:
    def __init__(self, league_name: str, filter_: FilterObj, download: bool = False):
        self.league_name = league_name
        self.filter = filter_
        self.download = download

    def GenerateDivinationTiersFromTag(self, min_price: float) -> None:
        divination_exceptions = self.filter.basetypes_from_tag("DivException")
        print(divination_exceptions)
        div_garbage, div_ex = calcs.calc_div_cards(
            self.league_name, self.download, divination_exceptions
        ).as_garbo_ex(min_price, "name")
        self.filter.apply_to_tag("DivExalt", lambda cat: overwrite_bt(cat, div_ex))
        self.filter.apply_to_tag(
            "DivGarbage", lambda cat: overwrite_bt(cat, div_garbage)
        )

    def GenerateUniqueTiersFromTag(self, min_price: float) -> None:
        unique_exceptions: List[str] = self.filter.basetypes_from_tag(
            "UniquesException"
        )
        print(unique_exceptions)
        unique_garbage, unique_ex, unique_mixed = calcs.calc_uniques(
            self.league_name, self.download, unique_exceptions
        ).as_garbo_ex_mixed(min_price)
        self.filter.apply_to_tag(
            "UniquesExalt", lambda cat: overwrite_bt(cat, unique_ex)
        )
        self.filter.apply_to_tag(
            "UniquesMixed", lambda cat: overwrite_bt(cat, unique_mixed)
        )
        self.filter.apply_to_tag(
            "UniquesGarbage", lambda cat: overwrite_bt(cat, unique_garbage)
        )

    def GenerateShaperElderSectionFromTag(
        self, min_price: float, style_chaos: Style, style_ex: Style
    ) -> None:
        bases_chaos, bases_ex = calcs.calc_item_bases(
            self.league_name, self.download
        ).as_chaos_ex_frames(min_price)
        for tier, baseDataframe in enumerate((bases_ex, bases_chaos), start=1):
            for (variant, ilvl), group in baseDataframe.groupby(
                ["variant", "levelRequired"]
            ):
                base_type_list = group["baseType"].values.tolist()
                cat = Category(
                    f"Bases-{variant}-{ilvl}-T{tier}",
                    ShaperItem=True if "Shaper" in variant else None,
                    ElderItem=True if "Elder" in variant else None,
                    ItemLevel=((">=" if ilvl == 86 else "=") + f" {ilvl}")
                    if ilvl > 0
                    else None,
                    Rarity="<= Rare",
                    BaseType=base_type_list,
                    Style=style_ex if tier == 1 else style_chaos,
                )
                self.filter.apply_to_tag(
                    "ShaperElder", lambda sec: cat_to_section(sec, cat)
                )

