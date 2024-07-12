from PIL import Image
from os.path import exists


def g_image_convert(fullname, nfullname, quality=90, color=(255, 255, 255)):
    if not exists(fullname):
        print(f"{fullname} 文件不存在")
        return
    image = Image.open(fullname)
    new_image = Image.new("RGB", image.size, color)
    new_image.paste(image, (0, 0), mask=image)
    new_image.save(nfullname, quality=quality)
