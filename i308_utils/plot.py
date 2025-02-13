import cv2
import numpy as np
from matplotlib import pyplot as plt


def prepare_plot_args(image):
    """prepara los argumentos para imshow según el tipo de imagen"""
    if len(image.shape) == 2:  # imagen en escala de grises
        cmap = 'gray'
        vmin, vmax = (0, 255) if image.dtype == np.uint8 else (None, None)
        return image, {'cmap': cmap, 'vmin': vmin, 'vmax': vmax}
    else:  # imagen en color (asume BGR)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), {}


def display_image(ax, image, title=None):
    """muestra una imagen en un eje matplotlib"""
    img_data, plot_args = prepare_plot_args(image)
    ax.imshow(img_data, **plot_args)
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=10)


def imshow(image, title=None):
    """grafica una imagen usando matplotlib"""
    fig, ax = plt.subplots()
    display_image(ax, image, title)
    plt.show()


def show_images(images, titles=None, grid=None, figsize=None, title=None, subtitle=None, show=True):
    """muestra múltiples imágenes en una cuadrícula"""
    if grid is None:
        grid = (1, len(images))

    if titles is None:
        titles = [None] * len(images)

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
            display_image(ax, images[i], titles[i])
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
