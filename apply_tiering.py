import poefilter as pf
import exfilter_styles as styles
from poepy_core import write_to_file
import poetiergen2

league_name = r'Synthesis'
download_mode = False
filter_file_name = r'testoutput2.filter'

shaperelder_cutoff = 15
divination_cutoff = 2
uniques_cutoff = 8

exfilter = pf.FilterObj(source_file = filter_file_name)

# Shaper/Elder Tiering

# exfilter['Shaper/Elder Items'] = poetiergen2.GenerateShaperElderSection(
#     league_name,
#     exfilter.sections['Shaper/Elder Items'],
#     15,
#     styles.STYLE_SHAPERELDER_CHAOS,
#     styles.STYLE_SHAPERELDER_EXALT,
#     download_mode
# )

# Divination Tiering

div_garbage, div_ex = poetiergen2.GenerateDivinationTiers(
    league_name,
    download_mode,
    divination_cutoff,
    exfilter.exception_from_section('Divination Cards'),
)

exfilter['Divination Cards']['Divination T1']['BaseType'] = div_ex
exfilter['Divination Cards']['Divination Garbage']['BaseType'] = div_garbage

# Uniques Tiering

unique_garbage, unique_ex, unique_mixed = poetiergen2.GenerateUniqueTiers(
    league_name,
    download_mode,
    uniques_cutoff,
    exfilter.exception_from_section('Uniques'),
)

exfilter['Uniques']['Uniques T1']['BaseType'] = unique_ex
exfilter['Uniques']['Uniques Garbage']['BaseType'] = unique_garbage

# path_to_filter = r'testoutput.filter'

# path_to_filter = os.path.join(os.path.expanduser(r"~\Documents\My Games\Path of Exile"), filter_file_name)

# write_to_file(path_to_filter, exfilter)