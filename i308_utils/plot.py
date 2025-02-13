import matplotlib.pyplot as plt
import cv2


def imshow(image, title=None):
    """

        Grafica una imagen usando matplotlib

    """
    if len(image.shape) == 2:  # Imagen en escala de grises
        plt.imshow(image, cmap='gray')
    else:  # Imagen en color (asumimos BGR)
        im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(im)

    if title is not None:
        plt.title(title, fontsize=10)
    plt.axis('off')
    plt.show()


def show_images(
        images,
        titles=None,
        grid=None,
        figsize=None,
        title=None,
        subtitle=None,
        show=True
):
    if grid is None:
        grid = (1, len(images))

    if titles is None:
        titles = [None for _ in images]

    n_rows, n_cols = grid
    if figsize is None:
        w = 10
        h = int(1.2 * n_rows * w / n_cols)
        figsize = (w, h)

    # print(figsize)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # fig.patch.set_facecolor('lightblue')

    for i, ax in enumerate(axes.flat):

        ax.axis('off')
        # ax.set_facecolor('green')
        if i >= len(images):
            continue

        image = images[i]
        if len(image.shape) == 2:  # imagen en escala de grises
            ax.imshow(images[i], cmap='gray', vmin=0, vmax=255)
        else:  # imagen en color (asume BGR)
            im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            ax.imshow(im)

        if titles[i] is not None:
            ax.set_title(titles[i])

    if title:
        fig.text(0.5, 1, title, ha='center', fontsize=12)

    if subtitle:
        fig.text(0.5, 0, subtitle, ha='center', fontsize=12)

    plt.tight_layout()

    if show:
        plt.show()
        return None

    else:

        return fig, axes