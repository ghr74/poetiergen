#! python3.6

import json
import regex
from timeit import default_timer as timer
import time
import requests
import poetiergen_constants as constants
from textwrap import dedent, indent

category_regex = r'[\s\w]*BaseType\s\K.*'
# base_regex = r'(?:# %TB-Bases){1}(?m)(?:[\s]*Show # %TB-Bases[\s\S]*?(?:BaseType.*))*'

url_uniques = []
url_div = ""
url_bases = ""

def SetURLs(LeagueName):
    global url_uniques
    global url_div
    global url_bases
    url_uniques = [
        # Armour URL
        "http://poe.ninja/api/Data/GetUniqueArmourOverview?league=" + LeagueName + "&date=" + time.strftime("%Y-%m-%d"),
        # Weapon URL
        "http://poe.ninja/api/Data/GetUniqueWeaponOverview?league=" + LeagueName + "&date=" + time.strftime("%Y-%m-%d"),
        # Flask URL
        "http://poe.ninja/api/Data/GetUniqueFlaskOverview?league=" + LeagueName + "&date=" + time.strftime("%Y-%m-%d"),
        # Accessory URL
        "http://poe.ninja/api/Data/GetUniqueAccessoryOverview?league=" + LeagueName + "&date=" + time.strftime("%Y-%m-%d"),
        # Jewel URL
        "http://poe.ninja/api/Data/GetUniqueJewelOverview?league=" + LeagueName + "&date=" + time.strftime("%Y-%m-%d"),
        # Unique Map URL
        "http://poe.ninja/api/Data/GetUniqueMapOverview?league=" + LeagueName + "&date=" + time.strftime("%Y-%m-%d"),
    ]
    # Div Card URL
    url_div = "http://poe.ninja/api/Data/GetDivinationCardsOverview?league=" + LeagueName + "&date=" + time.strftime("%Y-%m-%d")
    url_bases = "http://poe.ninja/api/Data/GetBaseTypeOverview?league=" + LeagueName + "&date=" + time.strftime("%Y-%m-%d")

def FileToJson(filepath):
    file_data = ""
    with open(filepath, 'r') as json_file:
        file_data = json_file.read()
    return json.loads(file_data).get('lines')

def DownloadJson(url):
    print("Downloading from: ", url)
    r = requests.get(url)
    r.encoding = 'ISO-8859-1'
    print("Download done, loading dataset...")
    return r.json().get('lines')

def GetDivinationData(download=False):
    div_data = {}
    if download:
        print("Starting Download...")
        div_data = DownloadJson(url_div)
        print("Download / Load complete.")
    else:
        div_data = FileToJson(constants.json_div_filepath)
    return div_data

def GetBasesData(download=False):
    bases_data = {}
    if download:
        print(f"Starting Download...")
        bases = DownloadJson(url_bases)
        print("Download / Load complete.")
    else:
        bases = FileToJson(constants.json_bases_filepath)
    return bases

def GetUniquesData(download=False):
    uniques_data = []
    if download:
        print("Starting Download...")
        for url in url_uniques:
            uniques_data.append(DownloadJson(url))
        print("Download / Load complete.")
    else:
        for path in constants.json_unique_filepaths:
            uniques_data.append(FileToJson(path))
    return uniques_data

def GetAllJsonData(download=False):
    uniques_data = []
    div_data, bases_data = {}, {}
    if download:
        print("Starting Download...")
        for url in url_uniques:
            uniques_data.append(DownloadJson(url))
        div_data = DownloadJson(url_div)
        bases_data = DownloadJson(url_bases)
        print("Download / Load complete.")
    else:
        for path in constants.json_unique_filepaths:
            uniques_data.append(FileToJson(path))

        div_data = FileToJson(constants.json_div_filepath)
        bases_data = FileToJson(constants.json_bases_filepath)
    return uniques_data, div_data, bases_data

