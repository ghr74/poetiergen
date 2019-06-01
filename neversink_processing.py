# MIT License

# Copyright (c) 2019 NeverSink

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from poepy_core import ternary, CodeTimer
import pandas as pd
import decimal

ns_drop_level_ignored_classes = {
    "rings",
    "amulets",
    "belts",
    "jewels",
    "daggers",
    "wands",
    "sceptres",
}

averagePriceMinimum = 3
approvedPricesMinimum = 8
unhealthyPriceRange = 500
# https://www.filterblade.xyz/datafiles/other/BasetypeStorage.csv
bt = pd.read_csv("BasetypeStorage.csv", usecols=["BaseType", "Class", "DropLevel"])


def evaluate_div_cards(data: pd.DataFrame) -> float:
    confidence = 1.0
    stackSize = data["stackSize"]

    confidence += ternary(stackSize <= 1, 0.2)
    confidence += ternary(stackSize <= 2, 0.1)
    confidence += ternary(stackSize <= 3, 0.1)
    confidence += ternary(stackSize <= 6, -0.05)
    confidence += ternary(stackSize <= 8, -0.1)
    confidence += ternary(stackSize <= 10, -0.1)
    confidence += ternary(stackSize <= 12, -0.1)
    # multiplier += this.AdjustPriceBasedOn(target, new Func<NinjaItem, bool>((NinjaItem s) => s.HasAspect("LargeRandomPoolAspect")), 0.1f);
    # multiplier += this.AdjustPriceBasedOn(target, new Func<NinjaItem, bool>((NinjaItem s) => s.HasAspect("CurrencyTypeAspect")), 0.1f);

    confidence = float(
        decimal.Decimal(confidence).quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )
    )
    return confidence


# 3.35 ms ± 20.8 µs per loop group size: 5 entries
def evaluate_bases(data: pd.DataFrame) -> float:
    baseType = data.loc[:, "baseType"].iat[0]  # 54 µs ± 1.8 µs per loop

    confidence = 1.0

    totalQuant = data["count"].sum()  # 134 µs ± 3.9 µs per loop
    minPrice = data["chaosValue"].min()  # 119 µs ± 5.1 µs per loop
    maxPrice = data["chaosValue"].max()  # 115 µs ± 1.46 µs per loop
    highestLevelPrice = data.sort_values(by="levelRequired", ascending=False)[
        "chaosValue"  # 1.47 ms ± 43.3 µs per loop
    ].iat[0]
    averagePrice = (
        data["chaosValue"] * data["count"]
    ).sum() / totalQuant  # 292 µs ± 9.04 µs per loop

    progression = (
        data.sort_values(by="levelRequired")["chaosValue"].diff().sum()
    )  # 1.74 ms ± 36.1 µs per loop

    # correct pricepeak
    confidence += ternary(highestLevelPrice < maxPrice, -0.2, 0.1)

    # min price relevant
    confidence += ternary(minPrice <= averagePriceMinimum, -0.15, 0.1)

    # count rules
    confidence += ternary(totalQuant <= 2, -0.5, 0)
    confidence += ternary(totalQuant <= 4, -0.3, 0)
    confidence += ternary(totalQuant <= 8, -0.1, 0.05)
    confidence += ternary(totalQuant <= 16, -0.05, 0.05)

    # progression rules
    confidence += ternary(progression <= averagePriceMinimum, 0, 0.05)
    confidence += ternary(progression <= 0, -0.1, 0.05)
    confidence += ternary(progression <= -5, -0.1, 0)
    confidence += ternary(progression <= -20, -0.1, 0)

    # outlier rules
    confidence += ternary(minPrice < averagePriceMinimum and maxPrice > 25, -0.1, 0)
    confidence += ternary(maxPrice >= unhealthyPriceRange, -0.1, 0)
    confidence += ternary(maxPrice / minPrice > 100, -0.1, 0)
    confidence += ternary(maxPrice / minPrice > 75, -0.1, 0)
    confidence += ternary(maxPrice / minPrice > 50, -0.1, 0)
    confidence += ternary(maxPrice / minPrice > 25, -0.1, 0)

    # item info based rules
    bt_ref = bt[bt["BaseType"].isin([baseType])]  # 555 µs ± 1.45 µs per loop
    if len(bt_ref) > 0:
        itemClass, dropLevel = bt_ref.loc[:, ["Class", "DropLevel"]].values.tolist()[
            0
        ]  # 855 µs ± 2.43 µs per loop
        if itemClass.lower() not in ns_drop_level_ignored_classes and dropLevel != 0:
            confidence += ternary(dropLevel < 70, 0, 0.05)
            confidence += ternary(dropLevel < 60, -0.05, 0.05)
            confidence += ternary(dropLevel < 50, -0.05, 0)
            confidence += ternary(dropLevel < 40, -0.1, 0)
            confidence += ternary(dropLevel < 30, -0.1, 0)
            confidence += ternary(dropLevel < 20, -0.15, 0)
            confidence += ternary(dropLevel < 10, -0.2, 0)

    confidence = float(
        decimal.Decimal(confidence).quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
        )  # 1.92 µs ± 2.67 ns per loop
    )
    return confidence
    # print(f'{baseType:<30}|{variant:^10}|{highestLevelPrice:^10}|{progression:^20}|{confidence:^10}')
