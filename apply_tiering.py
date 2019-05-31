import poefilter as pf
import exfilter_styles as styles
from poepy_core import write_to_file
import poetiergen2

league_name = r"Synthesis"
download_mode = False
filter_file_name = r"testoutput2.filter"

shaperelder_cutoff = 15
divination_cutoff = 2
uniques_cutoff = 8

exfilter = pf.FilterObj().from_file(filter_file_name)

# Shaper/Elder Tiering

poetiergen2.GenerateShaperElderSectionFromTag(
    league_name,
    download_mode,
    shaperelder_cutoff,
    styles.STYLE_SHAPERELDER_CHAOS,
    styles.STYLE_SHAPERELDER_EXALT,
    exfilter,
)

# Divination Tiering

poetiergen2.GenerateDivinationTiersFromTag(
    league_name, download_mode, divination_cutoff, exfilter
)


# Uniques Tiering

poetiergen2.GenerateUniqueTiersFromTag(
    league_name, download_mode, uniques_cutoff, exfilter
)

# path_to_filter = r'testoutput.filter'

# path_to_filter = os.path.join(os.path.expanduser(r"~\Documents\My Games\Path of Exile"), filter_file_name)

# write_to_file(path_to_filter, exfilter)
