import cv2
import numpy as np
from matplotlib import pyplot as plt


def prepare_plot_args(image, cmap=None):
    """Prepare the arguments for imshow based on the image type and optional colormap."""
    if len(image.shape) == 2:  # Grayscale image
        cmap = cmap or 'gray'  # Use provided colormap or default to 'gray'
        vmin, vmax = (0, 255) if image.dtype == np.uint8 else (None, None)
        return image, {'cmap': cmap, 'vmin': vmin, 'vmax': vmax}
    else:  # Color image (assumes BGR)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), {}


def display_image(ax, image, title=None, cmap=None):
    """Display an image on a matplotlib axis with an optional colormap."""
    img_data, plot_args = prepare_plot_args(image, cmap)
    ax.imshow(img_data, **plot_args)
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=10)


def imshow(image, title=None, figsize=None, show=True, cmap=None):
    """Plot an image using matplotlib with an optional colormap."""
    args = {}
    if figsize is not None:
        args = {"figsize": figsize}
    fig, ax = plt.subplots(**args)
    display_image(ax, image, title, cmap)
    if show:
        plt.show()
        return None
    else:
        return fig, ax


def show_images(images, titles=None, grid=None, figsize=None, title=None, subtitle=None, show=True, colormaps=None):
    """Display multiple images in a grid with optional colormaps."""
    if grid is None:
        grid = (1, len(images))

    if titles is None:
        titles = [None] * len(images)

    # Handle colormaps: if a single colormap is provided, use it for all images
    if colormaps is not None:
        if isinstance(colormaps, str):
            colormaps = [colormaps] * len(images)
        elif len(colormaps) != len(images):
            raise ValueError("Length of colormaps must match the number of images.")
    else:
        colormaps = [None] * len(images)

    n_rows, n_cols = grid
    if figsize is None:
        w = 10
        h = int(1.2 * n_rows * w / n_cols)
        figsize = (w, h)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    if isinstance(axes, np.ndarray):
        axes = axes.flat
    else:
        axes = [axes]

    for i, ax in enumerate(axes):
        if i < len(images):
            display_image(ax, images[i], titles[i], colormaps[i])
        else:
            ax.axis('off')

    if title:
        fig.text(0.5, 1, title, ha='center', fontsize=12)

    if subtitle:
        fig.text(0.5, 0, subtitle, ha='center', fontsize=12)

    plt.tight_layout()

    if show:
        plt.show()
        return None
    return fig, axes