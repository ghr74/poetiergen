import poefilter as pf

# fmt: off

STYLE_QUEST_EXTRA_SPECIAL = pf.Style(
    SetTextColor = "255 255 255 255",
    SetBorderColor = "255 255 255 255",
    SetBackgroundColor = "37 105 175 255",
    MinimapIcon = "0 Blue Triangle",
    PlayAlertSound = "2 300",
)
STYLE_EXPLICIT_MOD = pf.Style(
    SetTextColor = "255 190 0",
    SetBorderColor = "0 240 190 240",
    SetBackgroundColor = "0 75 30 255",
    PlayAlertSound = "3 300",
    MinimapIcon = "0 Green Diamond",
    PlayEffect = "Green Temp",
    CustomAlertSound = pf.CustomSound('RareItem'),  
)
STYLE_DIVINE_RECIPE = pf.Style(
    SetTextColor = "0 0 0 255",
    SetBorderColor = "0 0 0 255",
    SetBackgroundColor = "125 0 125 255",
    MinimapIcon = "0 Brown Triangle",
    PlayEffect = "Brown",
    PlayAlertSound = "8 150",
    CustomAlertSound = pf.CustomSound('TABBY'),
)
STYLE_JEWELLER_RECIPE = pf.Style(
    SetBackgroundColor = "34 34 51",
    SetTextColor = "179 99 255",
    SetBorderColor = "179 99 255",
    MinimapIcon = "0 Yellow Circle",
    PlayEffect = "Yellow Temp",
    PlayAlertSound = "4 130",
    CustomAlertSound = pf.CustomSound('Currency'),
)
STYLE_UNIQUES_CHAOS = pf.Style(
    SetTextColor = "0 0 0 255",
    SetBorderColor = "255 103 89",
    SetBackgroundColor = "255 103 89",
    MinimapIcon = "0 Brown Star",
    PlayEffect = "Brown",
    PlayAlertSound = "8 150",
    CustomAlertSound = pf.CustomSound('Unique'),
)
STYLE_UNIQUES_EXALT = STYLE_UNIQUES_CHAOS.changed_copy(
    SetTextColor = "175 96 37 255",
    SetBorderColor = "175 96 37 255",
    SetBackgroundColor = "255 255 255 255",
    PlayAlertSound = "6 300",
    CustomAlertSound = pf.CustomSound('Exalt'),
)
STYLE_UNIQUES_GARBAGE = pf.Style(
    SetFontSize = 42,
    SetBackgroundColor = "34 34 51",
    SetTextColor = "121 72 0 230",
    SetBorderColor = "34 34 51",
)
STYLE_DIVINATION_EXCEPTION = pf.Style(
    SetBackgroundColor = "34 34 51",
    SetBorderColor = "75 225 255",
    SetTextColor = "75 225 255",
)
STYLE_DIVINATION_CHAOS = STYLE_DIVINATION_EXCEPTION.changed_copy(
    MinimapIcon = "0 Blue Square",
    CustomAlertSound = pf.CustomSound('Divination'),
)
STYLE_DIVINATION_EXALT = pf.Style(
    SetTextColor = "255 0 0 255",
    SetBorderColor = "255 0 0 255",
    SetBackgroundColor = "255 255 255 255",
    MinimapIcon = "0 White Square",
    PlayEffect = "White",
    PlayAlertSound = "6 300",
    CustomAlertSound = pf.CustomSound('Exalt'),
)
STYLE_CURRENCY_EXALT = STYLE_DIVINATION_EXALT.changed_copy(
    MinimapIcon = "0 Red Circle",
    PlayEffect = "Yellow",
)
STYLE_CURRENCY_CHAOS = pf.Style(
    SetBackgroundColor = "34 34 51",
    SetTextColor = "29 255 26",
    SetBorderColor = "34 34 51",
    MinimapIcon = "0 Green Circle",
    PlayEffect = "Green Temp",
    PlayAlertSound = "5 100",
    CustomAlertSound = pf.CustomSound('Currency'),
)
STYLE_CURRENCY_LOW = pf.Style(
    SetBackgroundColor = "34 34 51",
    SetTextColor = "230 230 0",
)
STYLE_CURRENCY_GARBAGE = pf.Style(
    SetBorderColor = "125 125 255",
)
STYLE_CURRENCY_STACKABLE = pf.Style(
    SetBackgroundColor = "0 0 0 255",
    SetTextColor = "255 0 255",
    SetBorderColor = "255 0 255",
    PlayAlertSound = "2 300",
    MinimapIcon = "0 Blue Circle",
    CustomAlertSound = pf.CustomSound('Splinter'),
)
STYLE_MAP_FRAGMENTS = pf.Style(
    SetTextColor = "255 0 125",
    SetBackgroundColor = "0 0 0",
    SetBorderColor = "255 0 125",
    MinimapIcon = "0 Green Hexagon",
    PlayAlertSound = "4 300",
    CustomAlertSound = pf.CustomSound('Splinter'),
)
STYLE_MAP_SHAPED = pf.Style(
    SetBorderColor = "0 0 0",
    SetBackgroundColor = "0 255 136",
    SetTextColor = "0 0 0",
    MinimapIcon = "0 Green Hexagon",
    PlayEffect = "Green",
    PlayAlertSound = "1 135",
    CustomAlertSound = pf.CustomSound('ShapedMap'),
)
STYLE_MAP_ELDER = STYLE_MAP_SHAPED.changed_copy(
    SetBackgroundColor = "0 255 234 155",
    CustomAlertSound = pf.CustomSound("ElderMap", 'wav'),
)
STYLE_MAP_RED = STYLE_MAP_SHAPED.changed_copy(
    SetBackgroundColor = "255 0 0",
    MinimapIcon = "0 Red Hexagon",
    PlayEffect = "Red Temp",
    CustomAlertSound = pf.CustomSound("RedMap"),
)
STYLE_MAP_YELLOW = STYLE_MAP_SHAPED.changed_copy(
    SetBackgroundColor = "255 255 0",
    MinimapIcon = "0 Yellow Hexagon",
    PlayAlertSound = "4 200",
	CustomAlertSound = pf.CustomSound("YellowMap"),
)
STYLE_MAP_WHITE = pf.Style(
    SetBorderColor = "0 0 0",
    SetBackgroundColor = "34 34 51",
    SetTextColor = "24 244 167",
)
STYLE_SKILLGEM_LOW = pf.Style(
    SetBackgroundColor = "34 34 51",
	SetTextColor = "92 172 238",
)
STYLE_SKILLGEM_HIGH = STYLE_SKILLGEM_LOW.changed_copy(
    MinimapIcon = "0 Blue Diamond",
    PlayAlertSound = "5 200",
    CustomAlertSound = pf.CustomSound("TABBY"),
)
STYLE_SHAPERELDER_EXALT = pf.Style(
    SetTextColor = "50 130 165 255",
    SetBorderColor = "50 130 165 255",
    SetBackgroundColor = "255 255 255 255",
    PlayAlertSound = "1 300",
    MinimapIcon = "0 Red Diamond",
    PlayEffect = "Red",
)
STYLE_SHAPERELDER_CHAOS = pf.Style(
    SetTextColor = "255 255 255 255",
    SetBorderColor = "255 255 255 255",
    SetBackgroundColor = "20 110 220",
    PlayAlertSound = "3 300",
    MinimapIcon = "0 Yellow Diamond",
    PlayEffect = "Yellow",
)
STYLE_BASES_MEDIOCRE = pf.Style(
    MinimapIcon = "0 Yellow Diamond",
    SetBackgroundColor = "34 34 51",
	SetTextColor = "92 172 238",
    CustomAlertSound = pf.CustomSound("RareItem"),
)
STYLE_BASES_SHITTY = pf.Style(
    SetTextColor = "0 200 0",
	SetBackgroundColor = "34 34 51",
)
STYLE_CHROMATIC_RECIPE = pf.Style(
    SetFontSize = 33,
	SetTextColor = "255 255 119 0",
	SetBackgroundColor = "75 75 75 200",
    SetBorderColor = "255 45 175",
)
STYLE_HIDEALL = pf.Style(
    SetFontSize = 19,
    SetBackgroundColor = "00 00 00 0",
    SetBorderColor = "00 00 00 0",
    SetTextColor = "00 00 00 0",
)

# fmt: on
