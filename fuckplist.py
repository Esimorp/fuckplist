import sys
from PIL import Image

im = Image.open(sys.argv[1])
pix = im.load()
width = im.size[0]
height = im.size[1]

pix_map = [[-1 for col in range(width)] for row in range(height)]

index = 0
offset_x = 0
offset_y = [0 for x in range(width)]


def find_a_point():
    global offset_x
    for y in range(height):
        for x in range(offset_x, width):
            if y > offset_y[x] or offset_y[x] == 0:
                a, r, g, b = pix[x, y]
                if a != 0:
                    return x, y
        offset_x = 0
    return False


while True:
    point = find_a_point()
    if not point:
        break
    print('find a point', point)
    now_image_pixes = [point]
    now_length = len(now_image_pixes)
    while True:
        for point in now_image_pixes:
            if point[1] > 0:
                up_point = (point[0], point[1] - 1)
                a, r, g, b = pix[up_point[0], up_point[1]]
                if pix_map[up_point[0]][up_point[1]] != index and a != 0:
                    pix_map[up_point[0]][up_point[1]] = index
                    now_image_pixes.append(up_point)

            if point[1] < height - 1:
                down_point = (point[0], point[1] + 1)
                a, r, g, b = pix[down_point[0], down_point[1]]
                if pix_map[down_point[0]][down_point[1]] != index and a != 0:
                    pix_map[down_point[0]][down_point[1]] = index
                    now_image_pixes.append(down_point)

            if point[0] > 0:
                left_point = (point[0] - 1, point[1])
                a, r, g, b = pix[left_point[0], left_point[1]]
                if pix_map[left_point[0]][left_point[1]] != index and a != 0:
                    pix_map[left_point[0]][left_point[1]] = index
                    now_image_pixes.append(left_point)

            if point[0] < width - 1:
                right_point = (point[0] + 1, point[1])
                a, r, g, b = pix[right_point[0], right_point[1]]
                if pix_map[right_point[0]][right_point[1]] != index and a != 0:
                    pix_map[right_point[0]][right_point[1]] = index
                    now_image_pixes.append(right_point)

        if now_length == len(now_image_pixes):
            break
        else:
            now_length = len(now_image_pixes)

    start_x = point[0]
    start_y = point[1]
    end_x = 0
    end_y = 0
    for x in range(width):
        for y in range(height):
            if index == pix_map[x][y]:
                start_x = x if x < start_x else start_x
                end_x = x if x > end_x else end_x
                start_y = y if y < start_y else start_y
                end_y = y if y > end_y else end_y

    print('crop', start_x, start_y, end_x, end_y)
    box = (start_x, start_y, end_x, end_y)
    region = im.crop(box)
    region.save("fuck" + str(index) + ".png")
    for x in range(start_x, end_x + 2):
        offset_y[x] = end_y
    offset_x = end_x + 1
    index += 1
