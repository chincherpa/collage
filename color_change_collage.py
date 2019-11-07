from PIL import Image

imName = 'American-Staffordshire-Terrier-Canis-Lupus-Familiaris.jpg'
im= Image.open(imName)

out=im.convert("RGB", (
    0.412453, 0.357580, 0.180423, 0,
    0.212671, 0.715160, 0.072169, 0,
    0.019334, 0.119193, 0.950227, 0 ))
out.save("Image2.jpg")

out2=im.convert("RGB", (
    0.9756324, 0.154789, 0.180423, 0,
    0.212671, 0.715160, 0.254783, 0,
    0.123456, 0.119193, 0.950227, 0 ))
out2.save("Image3.jpg")

out3= im.convert("1")
out3.save("Image4.jpg")

out4=im.convert("RGB", (
    0.986542, 0.154789, 0.756231, 0,
    0.212671, 0.715160, 0.254783, 0,
    0.123456, 0.119193, 0.112348, 0 ))
out4.save("Image5.jpg")

out5=Image.blend(im, out4, 0.5)
out5.save("Image6.jpg")

listofimages=[imName, 'Image2.jpg', 'Image3.jpg', 'Image4.jpg', 'Image5.jpg', 'Image6.jpg']

def create_collage(width, height, listofimages):
    cols = 3
    rows = 2
    thumbnail_width = width//cols
    thumbnail_height = height//rows
    size = thumbnail_width, thumbnail_height
    new_im = Image.new('RGB', (width, height))
    ims = []
    for p in listofimages:
        im = Image.open(p)
        im.thumbnail(size)
        ims.append(im)
    i = 0
    x = 0
    y = 0
    for col in range(cols):
        for row in range(rows):
            print(i, x, y)
            new_im.paste(ims[i], (x, y))
            i += 1
            y += thumbnail_height
        x += thumbnail_width
        y = 0

    new_im.save("Collage.jpg")

create_collage(450, 300, listofimages)