import sys
import numpy as np
from PIL import Image
from dahuffman import HuffmanCodec

def to_bit(tag, data):
    if tag == 'p':
        return (data[0] * (256 ** 2) + data[1] * 256 + data[2]).to_bytes(3, byteorder='big', signed=False)
    elif tag in ('n', 'v', 'd'):
        return (data - 1).to_bytes(1, byteorder='big', signed=False)
    elif tag == 'i':
        return data.to_bytes(1, byteorder='big', signed=False)
    elif tag in ('R', 'C'):
        dr, dg, db = map(int, data)
        return (((dr % 64) << 10) + ((dg % 32) << 5) + (db % 32)).to_bytes(2, byteorder='big', signed=False)
    elif tag in ('r', 'c'):
        dr, dg, db = map(int, data)
        return (((dr % 8) << 5) + ((dg % 8) << 2) + (db % 4)).to_bytes(1, byteorder='big', signed=False)

img_path = sys.argv[1]
img = Image.open(img_path)
img, img.format = img.convert('RGB'), img.format

width, height = img.size
pixels = img.load()

byte = []
hash = {}

y = 0
while y < height:
    x = 0
    while x < width:
        current_pixel = pixels[x, y]

        # Try horizontal run
        run_h = 1
        while x + run_h < width and pixels[x + run_h, y] == current_pixel:
            run_h += 1
            if run_h == 256:
                break
        if run_h > 1:
            byte.append(('p', current_pixel))
            byte.append(('n', run_h - 1))
            x += run_h
            continue

        # Try vertical run
        run_v = 1
        while y + run_v < height and pixels[x, y + run_v] == current_pixel:
            run_v += 1
            if run_v == 256:
                break
        if run_v > 1:
            byte.append(('p', current_pixel))
            byte.append(('v', run_v - 1))
            for i in range(run_v):
                if x == width - 1:
                    x = 0
                    y += 1
                else:
                    x += 1
            continue

        # Try diagonal run
        run_d = 1
        while x + run_d < width and y + run_d < height and pixels[x + run_d, y + run_d] == current_pixel:
            run_d += 1
            if run_d == 256:
                break
        if run_d > 1:
            byte.append(('p', current_pixel))
            byte.append(('d', run_d - 1))
            x += run_d
            y += run_d
            continue

        # Index/hash fallback
        index = (current_pixel[0] * 3 + current_pixel[1] * 5 + current_pixel[2] * 7) % 256
        if current_pixel in hash.values():
            byte.append(('i', index))
        else:
            hash[index] = current_pixel
            byte.append(('p', current_pixel))

        x += 1
    y += 1

tags = [tag for tag, _ in byte]
codec = HuffmanCodec.from_data(tags)
huff_tags = codec.encode(tags)
cdata = [to_bit(tag, data) for tag, data in byte]
tag_size = len(huff_tags)

cmp_img = {
    'type': '_' * (4 - len(img.format)) + img.format,
    'height': height,
    'width': width,
    'tag_size': tag_size,
    'codec_size': len(str(codec.get_code_table())),
    'codec': codec.get_code_table(),
    'tags': huff_tags,
    'data': cdata
}

cmp_path = img_path[:img_path.find('.' + (img.format).lower())] + '_cmp'

with open(cmp_path, 'wb') as new_img:
    new_img.write(cmp_img['type'].encode('ascii'))
    new_img.write(cmp_img['height'].to_bytes(4, byteorder='big', signed=False))
    new_img.write(cmp_img['width'].to_bytes(4, byteorder='big', signed=False))
    new_img.write(cmp_img['tag_size'].to_bytes(4, byteorder='big', signed=False))
    new_img.write(cmp_img['codec_size'].to_bytes(4, byteorder='big', signed=False))
    new_img.write(str(cmp_img['codec']).encode())
    new_img.write(cmp_img['tags'])
    new_img.write(b''.join(cmp_img['data']))

print("Compression completed : ", cmp_path)
