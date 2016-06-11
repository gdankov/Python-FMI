from collections import defaultdict


def grey_out_pixel(pixel):
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2]

    grey = int(red * 0.2126 + green * 0.7152 + blue * 0.0722)
    return (grey, grey, grey)


def greyscale(func):
    def to_greyscale(*arguments):
        picture = arguments[0]
        greyed_out_picture = [[grey_out_pixel(pixel) for pixel in row]
                              for row in picture]

        if len(arguments) == 1:
            return func(greyed_out_picture)
        else:
            coef = arguments[1]
            return func(greyed_out_picture, coef)

    return to_greyscale


def transpose(picture):
    return [[row[i] for row in picture] for i in range(len(picture[0]))]


@greyscale
def rotate_left(picture):
    for row in picture:
        row.reverse()

    return transpose(picture)


@greyscale
def rotate_right(picture):
    transposed = transpose(picture)

    for row in transposed:
        row.reverse()

    return transposed


def invert_pixel(pixel):
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]

    new_pixel = (255 - r, 255 - g, 255 - b)
    return new_pixel


@greyscale
def invert(picture):
    reversed_picture = []

    for row in picture:
        reversed_picture.append(list(map(invert_pixel, row)))

    return reversed_picture


def lighten_pixel(pixel, coef):
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]

    new_r = int(r + coef * (255 - r))
    new_g = int(g + coef * (255 - g))
    new_b = int(b + coef * (255 - b))

    new_pixel = (new_r, new_g, new_b)
    return new_pixel


@greyscale
def lighten(picture, coef):
    lightened_picture = [[lighten_pixel(pixel, coef)
                          for pixel in row]for row in picture]

    return lightened_picture


def darken_pixel(pixel, coef):
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]

    new_r = int(r - coef * (r - 0))
    new_g = int(g - coef * (g - 0))
    new_b = int(b - coef * (b - 0))

    new_pixel = (new_r, new_g, new_b)
    return new_pixel


@greyscale
def darken(picture, coef):
    darkened_picture = [[darken_pixel(pixel, coef)
                         for pixel in row]for row in picture]

    return darkened_picture


def update_pixel_info(color, values, pixel):
    pixel_color = 0

    if color is 'red':
        pixel_color = pixel[0]
    elif color is 'green':
        pixel_color = pixel[1]
    else:
        pixel_color = pixel[2]

    values[pixel_color] += 1


def create_histogram(picture):
    histogram = {'red': defaultdict(int),
                 'green': defaultdict(int),
                 'blue': defaultdict(int)
                 }

    for row in picture:
        for pixel in row:
            update_pixel_info('red', histogram['red'], pixel)
            update_pixel_info('green', histogram['green'], pixel)
            update_pixel_info('blue', histogram['blue'], pixel)

    return histogram
