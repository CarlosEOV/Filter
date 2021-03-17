from Decoder_IMG import update_img

def average_grayscale(image):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            gray = int((pixel[0] + pixel[1] + pixel[2] ) / 3)
            pixels[i, j] = (gray, gray, gray, 255)
    return update_img(image)

def grayscale(image):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            gray = int((pixel[0] * 0.3) + (pixel[1] * 0.59) + (pixel[2] * 0.11))
            pixels[i, j] = (gray, gray, gray, 255)
    return update_img(image)

def luma_grayscale(image):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            gray = int((pixel[0] * 0.2126) + (pixel[1] * 0.7152) + (pixel[2] * 0.0722))
            pixels[i, j] = (gray, gray, gray, 255)
    return update_img(image)

def max_min_grayscale(image):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            gray = int((max(max(pixel[0], pixel[1]), pixel[2]) 
                        + min(min(pixel[0], pixel[1]), pixel[2])) / 2)
            pixels[i, j] = (gray, gray, gray, 255)
    return update_img(image)  

def max_grayscale(image):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            gray = max(max(pixel[0], pixel[1]), pixel[2]) 
            pixels[i, j] = (gray, gray, gray, 255)
    return update_img(image)

def min_grayscale(image):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            gray = min(min(pixel[0], pixel[1]), pixel[2]) 
            pixels[i, j] = (gray, gray, gray, 255)
    return update_img(image)

def red_grayscale(image):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            gray = pixel[0]
            pixels[i, j] = (gray, gray, gray, 255)
    return update_img(image)

def green_grayscale(image):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            gray = pixel[1]
            pixels[i, j] = (gray, gray, gray, 255)
    return update_img(image)

def blue_grayscale(image):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            gray = pixel[2]
            pixels[i, j] = (gray, gray, gray, 255)
    return update_img(image)

def shades_of_grayscale(image, number_of_shades = 5):
    pixels = image.load()
    ConversionFactor = 255 / (number_of_shades - 1)
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            AverageValue = (pixel[0] + pixel[1] + pixel[2] ) / 3
            gray = int((AverageValue / ConversionFactor) + 0.5) * int(ConversionFactor)
            pixels[i, j] = (gray, gray, gray, 255)
    return update_img(image)

def brightness(image, brightness=0):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            pixels[i, j] = (clamp(pixel[0] + brightness, 0 , 255), clamp(pixel[1] + brightness, 0 , 255), clamp(pixel[2] + brightness, 0 , 255), 255)
    return update_img(image)

def mosaic(image, w, h):
    pixels = image.load()
    size = (image.size[0], image.size[1])

    for i in range(0, size[0], w):
        for j in range(0, size[1], h):
            average_grid(pixels, i, j, w, h, size)
    
    return update_img(image)

def average_grid(pixels, origin_x, origin_y, x, y, img_size):
    w = origin_x + x
    h = origin_y + y
    if w > img_size[0]: w = img_size[0]
    if h > img_size[1]: h = img_size[1]
    average = [0, 0, 0]
    total = 0
    
    for i in range(origin_x, w):
        for j in range(origin_y, h):
            total += 1
            pixel = pixels[i, j]
            average[0] += pixel[0] 
            average[1] += pixel[1] 
            average[2] += pixel[2]
            
    if total != 0:
        for idx in range(3):
            average[idx] = int(average[idx] / total)

        for i in range(origin_x, w):
            for j in range(origin_y, h):
                pixel = pixels[i, j]
                pixels[i, j] = (average[0], average[1], average[2], 255)
    
def clamp(x, minimum, maximum, factor=1, bias=0):
    return max(minimum, min(factor * x + bias, maximum))

def high_contrast(image, inverted=False):
    pixels = image.load()
    white = 255
    black = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            gray = int((pixel[0] * 0.3) + (pixel[1] * 0.59) + (pixel[2] * 0.11))
            if inverted:
                color = white if gray < 127 else black
            else:
                color = white if gray > 127 else black
            pixels[i, j] = (color, color, color, 255)
    return update_img(image)

def RGB_components(image, r, g, b):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[i, j]
            pixels[i, j] = (r and pixel[0], g and pixel[1], b and pixel[0], 255)
    
    return update_img(image)

def convolution(image, filter_matrix, filter_width, filter_height, factor, bias):
    img_copy = image.copy()
    pixels = img_copy.load()
    og_pixels = image.load()
    w = image.size[0]
    h = image.size[1]
    for i in range(w):
        for j in range(h):
            red = 0
            green = 0
            blue = 0
            imageX = 0
            imageY = 0
            for m in range(filter_height):
                for n in range(filter_width):
                    imageX = (i - filter_width / 2 + n + w) % w
                    imageY = (j - filter_height / 2 + m + h) % h
                    pixel = pixels[imageX , imageY]
                    red += pixel[0] * filter_matrix[m][n]
                    green += pixel[1] * filter_matrix[m][n]
                    blue += pixel[2] * filter_matrix[m][n]
            
            og_pixels[i, j] = (int(clamp(red, 0, 255, factor, bias)), 
                            int(clamp(green, 0, 255, factor, bias)), 
                            int(clamp(blue, 0, 255, factor, bias)), 
                            255)

    return update_img(image)

def blur(image, intensity=0):
    
    blur_matrix_1 = [
        [0.0, 0.2, 0.0],
        [0.2, 0.2, 0.2],
        [0.0, 0.2, 0.0]
    ]

    blur_width_1 = 3
    blur_height_1 = 3
    factor_1 = 1.0
    bias_1 = 0.0

    blur_matrix_2 = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
    ]

    blur_width_2 = 5
    blur_height_2 = 5
    factor_2 = 1.0 / 13.0
    bias_2 = 0.0

    if intensity == 0:
        return convolution(image, blur_matrix_1, blur_width_1, blur_height_1, factor_1, bias_1)
    else:
        return convolution(image, blur_matrix_2, blur_width_2, blur_height_2, factor_2, bias_2)

def motion_blur(image):
    motion_blur_matrix = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]

    motion_blur_w = 9
    motion_blur_h = 9
    factor = 1.0 / 9.0
    bias = 0.0

    return convolution(image, motion_blur_matrix, motion_blur_w, motion_blur_h, factor, bias)

