import poetiergen2


filter_file_name = r'ExfilterTEST.filter'

league_name = r'Synthesis'
# Armed = Download + Write
armed_mode = False

UniqueExCategory = '%TB-Uniques-Exception'
DivExCategory = '%TB-Divination-Exception'

UniquesCategorySettings = (
    # T1 Category Name
    '%TB-Uniques-T1',
    # Mixed Category Name
    '%TB-Uniques-T2-MultiBase',
    # Garbage Category Name
    '%TB-Uniques-T4',
    # Price Cutoff
    21
)

DivinationCategorySettings = (
    # T1 Category Name
    '%TB-Divination-T1',
    # Garbage Category Name
    '%TB-Divination-T4',
    # Price Cutoff
    21
)

BasesSectionSettings = (
        # Category Name
        '%TB-Bases',
        # Min Price
        21, 
        (
            # Min Price (Chaos) , Category Style
            '''\
            SetFontSize 45
            SetTextColor 50 130 165 255
            SetBorderColor 50 130 165 255
            SetBackgroundColor 255 255 255 255
            PlayAlertSound 1 300
            MinimapIcon 0 Red Diamond
            PlayEffect Red\
            ''', 
            '''\
            SetFontSize 45
            SetTextColor 255 255 255 255
            SetBorderColor 255 255 255 255
            SetBackgroundColor 20 110 220
            PlayAlertSound 3 300
            MinimapIcon 0 Yellow Diamond
            PlayEffect Yellow\
            ''',
        )
)

poetiergen2.FilteryThingy(filter_file_name, league_name, armed_mode, UniqueExCategory, 
    DivExCategory, UniquesCategorySettings, DivinationCategorySettings, BasesSectionSettings)

# poetiergen2.FilteryThingy('testoutput.txt', league_name, armed_mode, 
#     uniques_category_settings=UniquesCategorySettings, 
#     divination_category_settings=DivinationCategorySettings, 
#     bases_section_settings=BasesSectionSettings)