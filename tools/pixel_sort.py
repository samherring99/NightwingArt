from PIL import Image
import numpy as np

def pixel_sort(image_path):
    img = Image.open(image_path)
    pixels = np.array(img)

    for i in range(pixels.shape[0]):
        row = pixels[i]
        # Sort based on pixel brightness
        row_sorted = sorted(row, key=lambda pixel: np.mean(pixel))
        pixels[i] = row_sorted

    result_img = Image.fromarray(pixels)
    result_img.save("outputs/test1_sorted.jpg")

pixel_sort("inputs/test1.jpg")
