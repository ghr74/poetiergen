#! python3.6
import requests
import os
import regex
import time
import json
from collections import defaultdict
import itertools
import poetiergen_config

# -- CONFIG --

filter_file_name = poetiergen_config.GetFilterFileName()

UniqueExCategory = poetiergen_config.GetUniqueExCategory()

UniqueMultiBaseCategory = poetiergen_config.GetUniqueMultiBaseCategory()
UniqueCategories = poetiergen_config.GetUniqueCategories()

DivExCategory = poetiergen_config.GetDivExCategory()
DivCategories = poetiergen_config.GetDivCategories()

Armed_Mode = poetiergen_config.GetArmedMode()

LeagueName = poetiergen_config.GetLeagueName()

# -- END CONFIG --

download_mode = False

write_mode = False

dbg_print = True

download_mode = download_mode or Armed_Mode
write_mode = write_mode or Armed_Mode

NotDroppedList = [
    # Award Only
        "Emperor's Mastery",
    # Vendor Recipe Only
        "The Goddess Unleashed",
        "The Goddess Scorned",
        "The Anima Stone",
        "The Retch",
        "Loreweave"
    # Vaal Only
        "Blood of Corruption",
    # Pieces Only
        "The Flow Untethered",
        "The Tempest's Binding",
        "The Rippling Thoughts",
    # Div Only / League Only
    #   Incursion
        "Apep's Slumber",
        "Apep's Supremacy",
        "Architect's Hand",
        "Coward's Chains",
        "Coward's Legacy",
        "Dance of the Offered",
        "Fate of the Vaal",
        "Mask of the Spirit Drinker",
        "Mask of the Stitched Demon",
        "Omeyocan",
        "Sacrificial Heart",
        "Shadowstitch",
        "Slavedriver's Hand",
        "Soul Catcher",
        "Soul Ripper",
        "Story of the Vaal",
        "String of Servitude",
        "Tempered Flesh",
        "Tempered Mind",
        "Tempered Spirit",
        "Transcendent Flesh",
        "Transcendent Mind",
        "Transcendent Spirit",
        "Zerphi's Heart",
    #   Talisman
        "Blightwell",
        "Eyes of the Greatwolf",
        "Faminebind",
        "Feastbind",
        "Rigwald's Command",
        "Rigwald's Crest",
        "Rigwald's Curse",
        "Rigwald's Quills",
        "Rigwald's Savagery",
    #   Nemesis
        "Headhunter",
        "Berek's Grip",
        "Berek's Pass",
        "Berek's Respite",
        "Blood of the Karui",
        "Lavianga's Spirit",
    #   Perandus
        "Seven-League Step",
        "Trypanon",
        "Umbilicus Immortalis",
        "Varunastra",
        "Zerphi's Last Breath",
    #   Tempest
        "Crown of the Pale King",
        "Jorrhast's Blacksteel",
        "Trolltimber Spire",
        "Ylfeban's Trickery",
    #   Torment
        "Brutus' Lead Sprinkler",
        "Scold's Bridle",
        "The Rat Cage",
    #   Anarchy
        "Daresso's Salute",
        "Gifts from Above",
        "Shavronne's Revelation",
        "Voll's Devotion",
    #   Onslaught
        "Death Rush",
        "Victario's Acuity",
    #   Beyond
        # "Edge of Madness",
        # "The Dark Seer",
        # "The Harvest",
    #   Ambush / Invasion
        "Vaal Caress",
        "Voideye",
    #   Breach, Blessing Only
        "Presence of Chayula",
        "Skin of the Lords",
        "The Blue Nightmare",
        "The Green Nightmare",
        "The Red Nightmare",
        "United in Dream",
        "Choir of the Storm",
        "Esh's Visage",
        "Hand of Wisdom and Action",
        "The Pandemonius",
        "The Perfect Form",
        "Tulfall",
        "The Red Trail",
        "The Surrender",
        "Uul-Netol's Embrace",
        "The Formless Inferno",
        "Xoph's Blood",
        "Xoph's Nurture",
    #   Bestiary
        "Craiceann's Carapace",
        "Craiceann's Chitin",
        "Craiceann's Pincers",
        "Craiceann's Tracks",
        "Farrul's Bite",
        "Farrul's Chase",
        "Farrul's Fur",
        "Farrul's Pounce",
        "Fenumus' Shroud",
        "Fenumus' Spinnerets",
        "Fenumus' Toxins",
        "Fenumus' Weave",
        "Saqawal's Flock",
        "Saqawal's Nest",
        "Saqawal's Talons",
        "Saqawal's Winds",
    # Boss-Only
    #   Normie-Atziri
        "Atziri's Promise",
        "Atziri's Step",
        "Doryani's Catalyst",
        "Doryani's Invitation",
    #   Uber-Atziri
        "Atziri's Disfavour",
        "Atziri's Acuity",
        "The Vertex",
        "Atziri's Splendour",
    #   Shaper
        "Dying Sun",
        "Shaper's Touch",
        "Starforge",
        "Voidwalker",
    #   T1 Elder
        "Blasphemer's Grasp",
        "Cyclopean Coil",
    #   T6 Elder
        "Nebuloch",
        "Shimmeron",
        "Hopeshredder",
        "Watcher's Eye",
    #   T11 Elder
        "Impresence",
    #   Uber Elder
        "Disintegrator",
        "Indigon",
        "Voidfletcher",
        "Mark of the Elder",
        "Mark of the Shaper",
        "Voidforge",
    #   Abyssal Liches
        "Darkness Enthroned",
        "Tombfist",
        "Lightpoacher",
        "Bubonic Trail",
        "Shroud of the Lightless",
    # Fated
        "Amplification Rod",
        "Asenath's Chant",
        "Atziri's Reflection",
        "Cameria's Avarice",
        "Corona Solaris",
        "Cragfall",
        "Crystal Vault",
        "Death's Opus",
        "Deidbellow",
        "Doedre's Malevolence",
        "Doomfletch's Prism",
        "Dreadbeak",
        "Dreadsurge",
        "Duskblight",
        "Ezomyte Hold",
        "Fox's Fortune",
        "Frostferno",
        "Geofri's Devotion",
        "Greedtrap",
        "Hrimburn",
        "Hrimnor's Dirge",
        "Hyrri's Demise",
        "Kaltensoul",
        "Kaom's Way",
        "Karui Charge",
        "Malachai's Awakening",
        "Martyr's Crown",
        "Mirebough",
        "Ngamahu Tiki",
        "Panquetzaliztli",
        "Queen's Escape",
        "Realm Ender",
        "Sanguine Gambol",
        "Shavronne's Gambit",
        "Silverbough",
        "Sunspite",
        "The Cauteriser",
        "The Dancing Duo",
        "The Effigon",
        "The Gryphon",
        "The Nomad",
        "The Oak",
        "The Signal Fire",
        "The Stormwall",
        "The Tactician",
        "The Tempest",
        "Thirst for Horrors",
        "Timetwist",
        "Voidheart",
        "Wall of Brambles",
        "Wildwrap",
        "Windshriek",
        "Winterweave",
]

