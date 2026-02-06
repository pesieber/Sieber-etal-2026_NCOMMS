#!/usr/bin/env python3

## Plotting settings for scientific paper (Nature style)
## Petra Sieber, Dec 2025

import matplotlib.pyplot as plt
import matplotlib as mpl

# Figure size Nature
single_width = 8.8/2.54 # 1 column
double_width = 18/2.54 # 2 columns (full width)

plt.style.use('default') # revert to original settings

def set_plot_param():
    # Text
    fontsize = 7
    mpl.rcParams['font.sans-serif'] = 'Arial'
    mpl.rcParams['font.size'] = fontsize
    mpl.rcParams['figure.titlesize'] = fontsize
    mpl.rcParams['figure.labelsize'] = fontsize
    mpl.rcParams['legend.fontsize'] = fontsize
    mpl.rcParams['axes.titlesize'] = fontsize
    mpl.rcParams['axes.labelsize'] = fontsize
    mpl.rcParams['xtick.labelsize'] = fontsize
    mpl.rcParams['ytick.labelsize'] = fontsize
    mpl.rcParams['axes.labelpad'] = 4
    mpl.rcParams['axes.titlepad'] = 4
    mpl.rcParams['mathtext.default'] = 'regular' # instead of $\mathregular{m^2}$
    # unicode superscript generator https://lingojam.com/SuperscriptGenerator
    
    # Lines
    linewidth = 0.5
    mpl.rcParams['axes.linewidth'] = linewidth
    mpl.rcParams['grid.linewidth'] = linewidth
    mpl.rcParams['lines.linewidth'] = 1
    mpl.rcParams['lines.markersize'] = 3
    
    # Ticks
    mpl.rcParams['xtick.major.size'] = 2.5
    mpl.rcParams['xtick.major.pad'] = 2
    mpl.rcParams['xtick.major.width'] = linewidth
    mpl.rcParams['xtick.minor.size'] = 1.5
    mpl.rcParams['xtick.minor.pad'] = 1.5
    mpl.rcParams['xtick.minor.width'] = linewidth
    mpl.rcParams['xtick.minor.visible'] = False # keep default
    mpl.rcParams['xtick.top'] = False # keep default
    
    mpl.rcParams['ytick.direction'] = 'out' # keep default
    mpl.rcParams['ytick.major.size'] = 2.5
    mpl.rcParams['ytick.major.pad'] = 2
    mpl.rcParams['ytick.major.width'] = linewidth
    mpl.rcParams['ytick.minor.size'] = 1.5
    mpl.rcParams['ytick.minor.pad'] = 1.5
    mpl.rcParams['ytick.minor.width'] = linewidth
    mpl.rcParams['ytick.minor.visible'] = False # keep default
    mpl.rcParams['ytick.right'] = False # keep default
    
    # Legend
    mpl.rcParams['legend.edgecolor'] = 'black'
    mpl.rcParams['legend.framealpha'] = 1
    mpl.rcParams['legend.handleheight'] = 0.7 # default
    mpl.rcParams['legend.handlelength'] = 2.0 # 2.0 default
    mpl.rcParams['legend.handletextpad'] = 0.5 # 0.8 default
    mpl.rcParams['legend.labelspacing'] = 0.4 # 0.5 default
    
    # Figure size
    single_width = 9/2.54 # 3.54
    double_width = 18/2.54 # 7.09
    mpl.rcParams['figure.figsize'] = [3.5, 2.5]  # max width is 3.5 inch (9 cm) for single column, 7 inch (18 cm) for double, max length is 9.7 inch (24.7 cm)
    mpl.rcParams['figure.dpi'] = 150 # display
    mpl.rcParams['figure.constrained_layout.use'] = False
    mpl.rcParams['figure.constrained_layout.w_pad'] = 0.02 # minimum space around the Axes in inches
    mpl.rcParams['figure.constrained_layout.h_pad'] = 0.02
    mpl.rcParams['figure.constrained_layout.wspace'] = 0.05 # space between subplots as a fraction of the size of the subplot group (only used if larger than w_pad or h_pad)
    mpl.rcParams['figure.constrained_layout.hspace'] = 0.05
    
    # Save
    mpl.rcParams['savefig.bbox'] = None # do not use 'tight' as this distorts sizes (incl. fonts)
    mpl.rcParams['savefig.pad_inches'] = 0.01 # use virtually all space when we specify figure dimensions (0.1 is default)
    mpl.rcParams['savefig.dpi'] = 300 # for png, does not affect vector formats like PDF
    mpl.rcParams['pdf.fonttype'] = 42 # use type 42 (= TrueType) fonts for PostScript and PDF files
    mpl.rcParams['ps.fonttype'] = 42

    # Boxplot settings
    mpl.rcParams['boxplot.boxprops.linewidth'] = 0.5
    mpl.rcParams['boxplot.whiskerprops.linewidth'] = 0.5
    mpl.rcParams['boxplot.capprops.linewidth'] = 0.5
    mpl.rcParams['boxplot.flierprops.linewidth'] = 0.5
    mpl.rcParams['boxplot.flierprops.markeredgewidth'] = 0.5
    mpl.rcParams['boxplot.meanprops.linewidth'] = 0.5
    mpl.rcParams['boxplot.medianprops.linewidth'] = 0.5

opts = dict(boxprops=dict(linewidth=0.5, edgecolor='black'),
            whiskerprops=dict(linewidth=0.5, color='black'),
            capprops=dict(linewidth=0.5, color='black'),
            medianprops=dict(linewidth=0.5, color='black'))