import exfilter_styles as styles
import poefilter as pf
from poepy_core import write_to_file
import poetiergen2

league_name = r'Synthesis'
download_mode = False

exfilter = pf.FilterObj("version for Synthesis League - blackytemp version based on CuteDog_ version - not recommended for anyone")
exfilter.append(pf.Section("QUEST & EXTRA",
        pf.Category("QUEST & EXTRA",
            Class = ["Quest Items", "Labyrinth Item", "Labyrinth Trinket", "Labyrinth Map Item", "Incursion Item", "Pantheon Soul", "Misc Map Items", "Piece"],
            Style = styles.STYLE_QUEST_EXTRA_SPECIAL,
        ),
    )
)
exfilter.append(pf.Section("Explicit Mod Filtering",
        pf.Category("Specific Mods",
            Identified = True,
            HasExplicitMod = ["It That Fled's Veiled", "Tacati's", "Citaqualotl's", "Matatl's", "Topotante's", "Xopec's", "Guatelitzi's", "of Tacati", "of Citaqualotl", "of Matatl", "of Puhuarte", "of Guatelitzi", "Brinerot", "Mutewind", "Redblade", "Betrayer's", "Deceiver's", "Turncoat's", "Subterranean", "of the Underground", "of Weaponcraft", "of Spellcraft", "of Crafting", "of Farrul", "of Craiceann", "of Fenumus", "of Saqawal"],
            Style = styles.STYLE_EXPLICIT_MOD,
        ),
        pf.Category("Enchanted Items",
            AnyEnchantment = True,
            Style = styles.STYLE_EXPLICIT_MOD,
        ),
        pf.Category("Good Fractured Items",
            FracturedItem = True,
            ItemLevel = ">= 82",
            Style = styles.STYLE_EXPLICIT_MOD,
        ),
        pf.Category("Synthesised Items",
            SynthesisedItem = True,
            Style = styles.STYLE_EXPLICIT_MOD,
        )
    )
)
exfilter.append(pf.Section("Jeweller's Recipe & High Linked Sockets",
    pf.Category("Divine Orb Vendor Recipe",
        LinkedSockets = ">= 6",
        Rarity = "<= Rare",
        Style = styles.STYLE_DIVINE_RECIPE
    ),
    pf.Category("Tabula Rasa Exception",
        SocketGroup = "WWWWWW",
        BaseType = "Simple Robe",
        Rarity = "Unique",
        Style = styles.STYLE_DIVINE_RECIPE
    ),
    pf.Category("Jeweller's Orb Vendor Recipe",
        Sockets = ">= 6",
        Style = styles.STYLE_JEWELLER_RECIPE
    )
))
exfilter.append(pf.Section("Uniques",
    pf.Category("5-Link uniques",
        LinkedSockets = 5,
        Rarity = "Unique",
        Style = styles.STYLE_UNIQUES_CHAOS,
    ),
    pf.Category("Unique Rings",
        Rarity = "Unique",
        Class = "Rings",
        Style = styles.STYLE_UNIQUES_CHAOS,
    ),
    pf.Category("Uniques T1",
        Rarity = "Unique",
        Style = styles.STYLE_UNIQUES_EXALT,
    ),
    pf.Category("Uniques Garbage",
        Rarity = "Unique",
        Style = styles.STYLE_UNIQUES_GARBAGE,
    ),
    pf.Category("Uniques Other",
        Rarity = "Unique",
        Style = styles.STYLE_UNIQUES_CHAOS,
    )
))
exfilter.append(pf.Section("Divination Cards",
    pf.Category("Hidden Exceptions",
        show = pf.HIDE,
        BaseType = ["The Wolf's Shadow", "Her Mask", "The Eye of the Dragon", "The Master Artisan"],
        Class = "Divination Card",
    ),
    pf.Category("Shown Exceptions",
        BaseType = ["Humility", "Beauty Through Death", "The Dragon's Heart", "The Encroaching Darkness", "Lysah's Respite", "The Survivalist", "Loyalty"],
        Class = "Divination Card",
        Style = styles.STYLE_DIVINATION_EXCEPTION,
    ),
    pf.Category("Divination T1",
        Class = "Divination Card",
        Style = styles.STYLE_DIVINATION_EXALT,
    ),
    pf.Category("Divination Garbage",
        show = pf.HIDE,
        Class = "Divination Card",
    ),
    pf.Category("Other Divination Cards",
        Class = "Divination Card",
        Style = styles.STYLE_DIVINATION_CHAOS,
    )
))
exfilter.append(pf.Section("Currency",
    pf.Category("Currency Exalt Tier",
        Class = ["Stackable Currency", "Delve Socketable Currency"],
        BaseType = ["Sanctified Fossil", "Tangled Fossil", "Glyphic Fossil", "Hollow Fossil", "Faceted Fossil", "Bloodstained Fossil", "Fractured Fossil", "Divine Orb", "Orb of Annulment", "Exalted Orb", "Eternal Orb", "Mirror of Kalandra", "Mirror Shard", "Prime Alchemical Resonator", "Prime Chaotic Resonator", "Exalted Shard"],
        Style = styles.STYLE_CURRENCY_EXALT,
    ),
    pf.Category("Hide Shitty Fossils",
        show = pf.HIDE,
        Class = "Stackable Currency",
        BaseType = ["Frigid Fossil", "Scorched Fossil", "Aberrant Fossil", "Jagged Fossil", "Bound Fossil", "Corroded Fossil", "Lucent Fossil", "Serrated Fossil"],
    ),
    pf.Category("Currency Chaos Tier",
        Class = ["Stackable Currency", "Delve Socketable Currency"],
        BaseType = ["Regal Orb", "Orb of Regret", "Chaos Orb", "Gemcutter's Prism", "Orb of Fusing", "Orb of Scouring", "Orb of Alchemy", "Vaal Orb", "Cartographer's Chisel", "Cartographer's Sextant", "Annulment Shard", "Ancient Shard", "Harbinger's Shard", "Stacked Deck", "Orb of Binding", "Engineer's Orb", "Ancient Orb", "Orb of Horizons", "Harbinger's Orb", "Prophecy", "Fossil", "Potent Chaotic Resonator", "Powerful Chaotic Resonator"],
        Style = styles.STYLE_CURRENCY_CHAOS,
    ),
    pf.Category("Low Currency T1",
        Class = ["Stackable Currency", "Delve Socketable Currency"],
        BaseType = ["Glassblower's Bauble", "Perandus Coin", "Horizon Shard", "Engineer's Shard", "Blessed Orb", "Silver Coin", "Chaos Shard"],
        Style = styles.STYLE_CURRENCY_LOW,
    ),
    pf.Category("Low Currency T2",
        show = pf.HIDE,
        Class = ["Stackable Currency", "Delve Socketable Currency"],
        BaseType = ["Orb of Chance", "Chromatic Orb", "Orb of Alteration", "Jeweller's Orb"],
        Style = styles.STYLE_CURRENCY_LOW,
    ),
    pf.Category("Low Currency T3",
        show = pf.HIDE,
        BaseType = ["Blacksmith's Whetstone", "Portal Scroll"],
        Style = styles.STYLE_CURRENCY_GARBAGE,
    ),
    pf.Category("Low Currency T4",
        show = pf.HIDE,
        BaseType = ["Armourer's Scrap", "Scroll of Wisdom", "Orb of Transmutation", "Orb of Augmentation"],
        Style = styles.STYLE_CURRENCY_GARBAGE,
    ),
    pf.Category("Currency Stacks",
        Class = "Stackable Currency",
        BaseType = ["Perandus Coin", "Shard"],
        StackSize = ">= 5",
        Style = styles.STYLE_CURRENCY_STACKABLE,
    ),
    pf.Category("Splinter and Essence",
        Class = "Stackable Currency",
        BaseType = ["Splinter of", "Remnant of Corruption", "Screaming Essence of", "Shrieking Essence of", "Deafening Essence of", "Blessing of", "Vial of", "of Hysteria", "of Insanity", "of Horror", "of Delirium"],
        Style = styles.STYLE_CURRENCY_STACKABLE,
    ),
    pf.Category("Hide Currency Rest",
        show = pf.HIDE,
        Class = ["Stackable Currency", "Delve Socketable Currency"],
        BaseType = ["Essence", "Shard", "Resonator"],
    )
))
exfilter.append(pf.Section("Maps",
    pf.Category("Map Fragments",
        Class = "Map Fragments",
        Style = styles.STYLE_MAP_FRAGMENTS,
    ),
    pf.Category("Shaped Maps",
        ShapedMap = True,
        Class = "Map",
        Style = styles.STYLE_MAP_SHAPED,
    ),
    pf.Category("Elder Maps",
        ElderMap = True,
        Class = "Map",
        Style = styles.STYLE_MAP_ELDER,
    ),
    pf.Category("High Tier Maps",
        Class = "Map",
        MapTier = ">= 15",
        Style = styles.STYLE_MAP_RED,
    ),
    pf.Category("Low Tier Maps",
        show = pf.HIDE,
        Class = "Map",
        MapTier = "<= 11",
        Style = styles.STYLE_MAP_WHITE,
    ),
    pf.Category("Mid Tier Maps",
        Class = "Map",
        Style = styles.STYLE_MAP_YELLOW,
    )
))
exfilter.append(pf.Section("Skillgems",
    pf.Category("Gigagems",
        Class = "Gems",
        BaseType = ["Vaal Breach", "Empower", "Enlighten", "Item Quantity"],
        Style = styles.STYLE_SKILLGEM_HIGH,
    ),
    pf.Category("Lvl 20 Gems",
        Class = "Gems",
        GemLevel = ">= 20",
        Style = styles.STYLE_SKILLGEM_HIGH,
    ),
    pf.Category("High Quality Gems",
        Class = "Gems",
        Quality = ">= 15",
        Style = styles.STYLE_SKILLGEM_LOW,
    ),
    pf.Category("Hide Rest of Gems",
        show = pf.HIDE,
        Class = "Gems",
        Style = styles.STYLE_SKILLGEM_LOW,
    )
))
exfilter.append(pf.Section("Magic/Rare Exceptions",
    pf.Category("Rare T1 Bases U wanna see hehe",
        BaseType = ["Steel Ring", "Opal Ring", "Marble Amulet", "Talisman"],
        Style = styles.STYLE_BASES_MEDIOCRE,
    ),
    pf.Category("Big Abyssal Jewels",
        BaseType = ["Searching Eye Jewel", "Hypnotic Eye Jewel"],
        Class = "Abyss Jewel",
        ItemLevel = ">= 82",
        Style = styles.STYLE_BASES_MEDIOCRE,
    ),
    pf.Category("Rare Jewels",
        show = pf.DISABLE,
        Class = "Jewel",
        Rarity = "Rare",
        Style = styles.STYLE_BASES_SHITTY,
    ),
    pf.Category("Dump Tab Rings and Amulets",
        show = pf.DISABLE,
        ItemLevel = ">= 75",
        Class = ["Amulets", "Rings"],
        BaseType = ["Ruby Ring", "Sapphire Ring", "Topaz Ring", "Two-Stone Ring", "Diamond Ring"],
        Rarity = "Rare",
        Style = styles.STYLE_BASES_SHITTY,
    ),
    pf.Category("Stygian Visages",
        show = pf.DISABLE,
        BaseType = "Stygian Vise",
        ItemLevel = ">= 83",
        Style = styles.STYLE_BASES_SHITTY,
    )
))
exfilter.append(pf.Section("Shaper/Elder Items",
))
exfilter.append(pf.Section("Chromatic Recipe",
    pf.Category("Chromatic Recipe",
        Width = 1,
        Rarity = "<= Rare",
        SocketGroup = "RGB",
        Style = styles.STYLE_CHROMATIC_RECIPE,
    )
))
exfilter.append(pf.Section("Final Filter Management",
    pf.Category("Hide all <= Rare items",
        show = pf.HIDE,
        Rarity = "<= Rare",
        Class = ["Amulets", "Rings", "Claws", "Daggers", "Wands", "Swords", "Axes", "Maces", "Bows", "Staves", "Quivers", "Belts", "Gloves", "Boots", "Armours", "Helmets", "Shields", "Sceptres", "Flask", "Jewel"],
        Style = styles.STYLE_HIDEALL,
    ),
    pf.Category("Show Everything Else for Safety"
    )
))

# Elder Tiering

exfilter.sections['Shaper/Elder Items'] = poetiergen2.GenerateShaperElderSection(
    league_name,
    exfilter.sections['Shaper/Elder Items'], 
    21, 
    styles.STYLE_SHAPERELDER_CHAOS, 
    styles.STYLE_SHAPERELDER_EXALT,
    download_mode
)

# Divination Tiering

div_garbage, div_ex = poetiergen2.GenerateDivinationTiers(
    league_name,
    download_mode,
    21,
    exfilter.exception_from_section('Divination Cards'),
)

exfilter.sections['Divination Cards'].categories['Divination T1'].seta(BaseType = div_ex)
exfilter.sections['Divination Cards'].categories['Divination Garbage'].seta(BaseType = div_garbage)

# Uniques Tiering

unique_garbage, unique_ex, unique_mixed = poetiergen2.GenerateUniqueTiers(
    league_name,
    download_mode,
    21,
    exfilter.exception_from_section('Uniques'),
)

exfilter.sections['Uniques'].categories['Uniques T1'].seta(BaseType = unique_ex)
exfilter.sections['Uniques'].categories['Uniques Garbage'].seta(BaseType = unique_garbage)

write_to_file('testoutput.txt', exfilter)