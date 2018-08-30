#! python3.6
# -- CONFIG --

filter_file_name = r'StartingExfilterIncursion.filter'

UniqueExCategory = '%TB-Uniques-Exception'
#                           Category Name,              Min Tier for MultiBase

# UniqueMultiBaseCategory = [['%TB-Uniques-T2-MultiBase', 3, list()]]
# UniqueCategories = sorted([
#     # Category Name , Min Price (Chaos)
#     ['%TB-Uniques-T1', 25, list()],
#     ['%TB-Uniques-T2', 8, list()],
#     ['%TB-Uniques-T3', 1, list()],
#     ['%TB-Uniques-T4', 0, list()],
# ], key=lambda UniqueCategory: UniqueCategory[1], reverse=True)

UniqueMultiBaseCategory = [['%TB-Uniques-T2-MultiBase', 2, list()]]
UniqueCategories = sorted([
    # Category Name , Min Price (Chaos)
    ['%TB-Uniques-T1', 15, list()],
    ['%TB-Uniques-T2', 5, list()],
    ['%TB-Uniques-T3', 3, list()],
    ['%TB-Uniques-T4', 0, list()],
], key=lambda UniqueCategory: UniqueCategory[1], reverse=True)

DivExCategory = '%TB-Divination-Exception'
DivCategories = sorted([
    # Category Name , Min Price (Chaos)
    ['%TB-Divination-T1', 15, list()],
    ['%TB-Divination-T2', 5, list()],
    ['%TB-Divination-T3', 2, list()],
    ['%TB-Divination-T4', 0, list()],
], key=lambda DivCategory: DivCategory[1], reverse=True)

# Armed = Download + Write
Armed_Mode = True

LeagueName = r"Incursion"

# -- END CONFIG --

def GetFilterFileName ():
    return filter_file_name

def GetUniqueExCategory ():
    return UniqueExCategory

def GetUniqueMultiBaseCategory ():
    return UniqueMultiBaseCategory

def GetUniqueCategories ():
    return UniqueCategories

def GetDivExCategory ():
    return DivExCategory

def GetDivCategories ():
    return DivCategories

def GetArmedMode ():
    return Armed_Mode

def GetLeagueName ():
    return LeagueName