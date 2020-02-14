from PIL import Image


def crop_image_squared(img):
  image_width, image_height = img.size
  left = (image_width - image_height) // 2
  top = 0
  right = left + image_height
  bottom = image_height

  return img.crop((left, top, right, bottom))


if __name__ == "__main__":
  import os
  currentPath = os.path.dirname(__file__)
  # imageFolder = os.path.join(currentPath, 'images')
  imageFolder = os.path.join(currentPath, 'squaretest')
  imageFolderSquares = 'squared_images'
  
  imageList = []
  for root, directories, files in os.walk(imageFolder):
    for file_ in files:
      if file_.endswith('jpg'):
        imageList.append(os.path.join(imageFolder, file_))

  for num, imageName in enumerate(imageList):
    filename = os.path.basename(imageName)
    original_image = Image.open(imageName)
    new_im = crop_image_squared(original_image)
    size = 600
    new_im = new_im.resize((size, size))
    resultImage = os.path.join(imageFolderSquares, os.path.splitext(filename)[0] + '_squared.jpg')
    new_im.save(resultImage)
    print(resultImage)
