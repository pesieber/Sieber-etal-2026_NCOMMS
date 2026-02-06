#!/usr/bin/env python3

## Plotting functions
## Petra Sieber, Dec 2025

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cf

# Plotting settings
lonmin, lonmax, latmin, latmax = [-11, 37, 35, 70.5]                   # window for plotting
set_lonmin, set_lonmax, set_latmin, set_latmax = [-35, 65, 30, 72.6]   # subset the data to get sensible vmin and vmax for the colorbar
data_proj = ccrs.PlateCarree()
map_proj = ccrs.LambertConformal(central_longitude=15) # for regional maps

# Regional plot with coastline and country borders
def format_axes(axes, single=False):
    def format_ax(ax):
        ax.coastlines(resolution='50m', linewidth=0.45)
        ax.add_feature(cf.BORDERS, linewidth=0.3)
        ax.set_extent([lonmin, lonmax, latmin, latmax], crs=data_proj)
        ax.gridlines(draw_labels=False, linewidth=0.3, color="gray", xlocs=range(-180, 180, 10), ylocs=range(-90, 90, 10))
    if single:
        format_ax(axes)
    else:
        for i, ax in enumerate(axes):
            format_ax(ax)

# Add row and column headers (based on https://stackoverflow.com/a/25814386)
def add_headers(fig, *, row_headers=None, col_headers=None, row_pad=1, col_pad=4, rotate_row_headers=True, **text_kwargs):
    axes = fig.get_axes()
    for ax in axes:
        sbs = ax.get_subplotspec()
        # Put headers on cols
        if (col_headers is not None) and sbs.is_first_row():
            ax.annotate(
                col_headers[sbs.colspan.start],
                xy=(0.5, 1),
                xytext=(0, col_pad),
                xycoords="axes fraction",
                textcoords="offset points",
                ha="center",
                va="baseline",
                **text_kwargs)
        # Put headers on rows
        if (row_headers is not None) and sbs.is_first_col():
            ax.annotate(
                row_headers[sbs.rowspan.start],
                xy=(0, 0.5),
                xytext=(-ax.yaxis.labelpad - row_pad, 0),
                xycoords=ax.transAxes, # ax.yaxis.label replaced by ax.transAxes
                textcoords="offset points",
                ha="center",
                va="center", # vertical even after rotation
                rotation=rotate_row_headers * 90,
                **text_kwargs)

# Make symmetric y-axis by setting same min/max absolute values
def make_symmetric(ax):
    low, high = ax.get_ylim() # get y-axis limits
    bound = max(abs(low), abs(high)) # find the new limits
    ax.set_ylim(-bound, bound) # set new limits

# Hat plot (based on https://matplotlib.org/stable/gallery/lines_bars_and_markers/hat_graph.html)
def hat_graph(ax, xlabels, values, group_labels, annot, colors, baseline_color):
    """
    Create a hat graph.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes to plot into.
    xlabels : list of str
        The category names to be displayed on the x-axis.
    values : (M, N) array-like
        The data values.
        Rows are the groups (len(group_labels) == M).
        Columns are the categories (len(xlabels) == N).
    group_labels : list of str
        The group labels displayed in the legend.
    """

    def label_bars(heights, rects):
        """Attach a text label on top of each bar."""
        for height, rect in zip(heights, rects):
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),  # 4 points vertical offset.
                        textcoords='offset points',
                        ha='center', va='bottom')

    values = np.asarray(values)
    x = np.arange(values.shape[1])
    ax.set_xticks(x, labels=xlabels)
    spacing = 0.3  # spacing between hat groups
    width = (1 - spacing) / values.shape[0]
    heights0 = values[0]
    for i, (heights, group_label, color) in enumerate(zip(values, group_labels, colors)):
        style = {'fill': False, 'edgecolor': baseline_color, 'linewidth': 0.5} if i == 0 else {'facecolor': color, 'edgecolor': 'black', 'linewidth': 0.5}
        rects = ax.bar(x - spacing/2 + i * width, heights - heights0, width, bottom=heights0, label=group_label, **style)
        if annot is True:
            label_bars(heights, rects)

    # Draw horizontal baseline across categories
    for xi, base in zip(x, heights0):
        ax.hlines(y=base, xmin=xi-width*1.3, xmax=xi+width*2.7, color=baseline_color, linewidth=0.5)

# Class from the mpl docs: https://matplotlib.org/users/colormapnorms.html
class MidpointNormalize(mpl.colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        super().__init__(vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))