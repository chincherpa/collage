import os
import random
from PIL import Image

currentPath = os.path.dirname(__file__)
imageFolder = os.path.join(currentPath, 'images')
resultImage = os.path.join(currentPath, 'collage.jpg')
imageFolderVariations = 'image_variation_collages'

outerFrame = True
cols = int(input("How many columns?:\t"))  #4
rows = int(input("How many rows?:\t"))  #5
space = int(input("How much space between?:\t"))  #50

Colors = {
    "w" : (255, 255, 255),  # white
    "b" : (0, 0, 0),  # black
    "p" : (193, 0, 207)  # pink
}

Color_choice = input("Space: [b]lack or [w]hite or [p]ink?:\t")
spaceColor = Colors[Color_choice.lower()]

position_original_choice = input("Original image: [f]irst or [l]ast?:\t")

position_original_first = (position_original_choice.lower() == 'f')

imageList = []
for root, directories, files in os.walk(imageFolder):
    for file_ in files:
        if file_.endswith('jpg'):
            imageList.append(os.path.join(imageFolder, file_))


def get_random_values(num):
    lrandom_numbers = []
    for i in range(1, num + 1):
        if i % 4 == 0:
            lrandom_numbers.append(0)
        else:
            lrandom_numbers.append(random.random())
    return tuple(lrandom_numbers)


for num, imageName in enumerate(imageList):

    original_image = Image.open(imageName)
    image_width, image_height = original_image.size

    if outerFrame:
        collage_width = image_width * cols + (space * (cols + 1))
        collage_height = image_height * rows + (space * (rows + 1))
    else:
        collage_width = image_width * cols + (space * (cols - 1))
        collage_height = image_height * rows + (space * (rows - 1))

    new_im = Image.new('RGB', (collage_width, collage_height), spaceColor)

    resultImage = os.path.join(imageFolderVariations, str(num) + '_collage.jpg')

    ims = []
    if position_original_first:
        ims.append(original_image)

    for i in range((cols * rows - 1)):  # minus 1, wegen Originalbild
        tRandomValues = get_random_values(12)
        out = original_image.convert("RGB", tRandomValues)
        ims.append(out)

    if not position_original_first:
        ims.append(original_image)

    i = 0
    if outerFrame:
        x = space
        y = space
    else:
        x = 0
        y = 0

    for col in range(cols):
        for row in range(rows):
            new_im.paste(ims[i], (x, y))
            i += 1
            y += (image_height + space)
        x += (image_width + space)

        if outerFrame:
            y = space
        else:
            y = 0

    new_im.save(resultImage)