def GenerateCategoryBlock(meta_category, effect_config, base_type_string, tier=0, ilvl=0, variant=""):
    variant_string = "ShaperItem True\n" if 'Shaper' in variant else "ElderItem True\n" if 'Elder' in variant else ""
    ilvl_string = "ItemLevel " + (">=" if ilvl==86 else "=") + f' {ilvl}\n' if ilvl > 0 else ""
    effect_string = dedent(effect_config)
    output_string = f'Show # {meta_category}-{variant}-{ilvl}-T{tier}\n' + indent(    
            f'{variant_string}'
            f'{ilvl_string}'
            'Rarity <= Rare\n'
            f'BaseType {base_type_string}\n'
            f'{effect_string}\n\n'
            , '\t')
    return output_string

def GenerateSectionBlock(baseDataframes, sectionSettings):
    from textwrap import indent
    if len(baseDataframes) == len(sectionSettings[2]):
        bases_output_string = f'# {sectionSettings[0]}\n\n'
        for tier, baseDataframe in enumerate(baseDataframes):
            output_string = ""
            for (n1, n2), group in baseDataframe.groupby(['variant', 'levelRequired']):
                base_type_string = BaseTypeString(group["baseType"].values.tolist())
                subcategory_string = GenerateCategoryBlock(sectionSettings[0], sectionSettings[2][tier], base_type_string, tier + 1, n2, n1)
                output_string += indent(subcategory_string, '\t')
            bases_output_string += output_string
        return bases_output_string
    else:
        return "GIGAERROR LUL FIX YOUR SETTINGS"

def scantier(filterpath, search):
    with open(filterpath, 'r') as filter_file:
        file_string = filter_file.read()
        res = regex.findall(search + category_regex, file_string)
    if res:
        return ' '.join(res).split('"',1)[1].rsplit('"',1)[0].replace('" ','').split('"')
    else:
        return []

def replace(source_file_path, pattern, substring):
    file_string = ""
    with open(source_file_path, 'r') as source_file:
        file_string = source_file.read()
    file_string = regex.sub(pattern, substring, file_string)
    with open(source_file_path, 'w') as target_file:
        target_file.write(file_string)  

def write_to_file(file_path, write_string):
    with open(file_path, 'w') as target_file:
        target_file.write(str(write_string))  

def BaseTypeString(base_types):
    return ' '.join(f'"{base_type}"' for base_type in base_types).strip()

def ReplaceCategory(path_to_filter, category, sublist):
    replace(path_to_filter, category + category_regex, BaseTypeString(sublist))

def ReplaceSection(path_to_filter, section, section_string):
    replace(path_to_filter, fr'(?:# {section}){{1}}(?m)(?:[\s]*Show # {section}[\s\S]*?(?:BaseType.*))*', section_string)

def quicktime(fun):
    start = timer()
    fun()
    end = timer()
    print(end-start)

def ternary(condition, true_value, false_value = 0):
    return (true_value if condition else false_value)

def InvestigatedItem(item):
    inv_set = {
        # ('Marble Amulet', 86, 'Normal'),
        # ('Prismatic Ring', 82, 'Shaper'),
        # ('Latticed Ringmail', 84, 'Elder'),
        # ('Leatherscale Boots', 82, 'Elder'),
        # ('Bone Helmet', 86, 'Elder'),
        # ('Opal Ring', 85, 'Elder'),
        # ('Eternal Burgonet', 84, 'Elder')
        # ('Titanium Spirit Shield', 86, 'Shaper')
        # ('Driftwood Sceptre', 82, 'Normal'),
        # ('Highland Blade', 82, 'Normal')

        # ('Marble Amulet', 'Normal'),
        # ('Prismatic Ring', 'Shaper'),
        # ('Latticed Ringmail', 'Elder'),
        # ('Leatherscale Boots', 'Elder'),
        # ('Bone Helmet', 'Elder'),
        # ('Opal Ring', 'Elder'),
        # ('Eternal Burgonet', 'Elder'),
        # ('Titanium Spirit Shield', 'Shaper'),
        # ('Driftwood Sceptre', 'Normal'),
        # ('Highland Blade', 'Normal')
    }
    return item in inv_set