import os
from importlib import reload
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd

import neversink_processing as neversink
import poepy_core as core
from poetiergen_constants import (
    NotDroppedList,
    bases_useless_columns,
    divs_useless_columns,
    uniques_useless_columns,
    json_bases_filepath,
    json_div_filepath,
    json_unique_filepaths,
)


class EvaluatedData:
    def __init__(self, type_: str, data: pd.DataFrame) -> None:
        self.type = type_
        self.data = data

    def as_json(self, file_name: Optional[str] = None, col: str = None) -> str:
        fx_data: Union[pd.DataFrame, pd.Series] = self.data
        if col is not None:
            fx_data = fx_data.groupby(col).apply(lambda g: g.to_dict(orient="records"))
        if file_name is not None:
            fx_data.to_json(path_or_buf=file_name)
        return fx_data.to_json()

    def as_garbo_ex(
        self, min_price: float, col: str = "baseType"
    ) -> Tuple[List[str], List[str]]:
        m = self.data["aValue"] >= min_price
        cdf, garbo = self.data[m], self.data[~m]
        ex = cdf[cdf.exaltedValue >= 1]
        return garbo[col].values.tolist(), ex[col].values.tolist()

    def as_garbo_ex_mixed(
        self, min_price, col: str = "baseType"
    ) -> Tuple[List[str], List[str], List[str]]:
        gvq = self.data.groupby("baseType")
        garbo, ex, mixed = [], [], []
        for bt, group in gvq:
            if group.sort_values(by="exaltedValue")["exaltedValue"].iat[0] >= 1:
                ex.append(bt)
            else:
                maxPrice = group["chaosValue"].max()
                if maxPrice < min_price:
                    garbo.append(bt)
                elif maxPrice >= min_price and group["chaosValue"].min() < min_price:
                    mixed.append(bt)
        return garbo, ex, mixed

    def as_chaos_ex_frames(self, min_price: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
        cdf = self.data.query(
            f"aValue >= {min_price}"
        )  # minimum count for normal variant items
        m = cdf["exaltedValue"] >= 1
        ex, chaos = cdf[m], cdf[~m]
        return chaos, ex


# Div Card Tiering:


class PoeTierCalculator:
    def __init__(
        self, league: str = None, download: bool = False, use_cache: bool = True
    ):
        self.league = league
        self.download = download
        self.use_cache = use_cache

    def calc_div_cards(self,
        exceptions: List[str] = []
    ) -> EvaluatedData:
        json_data = (
            core.GetDivinationData(self.league, self.download, self.use_cache)
            if self.download
            else core.FileToJson(json_div_filepath)
        )
        df = pd.DataFrame.from_records(json_data, exclude=divs_useless_columns)
        df = df[~df["name"].isin(exceptions)]
        df.loc[:, "confidence"] = df.apply(neversink.evaluate_div_cards, axis=1)
        df.loc[:, "aValue"] = df["chaosValue"] * df["confidence"]
        df = df[["chaosValue", "exaltedValue", "name", "aValue"]]

        return EvaluatedData("DivinationCard", df)


    # Uniques Tiering:


    def calc_uniques(self,
        exceptions: List[str] = []
    ) -> EvaluatedData:
        json_data = (
            core.GetUniquesData(self.league, self.download, self.use_cache)
            if self.download
            else [core.FileToJson(js) for js in json_unique_filepaths]
        )
        df = pd.concat(
            (
                pd.DataFrame.from_records(f, exclude=uniques_useless_columns)
                for f in json_data
            ),
            ignore_index=True,
            sort=True,
        )
        df = df[~df["baseType"].isin(exceptions)]
        df = df[(~df["name"].isin(NotDroppedList)) & (df["links"] < 5)]
        df = df[["baseType", "chaosValue", "exaltedValue", "name"]]
        return EvaluatedData("Uniques", df)


    # Bases Tiering:

    # 5.11 s ± 22.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    def calc_item_bases(self) -> EvaluatedData:
        json_data = (
            core.GetBasesData(self.league, self.download, self.use_cache)
            if self.download
            else core.FileToJson(json_bases_filepath)
        )
        df = pd.DataFrame.from_records(json_data, exclude=bases_useless_columns)
        df = df[pd.notnull(df["variant"])]
        gvq = df.groupby(["variant", "baseType"])

        def fun(group):
            group["confidence"] = neversink.evaluate_bases(group)
            return group

        df = gvq.apply(fun)

        m = df["confidence"] > 0.35
        df.loc[m, "aValue"] = df[m]["chaosValue"] * df[m]["confidence"]
        df.loc[~m, "aValue"] = 0
        df = df[
            ["baseType", "chaosValue", "exaltedValue", "aValue", "variant", "levelRequired"]
        ]
        return EvaluatedData("ShaperElder", df)


# Pandas snippets

# df.apply(lambda x: x['chaosValue']*x['confidence'] if x['confidence'] > 0.35 else 0, axis=1)

# base_groups = df.query('count >= 5 & chaosValue >= 21').groupby(['variant','levelRequired'])
# data = df.query('baseType == "Gilded Sallet" and variant == "Elder"')['chaosValue'].describe()
# for (n1, n2), group in gvq:
# confidence = neversink.evaluate(n1, n2, group)
# df['confidence'] = group.groupby(group.index)['baseType'].transform(lambda x: fun(n1, n2, group))
# if poepy.InvestigatedItem((n2, n1)):
#     print(group.dtypes)
# print(f'{confidence}')

# ' '.join(gvq.get_group(('Shaper', 86))['baseType'])

# gvq.get_group(('Shaper', 86)).loc[:,['baseType', 'chaosValue']]


# artFilename                object
# baseType                   object
# chaosValue                float64
# corrupted                    bool
# count                       int64
# detailsId                  object
# exaltedValue              float64
# explicitModifiers          object
# flavourText                object
# gemLevel                    int64
# gemQuality                  int64
# icon                       object
# id                          int64
# implicitModifiers          object
# itemClass                   int64
# itemType                   object
# levelRequired               int64
# links                       int64
# lowConfidenceSparkline     object
# mapTier                     int64
# name                       object
# prophecyText               object
# sparkline                  object
# stackSize                   int64
# variant                    object
