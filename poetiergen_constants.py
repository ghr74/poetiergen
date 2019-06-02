import os

category_regex = r"[\s\w]*BaseType\s\K.*"
base_regex = r"(?:# %TB-Bases){1}(?m)(?:[\s]*Show # %TB-Bases[\s\S]*?(?:BaseType.*))*"

json_unique_filepaths = [
    "test_data\GetUniqueArmourOverview.json",
    "test_data\GetUniqueWeaponOverview.json",
    "test_data\GetUniqueFlaskOverview.json",
    "test_data\GetUniqueAccessoryOverview.json",
    "test_data\GetUniqueJewelOverview.json",
    "test_data\GetUniqueMapOverview.json",
]
json_div_filepath = "test_data\GetDivinationCardsOverview.json"
json_bases_filepath = "test_data\GetBaseTypeOverview.json"

bases_useless_columns = [
    "artFilename",
    "corrupted",
    "explicitModifiers",
    "flavourText",
    "gemLevel",
    "gemQuality",
    "icon",
    "implicitModifiers",
    "links",
    "mapTier",
    "prophecyText",
    "stackSize",
    "name",
    "itemClass",
    "detailsId",
]

divs_useless_columns = [
    "artFilename",
    "links",
    "mapTier",
    "explicitModifiers",
    "itemClass",
    "itemType",
    "levelRequired",
    "prophecyText",
    "variant",
    "baseType",
    "corrupted",
    "flavourText",
    "gemLevel",
    "gemQuality",
    "implicitModifiers",
    "icon",
]

uniques_useless_columns = [
    "artFilename",
    "corrupted",
    "prophecyText",
    "variant",
    "mapTier",
    "explicitModifiers",
    "implicitModifiers",
    "itemClass",
    "flavourText",
    "gemLevel",
    "gemQuality",
    "icon",
    "levelRequired",
    "stackSize",
]

NotDroppedList = [
    # Award Only
    "Emperor's Mastery",
    # Vendor Recipe Only
    "The Goddess Unleashed",
    "The Goddess Scorned",
    "The Anima Stone",
    "The Retch",
    "Loreweave",
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
    # Special
    "Tabula Rasa",
]
