import os
from importlib import reload
from typing import List, Tuple

import numpy as np
import pandas as pd

import neversink_processing as neversink
import poepy_core as poepy
from poetiergen_constants import (
    NotDroppedList,
    bases_useless_columns,
    json_bases_filepath,
    json_div_filepath,
    json_unique_filepaths,
)

# Div Card Tiering:


def calc_div_cards(
    min_price: float, json_data: List[dict] = None, exceptions: List[str] = []
) -> Tuple[List[str], List[str]]:
    json_data = (
        json_data if json_data is not None else poepy.FileToJson(json_div_filepath)
    )
    df = pd.DataFrame(json_data)
    df = df[~df["name"].isin(exceptions)]
    df.loc[:, "confidence"] = df.apply(neversink.evaluate_div_cards, axis=1)
    df.loc[:, "aValue"] = df.apply(lambda x: x["chaosValue"] * x["confidence"], axis=1)

    # cdf = df.query(f'aValue >= {min_price}')
    m = df["aValue"] >= min_price
    cdf, garbo = df[m], df[~m]
    # m = cdf['exaltedValue'] >= 1
    # ex, chaos = df[m], df[~m]
    ex = cdf[cdf.exaltedValue >= 1]
    return garbo["name"].values.tolist(), ex["name"].values.tolist()


# Uniques Tiering:


def calc_uniques(
    min_price: float, json_data: List[List[dict]] = None, exceptions: List[str] = []
) -> Tuple[List[str], List[str], List[str]]:
    json_data = (
        json_data
        if json_data is not None
        else [poepy.FileToJson(js) for js in json_unique_filepaths]
    )
    df = pd.concat((pd.DataFrame(f) for f in json_data), ignore_index=True, sort=True)
    df = df[~df["baseType"].isin(exceptions)]
    df = df.query(
        "name not in @NotDroppedList and links < 5"
    )  # doing df[~df['name'].isin(NotDroppedList)][df['links']<5] is slightly faster but looks worse v0v
    gvq = df.groupby("baseType")
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


# Bases Tiering:


def calc_item_bases(
    min_price: float, json_data: List[dict] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    json_data = (
        json_data if json_data is not None else poepy.FileToJson(json_bases_filepath)
    )
    df = pd.DataFrame(json_data)
    # df['variant'].fillna('Normal', inplace=True)
    df = df[pd.notnull(df["variant"])]

    df = df.drop(columns=bases_useless_columns)

    gvq = df.groupby(["variant", "baseType"])

    def fun(group):
        group["confidence"] = neversink.evaluate_bases(group)
        return group

    df = gvq.apply(fun)
    df.loc[:, "aValue"] = df.apply(
        lambda x: x["chaosValue"] * x["confidence"] if x["confidence"] > 0.35 else 0,
        axis=1,
    )

    cdf = df.query(f"aValue >= {min_price}")  # minimum count for normal variant items
    m = cdf["exaltedValue"] >= 1
    ex, chaos = cdf[m], cdf[~m]
    return chaos, ex


# calc_item_bases(poepy.FileToJson(json_filepath))
# calc_div_cards(poepy.FileToJson(json_filepath))


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
