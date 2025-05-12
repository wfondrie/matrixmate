"""MatrixMate creates educational graphics depicting matrices.

That's all. I was just tired of drawing these by hand.
"""
import logging

import sys
import click
import matplotlib.pyplot as plt
import numpy as np


def draw_matrix(
    n_rows: int,
    n_cols: int,
    fill_colors: str | np.ndarray = "black",
    edge_color: str = "white",
    edge_width: float = 2.0,
    size: float = 1.0,
) -> tuple[plt.Figure, plt.Axes]:
    """Illustrate a matrix of a specified size.

    Parameters
    ----------
    n_rows : int
        Number of rows in the matrix.
    n_cols : int
        Number of columns in the matrix.
    fill_colors : str or array of str
        Either a single Matplotlib‐compatible color, or an array of
        colors. If an array, it must match the provided shape.
    edge_color : color
        A Matplotlib-compatible color for the grid lines.
    edge_width : float
        Line width of the grid lines.
    size : float
        Size of each cell of the matrix, in inches.
    dpi : float
        The resolution of the figure.

    Returns
    -------
    fig, ax : Matplotlib Figure and Axes objects
    """
    if not np.ndim(fill_colors):
        fill_colors = np.full((n_rows, n_cols), fill_colors, dtype=object)
    else:
        fill_colors = np.array(fill_colors)

    fig, ax = plt.subplots(
        figsize=(n_cols * size, n_rows * size),
        dpi=100,
        frameon=False,
    )

    # Draw one Rectangle per cell
    for i in range(n_rows):
        for j in range(n_cols):
            ax.add_patch(
                plt.Rectangle(
                    (j, i),   # lower‐left corner at (col, row)
                    1, 1,     # width=1, height=1
                    facecolor=fill_colors[i, j],
                    edgecolor=edge_color,
                    linewidth=edge_width,
                )
            )

    # Set limits exactly to the grid and force square cells
    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)
    ax.set_aspect('equal')
    ax.axis('off')  # no ticks, no frame

    # Remove all margins
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig, ax


@click.command()
@click.argument("n_rows", type=int)
@click.argument("n_cols", type=int)
@click.option(
    "-f",
    "--fill-color",
    type=str,
    help="A Matplotlib-compatible fill color.",
    default="black",
)
@click.option(
    "-e",
    "--edge-color",
    type=str,
    help="A Matplotlib-compatible edge color.",
    default="white",
)
@click.option(
    "-w",
    "--edge-width",
    type=float,
    help="Width of the edges.",
    default=4.0
)
@click.option(
    "-s",
    "--size",
    type=float,
    help="Size of each cell in inches.",
    default=1.0,
)
@click.option(
    "-d",
    "--dpi",
    type=float,
    help="Resolution of the figure. Doesnt affect SVG outputs.",
    default=100,
)
@click.option(
    "-o",
    "--output-format",
    type=click.Choice(["png", "svg", "jpg"]),
    help="The output format.",
    default="png",
)
def main(n_rows, n_cols, fill_color, edge_color, edge_width, size, dpi, output_format):
    """Create a simple matrix graphic.

    The image is sent to stdout.
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.info("Creating a matrix graphic...")

    fix, ax = draw_matrix(
        n_rows,
        n_cols,
        fill_colors=fill_color,
        edge_color=edge_color,
        edge_width=edge_width,
        size=size,
    )

    out = plt.savefig(
        sys.stdout,
        format=output_format,
        dpi=dpi,
        transparent=True,
    )


if __name__ == "__main__":
    main()