UniqueEx = []
DivEx = []

path_to_filter = os.path.join(os.path.expanduser(r"~\Documents\My Games\Path of Exile"), filter_file_name)
category_regex = r'[\s\w]*BaseType\s\K.*'
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

def BaseTypeString(category):
    return ''.join('"'+x+'" ' for x in category).strip()

def ReplaceCategory(category, sublist):
    replace(path_to_filter, category + category_regex, BaseTypeString(sublist))

def ReplaceCategory2(full_category):
    replace(path_to_filter, full_category[0] + category_regex, BaseTypeString(full_category[2]))

DivEx = scantier(path_to_filter, DivExCategory)
UniqueEx = scantier(path_to_filter, UniqueExCategory)

def LoadUniqueData(data):
    global UniqueEx
    global UniqueMultiBaseCategory
    global NotDroppedList
    global UniqueCategories

    bt_dict = defaultdict(list)

    for item in data:

        item_name = item.get('name')
        item_bt = item.get('baseType')
        item_price = item.get('chaosValue')
        item_links = item.get('links')

        if item_links < 5 and item_bt not in UniqueEx and "Piece" not in item_bt and item_name not in NotDroppedList and "Tabula Rasa" not in item_name :
            for idx, cat in enumerate(UniqueCategories, start=1):
                if item_price >= cat[1]:
                    bt_dict[item_bt].append(idx)
                    break


    for bt in bt_dict:

        Votes = bt_dict[bt]
        VotesAboveCutoff = sum(Vote <= UniqueMultiBaseCategory[0][1] for Vote in Votes)
        VotesBelowCutoff = len(Votes) - VotesAboveCutoff

        if VotesAboveCutoff > 0 and VotesBelowCutoff > 0:
            UniqueMultiBaseCategory[0][2].append(bt)
        else:
            UniqueCategories[sorted(Votes, reverse=True)[0] - 1][2].append(bt)

