# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

from __future__ import division, unicode_literals
import math
import numpy as np

from monty.dev import deprecated

"""
Utilities for generating nicer plots.
"""


__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "Mar 13, 2012"


def pretty_plot(width=8, height=None, plt=None, dpi=None,
                color_cycle=("qualitative", "Set1_9")):
    """
    Provides a publication quality plot, with nice defaults for font sizes etc.

    Args:
        width (float): Width of plot in inches. Defaults to 8in.
        height (float): Height of plot in inches. Defaults to width * golden
            ratio.
        plt (matplotlib.pyplot): If plt is supplied, changes will be made to an
            existing plot. Otherwise, a new plot will be created.
        dpi (int): Sets dot per inch for figure.
        color_cycle (tuple): Set the color cycle for new plots to one of the
            color sets in palettable. Defaults to a qualitative Set1_9.

    Returns:
        Matplotlib plot object with properly sized fonts.
    """
    ticksize = int(width * 2.5)

    golden_ratio = (math.sqrt(5) - 1.0) / 2.0

    if not height:
        height = int(width * golden_ratio)

    if plt is None:
        import matplotlib.pyplot as plt
        import importlib
        mod = importlib.import_module("palettable.colorbrewer.%s" %
                                      color_cycle[0])
        colors = getattr(mod, color_cycle[1]).mpl_colors
        from cycler import cycler

        plt.figure(figsize=(width, height), facecolor="w", dpi=dpi)
        ax = plt.gca()
        ax.set_prop_cycle(cycler('color', colors))
    else:
        fig = plt.gcf()
        fig.set_size_inches(width, height)
    plt.xticks(fontsize=ticksize)
    plt.yticks(fontsize=ticksize)

    ax = plt.gca()
    ax.set_title(ax.get_title(), size=width * 4)

    labelsize = int(width * 3)

    ax.set_xlabel(ax.get_xlabel(), size=labelsize)
    ax.set_ylabel(ax.get_ylabel(), size=labelsize)

    return plt


@deprecated(pretty_plot, "get_publication_quality_plot has been renamed "
                         "pretty_plot. This stub will be removed in pmg 5.0.")
def get_publication_quality_plot(*args, **kwargs):
    return pretty_plot(*args, **kwargs)


def get_ax_fig_plt(ax=None):
    """
    Helper function used in plot functions supporting an optional Axes argument.
    If ax is None, we build the `matplotlib` figure and create the Axes else
    we return the current active figure.

    Returns:
        ax: :class:`Axes` object
        figure: matplotlib figure
        plt: matplotlib pyplot module.
    """
    import matplotlib.pyplot as plt
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
    else:
        fig = plt.gcf()

    return ax, fig, plt


def get_ax3d_fig_plt(ax=None):
    """
    Helper function used in plot functions supporting an optional Axes3D
    argument. If ax is None, we build the `matplotlib` figure and create the
    Axes3D else we return the current active figure.

    Returns:
        ax: :class:`Axes` object
        figure: matplotlib figure
        plt: matplotlib pyplot module.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import axes3d
    if ax is None:
        fig = plt.figure()
        ax = axes3d.Axes3D(fig)
    else:
        fig = plt.gcf()

    return ax, fig, plt


def get_axarray_fig_plt(ax_array, nrows=1, ncols=1, sharex=False, sharey=False,
                        squeeze=True, subplot_kw=None, gridspec_kw=None,
                        **fig_kw):
    """
    Helper function used in plot functions that accept an optional array of Axes
    as argument. If ax_array is None, we build the `matplotlib` figure and
    create the array of Axes by calling plt.subplots else we return the
    current active figure.

    Returns:
        ax: Array of :class:`Axes` objects
        figure: matplotlib figure
        plt: matplotlib pyplot module.
    """
    import matplotlib.pyplot as plt

    if ax_array is None:
        fig, ax_array = plt.subplots(nrows=nrows, ncols=ncols, sharex=sharex,
                                     sharey=sharey, squeeze=squeeze,
                                     subplot_kw=subplot_kw,
                                     gridspec_kw=gridspec_kw, **fig_kw)
    else:
        fig = plt.gcf()
        if squeeze:
            ax_array = np.array(ax_array).ravel()
            if len(ax_array) == 1:
                ax_array = ax_array[1]

    return ax_array, fig, plt


def add_fig_kwargs(func):
    """
    Decorator that adds keyword arguments for functions returning matplotlib
    figures.

    The function should return either a matplotlib figure or None to signal
    some sort of error/unexpected event.
    See doc string below for the list of supported options.
    """
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        # pop the kwds used by the decorator.
        title = kwargs.pop("title", None)
        size_kwargs = kwargs.pop("size_kwargs", None)
        show = kwargs.pop("show", True)
        savefig = kwargs.pop("savefig", None)
        tight_layout = kwargs.pop("tight_layout", False)

        # Call func and return immediately if None is returned.
        fig = func(*args, **kwargs)
        if fig is None:
            return fig

        # Operate on matplotlib figure.
        if title is not None:
            fig.suptitle(title)

        if size_kwargs is not None:
            fig.set_size_inches(size_kwargs.pop("w"), size_kwargs.pop("h"),
                                **size_kwargs)

        if savefig:
            fig.savefig(savefig)
        if tight_layout:
            fig.tight_layout()
        if show:
            import matplotlib.pyplot as plt
            plt.show()

        return fig

    # Add docstring to the decorated method.
    s = "\n" + """\
    keyword arguments controlling the display of the figure:

    ================  ====================================================
    kwargs            Meaning
    ================  ====================================================
    title             Title of the plot (Default: None).
    show              True to show the figure (default: True).
    savefig           'abc.png' or 'abc.eps' to save the figure to a file.
    size_kwargs       Dictionary with options passed to fig.set_size_inches
                      example: size_kwargs=dict(w=3, h=4)
    tight_layout      True if to call fig.tight_layout (default: False)
    ================  ===================================================="""

    if wrapper.__doc__ is not None:
        # Add s at the end of the docstring.
        wrapper.__doc__ += "\n" + s
    else:
        # Use s
        wrapper.__doc__ = s

    return wrapper
