import poefilter as pf
import exfilter_styles as styles
from poepy_core import write_to_file
from poetiergen import PoeTierGenerator
import os

league_name = r"Legion"
download = True
use_cache = False
input_filter = r"ExfilterLegion.filter"
output_filter = r"ExfilterGen.filter"

shaperelder_cutoff = 10
divination_cutoff = 0.8
uniques_cutoff = 5

input_filter = os.path.join(
    os.path.expanduser(r"~\Documents\My Games\Path of Exile"), input_filter
)

exfilter = pf.FilterObj().from_file(input_filter)

# Shaper/Elder Tiering

gen = PoeTierGenerator(league_name, exfilter, download, use_cache)

gen.GenerateShaperElderSectionFromTag(
    shaperelder_cutoff, styles.STYLE_SHAPERELDER_CHAOS, styles.STYLE_SHAPERELDER_EXALT
)

# Divination Tiering

gen.GenerateDivinationTiersFromTag(divination_cutoff)


# Uniques Tiering

gen.GenerateUniqueTiersFromTag(uniques_cutoff)

# path_to_filter = r'testoutput.filter'

output_filter = os.path.join(
    os.path.expanduser(r"~\Documents\My Games\Path of Exile"), output_filter
)

write_to_file(output_filter, exfilter)