def LoadDivinationData(data):
    global DivEx
    global DivCategories

    for item in data:

        item_name = item.get('name')
        item_price = item.get('chaosValue')

        if item_name not in DivEx :
            for idx, cat in enumerate(DivCategories):
                if item_price >= cat[1]:
                    DivCategories[idx][2].append(item_name)
                    break


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
]
# Div Card URL
url_div = "http://poe.ninja/api/Data/GetDivinationCardsOverview?league=" + LeagueName + "&date=" + time.strftime("%Y-%m-%d")

json_unique_filepaths = [
    os.path.expanduser(r'~\Dropbox\programming\poetiergen\GetUniqueArmourOverview.json'),
    os.path.expanduser(r'~\Dropbox\programming\poetiergen\GetUniqueWeaponOverview.json'),
    os.path.expanduser(r'~\Dropbox\programming\poetiergen\GetUniqueFlaskOverview.json'),
    os.path.expanduser(r'~\Dropbox\programming\poetiergen\GetUniqueAccessoryOverview.json'),
    os.path.expanduser(r'~\Dropbox\programming\poetiergen\GetUniqueJewelOverview.json')
]
json_div_filepath = os.path.expanduser(r'~\Dropbox\programming\poetiergen\GetDivinationCardsOverview.json')

def FileToJson(filepath):
    file_data = ""
    with open(filepath, 'r') as json_file:
        file_data = json_file.read()
    return json.loads(file_data).get('lines')

if download_mode:
    print("Starting Download...")
    for url in url_uniques:
        print("Downloading from: ", url)
        r = requests.get(url)
        print("Download done, loading dataset...")
        r.encoding = 'ISO-8859-1'
        LoadUniqueData(r.json().get('lines'))
        print("Dataset loaded.")
    print("Downloading from: ", url_div)
    r = requests.get(url_div)
    print("Download done, loading dataset...")
    r.encoding = 'ISO-8859-1'
    LoadDivinationData(r.json().get('lines'))
    print("Dataset loaded.")
    print("Download / Load complete.")

else:

    for path in json_unique_filepaths:
        LoadUniqueData(FileToJson(path))

    LoadDivinationData(FileToJson(json_div_filepath))

if write_mode:
    print("Starting replace...")
    for cat in itertools.chain(UniqueCategories, DivCategories, UniqueMultiBaseCategory):
        print(cat[0], " - ", len(cat[2]), " Entries")
        ReplaceCategory2 (cat)
    print("Replace complete.")

else:
    if dbg_print:
        for cat in itertools.chain(UniqueCategories, DivCategories, UniqueMultiBaseCategory):
            print(cat[0], " - ", len(cat[2]), " Entries")
        print(DivEx)
        print(UniqueEx)
        print(path_to_filter)
        for url in url_uniques:
            print(url)
        print(url_div)
        for cat in itertools.chain(UniqueCategories, UniqueMultiBaseCategory):
            if "War Hammer" in cat[2]:
                print(cat[0])
    else:
        print(DivEx)