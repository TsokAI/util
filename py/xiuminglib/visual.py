"""
Utility Functions for Visualizations

Xiuming Zhang, MIT CSAIL
June 2017
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def matrix_as_heatmap(mat, outpath=None, figtitle=None):
    """
    Visualizes a matrix as heatmap

    Args:
        mat: Matrix to visualize as heatmp
            2D numpy array
        outpath: Path to which the visualization is saved
            String
            Optional; defaults to './heatmap.png'
        figtitle: Figure title
            String
            Optional; defaults to None (no title)

    Returns:
        None
    """

    figsize = 14
    plt.figure(figsize=(figsize, figsize))
    ax = plt.gca()

    # Set title
    if figtitle is not None:
        ax.set_title(figtitle)

    # Generate heatmap with matrix entries
    im = ax.imshow(mat)

    # Colorbar
    # Create an axes on the right side of ax. The width of cax will be 2%
    # of ax and the padding between cax and ax will be fixed at 0.1 inch.
    cax = make_axes_locatable(ax).append_axes('right', size='2%', pad=0.1)
    plt.colorbar(im, cax=cax)

    # Save plot
    if outpath is None:
        outpath = './heatmap.png'
    plt.savefig(outpath, bbox_inches='tight')
