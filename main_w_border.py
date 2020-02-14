import os
import random
from PIL import Image

from square_image import crop_image_squared

currentPath = os.path.dirname(__file__)
imageFolder = os.path.join(currentPath, "images")
# resultImage = os.path.join(currentPath, "collage.jpg")
tempImage = os.path.join(currentPath, "temp_collage.jpg")

COLORS = {
    "b": (0, 0, 0),  # BLACK
    "f": "FIRSTPIXEL",
    "p": (200, 0, 200),  # PINK
    "w": (255, 255, 255),  # WHITE
    "r": (
        random.choice(range(256)),
        random.choice(range(256)),
        random.choice(range(256)),
    ),
}

imageList = []
for root, directories, files in os.walk(imageFolder):
    for file_ in files:
        if file_.endswith("jpg"):
            imageList.append(os.path.join(imageFolder, file_))


def get_optimal_space(w, h, cols, rows, ratio):
    print(f"{w=}, {h=}, {ratio=}")
    res = []
    for x in range(100):
        x_term = x + (w + x) * cols
        dc = h * rows
        space_y = ((x_term / ratio) - dc) / (rows + 1)
        if space_y.is_integer() and space_y > 0:
            res.append((x, space_y))
    print(*res, sep="\n")
    print("#" * 30)


def main(
    listofimages,
    cols=False,
    rows=False,
    ratio=False,
    spaceColor=False,
    spaces=False,
    sborder=False,
    sborder_color=False,
    iborder=False,
    squared=False,
):
    #   global cols
    #   global rows
    #   global ratio

    if not cols:
        cols = int(input("Num of columns?:\t"))
    if not rows:
        rows = int(input("Num of rows?:\t"))
    if not ratio:
        ratio = input("Expected ratio (10/15)?:\t")

    try:
        ratio = int(ratio.split("/")[0]) / int(ratio.split("/")[1])
    except (IndexError, ValueError):
        ratio = 10 / 15

    num_of_images = cols * rows

    if num_of_images > len(listofimages):
        print("Not enough images!")
        print(f"Expected: {cols * rows} - there are only {len(listofimages)} in list")
        exit()

    random.shuffle(listofimages)
    im1 = Image.open(listofimages[0])

    if squared:
        im1 = crop_image_squared(im1)

    image_width, image_height = im1.size

    if not spaceColor:
        spaceColor = input(
            "Color of space between images? ([B]lack, [W]hite, [P]ink, [1]stPixel, [R]andom) or [N]o space:\t"
        )

    bSpace = True
    if spaceColor.lower() in COLORS.keys():
        if spaceColor == "f":
            spaceColor = im1.convert("RGB").getpixel((1, 1))
        else:
            spaceColor = COLORS[spaceColor]
    elif spaceColor.lower() == "n":
        spaceColor = COLORS["w"]  # defaults to WHITE
        bSpace = False
        print("No space between images")

    if bSpace:
        if not spaces:
            get_optimal_space(image_width, image_height, cols, rows, ratio)
            spaces = input("Space X, Space Y?:\t")
        space_hor = int(spaces.split(",")[0])
        space_ver = int(spaces.split(",")[1])
    else:
        space_hor = 0
        space_ver = 0

    if not sborder:
        sborder = input("Border around images?[y/n]\t") or 0

    bborder = False
    if sborder.lower() == "y":
        bborder = True
        if not sborder_color:
            sborder_color = input(
                "Color of border around images? ([B]lack, [W]hite, [P]ink, [R]andom)\t"
            )
        if sborder_color.lower() in COLORS.keys():
            borderColor = COLORS[sborder_color]

        if not iborder:
            iborder = int(input("Border size?\t"))
        temp_im_width = image_width + (iborder * 2)
        temp_im_heigth = image_height + (iborder * 2)

    collage_width = (image_width * cols) + (
        space_hor * (cols + 1)
    )  # + (iborder * cols * 2)
    collage_height = (image_height * rows) + (
        space_ver * (rows + 1)
    )  # + (iborder * rows * 2)

    new_im = Image.new("RGB", (collage_width, collage_height), spaceColor)

    ims = []
    for image in listofimages:
        im = Image.open(image)
        if squared:
            im = crop_image_squared(im)

        if bborder:
            temp_im = Image.new("RGB", (temp_im_width, temp_im_heigth), borderColor)
            temp_im.paste(im, (iborder, iborder))
            im = temp_im
            im.save(tempImage)
        ims.append(im)

    i = 0
    if bSpace:
        x = space_hor - iborder
        y = space_ver - iborder
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
            y = space_ver - iborder
        else:
            y = 0

    rand_num = random.randint(1000, 9999)
    resultImage = os.path.join(currentPath, "collage_" + str(cols) + "_" + str(rows) + "_" +
                               str(ratio).replace("/", "x") + "_" + str(spaceColor) + "_" + str(spaces) +
                               "_" + sborder + "_" + sborder_color + "_" + str(iborder) +
                               "_" + ("squared" if squared else "nope") + "_" + str(rand_num) + ".jpg")
    new_im.save(resultImage)
    return resultImage


if __name__ == "__main__":
    resultImage = main(
        imageList,
        cols=3,
        rows=3,
        ratio="1/1",
        spaceColor="r",
        spaces="40,40",
        sborder="y",
        sborder_color="b",
        iborder=10,
        squared=True,
    )
    print(resultImage)
    os.startfile(resultImage)
