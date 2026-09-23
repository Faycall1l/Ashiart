"""Pixel-level tonal operators on grayscale images (NumPy, no extra deps)."""

import numpy as np
from PIL import Image


def apply_clahe(gray, tiles=8, clip=2.0):
    """Contrast-limited adaptive histogram equalization.

    Splits the frame into tiles, equalizes each with a clipped
    histogram, and blends tile mappings with bilinear interpolation so
    no seams appear. Flat tiles stay flat: clipped excess redistributes
    uniformly instead of amplifying noise.

    Args:
        gray (PIL.Image): Grayscale image.
        tiles (int): Tile count per axis.
        clip (float): Clip limit as a multiple of the uniform height.

    Returns:
        PIL.Image: Locally equalized grayscale image.
    """
    source = np.asarray(gray, dtype=np.float64)
    height, width = source.shape
    tile_h = max(height // tiles, 1)
    tile_w = max(width // tiles, 1)
    rows = (height + tile_h - 1) // tile_h
    cols = (width + tile_w - 1) // tile_w
    padded = np.pad(source, ((0, rows * tile_h - height), (0, cols * tile_w - width)),
                    mode="edge")
    full_h, full_w = padded.shape

    luts = np.zeros((rows, cols, 256))
    for i in range(rows):
        for j in range(cols):
            tile = padded[i * tile_h:(i + 1) * tile_h, j * tile_w:(j + 1) * tile_w]
            if tile.max() == tile.min():
                luts[i, j] = np.arange(256)
                continue
            hist, _ = np.histogram(tile, bins=256, range=(0, 256))
            limit = clip * tile.size / 256
            hist = np.minimum(hist, limit) + max(np.maximum(hist - limit, 0).sum(), 0) / 256
            cdf = hist.cumsum()
            positive = cdf[cdf > 0]
            denom = tile.size - positive[0] if positive.size else 0
            luts[i, j] = (cdf - positive[0]) / denom * 255 if denom > 0 else np.arange(256)

    grid_y, grid_x = np.mgrid[0:full_h, 0:full_w]
    pos_y = np.clip((grid_y + 0.5 - tile_h / 2) / tile_h, 0, rows - 1)
    pos_x = np.clip((grid_x + 0.5 - tile_w / 2) / tile_w, 0, cols - 1)
    y0 = np.floor(pos_y).astype(int)
    x0 = np.floor(pos_x).astype(int)
    y1 = np.minimum(y0 + 1, rows - 1)
    x1 = np.minimum(x0 + 1, cols - 1)
    wy = (pos_y - y0)[..., None]
    wx = (pos_x - x0)[..., None]
    levels = padded.astype(int)[..., None]
    top = np.take_along_axis(luts[y0, x0], levels, axis=-1) * (1 - wx)
    top += np.take_along_axis(luts[y0, x1], levels, axis=-1) * wx
    bottom = np.take_along_axis(luts[y1, x0], levels, axis=-1) * (1 - wx)
    bottom += np.take_along_axis(luts[y1, x1], levels, axis=-1) * wx
    mapped = (top * (1 - wy) + bottom * wy)[:, :, 0]
    return Image.fromarray(np.round(mapped[:height, :width]).astype(np.uint8), mode="L")


def _gaussian_blur(frame, sigma):
    """Separable Gaussian blur with edge replication."""
    radius = max(int(3 * sigma), 1)
    axis = np.arange(-radius, radius + 1)
    kernel = np.exp(-(axis ** 2) / (2 * sigma ** 2))
    kernel /= kernel.sum()
    padded = np.pad(frame, radius, mode="edge")
    rows = np.array([np.convolve(row, kernel, mode="valid") for row in padded])
    cols = np.array([np.convolve(col, kernel, mode="valid") for col in rows.T])
    return cols.T


def apply_dog(gray, small=0.8, large=2.0, amplify=2.0):
    """Difference-of-Gaussians detail emphasis.

    Adds the amplified mid-frequency band (small-scale minus
    large-scale blur) back onto the image, sharpening contours and
    texture without shifting global tone.

    Args:
        gray (PIL.Image): Grayscale image.
        small (float): Detail Gaussian sigma.
        large (float): Background Gaussian sigma; must exceed small.
        amplify (float): Detail gain.

    Returns:
        PIL.Image: Detail-emphasized grayscale image.
    """
    if large <= small:
        raise ValueError(f"DoG large sigma must exceed small: {small}, {large}")
    frame = np.asarray(gray, dtype=np.float64)
    detail = _gaussian_blur(frame, small) - _gaussian_blur(frame, large)
    return Image.fromarray(np.clip(np.round(frame + amplify * detail), 0, 255).astype(np.uint8), mode="L")
