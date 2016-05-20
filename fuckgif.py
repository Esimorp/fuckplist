import os
from PIL import Image


def fuck_point(point, pix, width, height, color):
    now_image_pixes = [point]
    now_length = len(now_image_pixes)
    pix_map = [[-1 for col in range(height)] for row in range(width)]
    while True:
        for point in now_image_pixes:
            if point[1] > 0:
                up_point = (point[0], point[1] - 1)
                a, r, g, b = pix[up_point[0], up_point[1]]
                if pix_map[up_point[0]][
                    up_point[1]] != 1 and a == color[0] and r == color[1] and g == color[2] and b == color[3]:
                    pix_map[up_point[0]][up_point[1]] = 1
                    now_image_pixes.append(up_point)

            if point[1] < height - 1:
                down_point = (point[0], point[1] + 1)
                print(down_point)
                a, r, g, b = pix[down_point[0], down_point[1]]
                if pix_map[down_point[0]][
                    down_point[1]] != 1 and a == color[0] and r == color[1] and g == color[2] and b == color[3]:
                    pix_map[down_point[0]][down_point[1]] = 1
                    now_image_pixes.append(down_point)

            if point[0] > 0:
                left_point = (point[0] - 1, point[1])
                a, r, g, b = pix[left_point[0], left_point[1]]
                if pix_map[left_point[0]][
                    left_point[1]] != 1 and a == color[0] and r == color[1] and g == color[2] and b == color[3]:
                    pix_map[left_point[0]][left_point[1]] = 1
                    now_image_pixes.append(left_point)

            if point[0] < width - 1:
                right_point = (point[0] + 1, point[1])
                a, r, g, b = pix[right_point[0], right_point[1]]
                if pix_map[right_point[0]][
                    right_point[1]] != 1 and a == color[0] and r == color[1] and g == color[2] and b == color[3]:
                    pix_map[right_point[0]][right_point[1]] = 1
                    now_image_pixes.append(right_point)

        if now_length == len(now_image_pixes):
            break
        else:
            now_length = len(now_image_pixes)
    return now_image_pixes


def fuck_gif(path):
    im = Image.open(path)

    i = 0
    p = im.getpalette()
    try:
        while True:
            if not im.getpalette():
                im.putpalette(p)
            new_frame = Image.new('RGBA', im.size)
            new_frame.paste(im, (0, 0), im.convert('RGBA'))
            pix = new_frame.load()
            width = new_frame.size[0]
            height = new_frame.size[1]
            print(width, height)
            a, r, g, b = pix[0, 0]
            if a != 0:
                for point in fuck_point((0, 0), pix, width, height, (a, r, g, b)):
                    new_frame.putpixel(point, (0, 0, 0, 0))
            a, r, g, b = pix[0, height - 1]
            if a != 0:
                for point in fuck_point((0, height - 1), pix, width, height, (a, r, g, b)):
                    new_frame.putpixel(point, (0, 0, 0, 0))
            a, r, g, b = pix[width - 1, 0]
            if a != 0:
                for point in fuck_point((width - 1, 0), pix, width, height, (a, r, g, b)):
                    new_frame.putpixel(point, (0, 0, 0, 0))
            a, r, g, b = pix[width - 1, height - 1]
            if a != 0:
                for point in fuck_point((width - 1, height - 1), pix, width, height, (a, r, g, b)):
                    new_frame.putpixel(point, (0, 0, 0, 0))

            new_frame.save('%s_%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')
            i += 1
            im.seek(im.tell() + 1)
    except EOFError:
        pass


def main():
    fuck_gif('a13.gif')


if __name__ == "__main__":
    main()
