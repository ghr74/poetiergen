#! python3.6
import os
import regex
import json
import requests
import poetiergen_calcs as calcs
import poetiergen_constants as constants
import poepy_core as core
import itertools

def FilteryThingy(filter_file_name, league_name, armed_mode=False, 
uniques_exception_category=None, divination_exception_category=None, 
uniques_category_settings=None, divination_category_settings=None, bases_section_settings=None):
    # -- VARS --
    core.SetURLs(league_name)
    path_to_filter = os.path.join(os.path.expanduser(r"~\Documents\My Games\Path of Exile"), filter_file_name)
    # path_to_filter = filter_file_name
    download_mode = False
    write_mode = True
    download_mode = download_mode or armed_mode
    write_mode = write_mode or armed_mode
    # -- EXCEPTIONS --
    unique_exceptions = core.scantier(path_to_filter, uniques_exception_category) if type(uniques_exception_category) == str else []
    divination_exceptions = core.scantier(path_to_filter, divination_exception_category) if type(divination_exception_category) == str else []
    # -- PROCESS --
    # -- Get data from poe.ninja
    unique_data, div_data, bases_data = core.GetAllJsonData(download_mode)
    # -- Calculate Unique BaseType lists
    unique_garbage, unique_ex, unique_mixed = calcs.calc_uniques(uniques_category_settings[3], unique_data, unique_exceptions)
    # -- Calculate Divination BaseType lists
    div_garbage, div_ex = calcs.calc_div_cards(divination_category_settings[2], div_data, divination_exceptions)
    # -- Calculate Bases dataframes
    bases_chaos, bases_ex = calcs.calc_item_bases(bases_section_settings[1], bases_data)
    # -- Generate Bases section string
    bases_section_string = core.GenerateSectionBlock((bases_ex, bases_chaos), bases_section_settings)
    # -- Replace / debug output
    categories = {
            divination_category_settings[0]:div_ex,
            divination_category_settings[1]:div_garbage, 
            uniques_category_settings[0]:unique_ex,
            uniques_category_settings[1]:unique_mixed,
            uniques_category_settings[2]:unique_garbage, 
            }
    bases_categories = {
        'Bases Chaos':len(bases_chaos),
        'Bases Ex':len(bases_ex),
    }
    if write_mode:
        print("Starting replace...")
        for k, v in categories.items():
            print(f'{k}  - {len(v)}  Entries')
            core.ReplaceCategory(path_to_filter, k, v)
        for k, v in bases_categories.items():
            print(f'{k}  - {v}  Entries')
        core.ReplaceSection(path_to_filter, bases_section_settings[0], bases_section_string)
        print("Replace complete.")
    else:
        print("Debug output...")
        for k, v in categories.items():
            print(f'{k}  - {len(v)}  Entries')
        for k, v in bases_categories.items():
            print(f'{k}  - {v}  Entries')
        print(divination_exceptions)
        print(unique_exceptions)
        # print(bases_section_string)

def GenerateDivinationTiers(league_name, download_mode, min_price, divination_exception_categories=[]):
    # core.SetURLs(league_name)
    divination_exceptions = []
    for cat in divination_exception_categories:
        divination_exceptions.extend(cat.geta('BaseType'))
    print(divination_exceptions)
    div_data = core.GetDivinationData(league_name, download_mode)
    div_garbage, div_ex = calcs.calc_div_cards(min_price, div_data, divination_exceptions)
    return div_garbage, div_ex

def GenerateUniqueTiers(league_name, download_mode, min_price, uniques_exception_categories=[]):
    # core.SetURLs(league_name)
    unique_exceptions = []
    for cat in uniques_exception_categories:
        unique_exceptions.extend(cat.geta('BaseType'))
    print(unique_exceptions)
    unique_data = core.GetUniquesData(league_name, download_mode)
    unique_garbage, unique_ex, unique_mixed = calcs.calc_uniques(min_price, unique_data, unique_exceptions)
    return unique_garbage, unique_ex, unique_mixed

def GenerateShaperElderSection(league_name, section, min_price, style_chaos, style_ex, download_mode=False):
    from poefilter import Category
    # core.SetURLs(league_name)
    bases_data = core.GetBasesData(league_name, download_mode)
    bases_chaos, bases_ex = calcs.calc_item_bases(min_price, bases_data)
    for tier, baseDataframe in enumerate((bases_ex, bases_chaos), start=1):
        for (variant, ilvl), group in baseDataframe.groupby(['variant', 'levelRequired']):
            base_type_list = group['baseType'].values.tolist()
            section.append(Category(f'Bases-{variant}-{ilvl}-T{tier}',
                ShaperItem = True if 'Shaper' in variant else None,
                ElderItem = True if 'Elder' in variant else None,
                ItemLevel = ((">=" if ilvl==86 else "=") + f' {ilvl}') if ilvl > 0 else None,
                Rarity = "<= Rare",
                BaseType = base_type_list,
                Style = style_ex if tier == 1 else style_chaos,
            ))
    return section