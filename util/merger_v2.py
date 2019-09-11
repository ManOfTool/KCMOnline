import os, sys
from PIL import Image
from math import ceil

'''
merger_v2.py mode src_path saved_name
mode:
    l: linear
    w: wrap
    v: vertical
    h: horizontal
src_path: directory or images
saved_name: saved name with subname

Modify from KCMerge
https://github.com/ManOfTool/KCMerge
'''

def Merging(mode, src_path, saved, rows):

    src_path = appendFile(src_path)

    n_imgs = len(src_path)
    x, y = modeSelect(mode, n_imgs, rows)
    if x == -1:
        return x

    width, height = 0, 0
    x_offset, y_offset = 0, 0

    print('[.]x: {}, y: {}'.format(x, y))

    try:
        images = [Image.open(f) for f in src_path]
    except Exception as e:
        print(e)
        clearFolder(src_path)
        return -1

    # Create image template
    for i in images:
        if i.width > width:
            width = i.width
        if i.height > height:
            height = i.height

    template_img = Image.new('RGB', (width * x, height * y), color=0xffffff)

    # Merging images
    cnt = 0
    for i in range(y):
        for j in range(x):
            template_img.paste(images[cnt], (x_offset + width * j, y_offset + height * i))
            cnt += 1

    template_img.save(saved, 'JPEG', quality=80, optimize=True, Progressive=True)

    print('[+]Image saved to {}'.format(os.path.abspath(saved)))

    # Remove files after done
    clearFolder(src_path)

    return 0

def appendFile(src_path):
    if os.path.isdir(src_path[0]):
        root_path = os.path.abspath(src_path[0])
        src_path = os.listdir(src_path[0])
        src_path = [os.path.join(root_path, src) for src in src_path]

    return src_path

# Determine a mode
def modeSelect(mode, n_imgs, n):
    x, y = 0, 0
    mode = ''.join(sorted(mode))

    if mode == 'hl':
        print('[.]Mode: Horizontal, Linear')
        x = n_imgs
        y = 1

    elif mode == 'hw':
        print('[.]Mode: Horizontal, Wrap')
        x = ceil(n_imgs / 2)
        y = ceil(n_imgs / x)

    elif mode == 'lv':
        print('[.]Mode: Vertical, Linear')
        x = 1
        y = n_imgs

    elif mode == 'vw':
        print('[.]Mode: Vertical, Wrap')
        y = ceil(n_imgs / 2)
        x = ceil(n_imgs / y)

    elif mode == 'cs':
        print('[.]Mode: custom')
        x = ceil(n_imgs / n)
        y = ceil(n_imgs / x)

    else:
        print('[!]Unknow mode')
        print('[!]Your mode: {}'.format(mode))
        x, y = -1, -1

    return x, y

# Remove files in given list
def clearFolder(src_path):
    for f in src_path:
        if os.path.exists(f):
            os.remove(os.path.abspath(f))

if __name__ == "__main__":
    args = sys.argv

    if len(args) < 4:
        print('[!]Missing arguments. Check yourself!')
        exit()

    mode = args[1]
    src_path = args[2:-1]
    saved_name = args[-1]

    Merging(mode, src_path, saved_name)