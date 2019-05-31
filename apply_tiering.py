import poefilter as pf
import exfilter_styles as styles
from poepy_core import write_to_file
from poetiergen import PoeTierGenerator

league_name = r"Synthesis"
download = False
filter_file_name = r"testoutput2.filter"

shaperelder_cutoff = 15
divination_cutoff = 2
uniques_cutoff = 8

exfilter = pf.FilterObj().from_file(filter_file_name)

# Shaper/Elder Tiering

gen = PoeTierGenerator(league_name, exfilter, download)

gen.GenerateShaperElderSectionFromTag(
    shaperelder_cutoff, styles.STYLE_SHAPERELDER_CHAOS, styles.STYLE_SHAPERELDER_EXALT
)

# Divination Tiering

gen.GenerateDivinationTiersFromTag(divination_cutoff)


# Uniques Tiering

gen.GenerateUniqueTiersFromTag(uniques_cutoff)

# path_to_filter = r'testoutput.filter'

# path_to_filter = os.path.join(os.path.expanduser(r"~\Documents\My Games\Path of Exile"), filter_file_name)

# write_to_file(path_to_filter, exfilter)
