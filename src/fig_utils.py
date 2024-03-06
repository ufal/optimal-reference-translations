import matplotlib.style
import matplotlib as mpl
from cycler import cycler

FONT_MONOSPACE = {'fontname':'monospace'}
MARKERS = "o^s*DP1"
COLORS = [
    "cornflowerblue",
    "darkseagreen",
    "seagreen",
    "salmon",
    "orange",
    "dimgray",
    "violet",
]

mpl.rcParams['axes.prop_cycle'] = cycler(color=COLORS)
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.markersize'] = 7
mpl.rcParams['axes.linewidth'] = 1.5

# 'axes.linewidth', 'boxplot.boxprops.linewidth', 'boxplot.capprops.linewidth', 'boxplot.flierprops.linewidth', 'boxplot.meanprops.linewidth', 'boxplot.medianprops.linewidth', 'boxplot.whiskerprops.linewidth', 'contour.linewidth', 'grid.linewidth', 'hatch.linewidth', 'lines.linewidth', 'patch.linewidth']



METRIC_PRETTY_NAME = {
    "bleu": "BLEU",
    "ter": "TER",
    "meteor": "METEOR",
    "chrf": "chrF",
    "comet": "COMET",
    "bleurt": "BLEURT"
}

COLORS_EXTRA = ["#9c2963", "#fb9e07"]
