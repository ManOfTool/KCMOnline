from base64 import b64encode, b64decode
from PIL import Image
from io import BytesIO
from math import ceil
from uuid import uuid4
import re, os

FILE_PATH = ''
MIME_CHECK = re.compile('data:image/(jpeg|png);base64')

def mergeImages(dataList, mode=0, row=2):
    images = []
    for i in dataList:
        prefix, d = splitData(i)

        if MIME_CHECK.match(prefix):
            try:
                images.append(Image.open(BytesIO(b64decode(d))))
            except Exception as e:
                return str(e)

    num_images = len(images)

    if num_images == 0:
        return 'No images found', None

    x, y = modeSelect(mode, num_images, row)

    if (x, y) == (-1, -1):
        return 'Unknown mode', None

    max_width = max([i.width for i in images])
    max_height = max([i.height for i in images])

    print(max_height, max_width)

    new_image = Image.new('RGB', (max_width*x, max_height*y), (255,255,255))

    # exit()
    x_offset = 0
    y_offset = 0

    # Merging images
    cnt = 0
    for i in range(y):
        for j in range(x):
            new_image.paste(
                images[cnt],
                (x_offset + max_width * j, y_offset + max_height * i))
            cnt += 1

            if cnt >= num_images:
                break

    file_name = FILE_PATH + uuid4().hex + '.jpg'
    new_image.save(file_name, 'JPEG', quality=80, optimize=True, Progressive=True)

    with open(file_name, 'rb') as f:
        f = f.read()
    result = str(b64encode(f), 'utf-8')

    os.remove(file_name)

    return 'Done', 'data:image/jpeg;base64,' + result

def modeSelect(mode, n=0, r=2):
    x = -1
    y = -1
    if r == 0:
        r = 1
    r = abs(r)

    if mode == 'hl':
        x = n
        y = 1

    elif mode == 'hw':
        x = ceil(n / 2)
        y = ceil(n / x)

    elif mode == 'vl':
        x = 1
        y = n

    elif mode == 'vw':
        y = ceil(n / 2)
        x = ceil(n / y)

    elif mode == 'cs':
        x = ceil(n / r)
        y = ceil(n / x)

    return x, y


def splitData(dataURL):
    s = dataURL.split(',')
    return (s[0], s[-1])
