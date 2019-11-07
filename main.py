import os
import random
from PIL import Image

currentPath = os.path.dirname(__file__)
imageFolder = os.path.join(currentPath, "images")
resultImage = os.path.join(currentPath, "collage.jpg")

COLORS = {
    "b": (0, 0, 0),  # BLACK
    "w": (255, 255, 255),  # WHITE
    "p": (200, 0, 200),  # PINK
    "1": "FIRSTPIXEL",
}

imageList = []
for root, directories, files in os.walk(imageFolder):
    for file_ in files:
        if file_.endswith("jpg"):
            imageList.append(os.path.join(imageFolder, file_))


def get_optimal_space(w, h, ratio):
    res = []
    for x in range(100):
        x_term = x + (w + x) * cols
        dc = h * rows
        space_y = ((x_term / ratio) - dc) / (rows + 1)
        if space_y.is_integer() and space_y > 0:
            res.append((x, space_y))
    print(*res, sep="\n")
    print("#" * 30)


def create_collage(listofimages):
    global cols
    global rows
    global ratio

    cols = int(input("Num of columns?:\t"))
    rows = int(input("Num of rows?:\t"))
    ratio = input("Expected ratio (10/15)?:\t")

    ratio = int(ratio.split("/")[0]) / int(ratio.split("/")[1])

    num_of_images = cols * rows

    if num_of_images > len(listofimages):
        print("Not enough images!")
        print(f"Expected: {cols * rows} - there are only {len(listofimages)} in list")
        exit()

    random.shuffle(listofimages)
    im1 = Image.open(listofimages[0])

    image_width, image_height = im1.size

    spaceColor = input(
        "Color of space between images? ([B]lack, [W]hite, [P]ink, [1]stPixel) or [N]o space:\t"
    )

    bSpace = True
    if spaceColor.lower() in COLORS.keys():
        if spaceColor == "1":
            spaceColor = im1.convert("RGB").getpixel((1, 1))
        else:
            spaceColor = COLORS[spaceColor]
    elif spaceColor.lower() == "n":
        spaceColor = COLORS["w"]  # defaults to WHITE
        bSpace = False
        print("No space between images")

    if bSpace:
        get_optimal_space(image_width, image_height, ratio)
        spaces = input("Space X, Space Y?:\t")
        space_hor = int(spaces.split(",")[0])
        space_ver = int(spaces.split(",")[1])
    else:
        space_hor = 0
        space_ver = 0

    collage_width = image_width * cols + (space_hor * (cols + 1))
    collage_height = image_height * rows + (space_ver * (rows + 1))

    new_im = Image.new("RGB", (collage_width, collage_height), spaceColor)

    ims = []
    for image in listofimages:
        im = Image.open(image)
        ims.append(im)

    i = 0
    if bSpace:
        x = space_hor
        y = space_ver
    else:
        x = 0
        y = 0

    for col in range(cols):
        for row in range(rows):
            new_im.paste(ims[i], (x, y))
            i += 1
            y += image_height + space_ver

        x += image_width + space_hor

        if bSpace:
            y = space_ver
        else:
            y = 0

    new_im.save(resultImage)


create_collage(imageList)

os.startfile(resultImage)
