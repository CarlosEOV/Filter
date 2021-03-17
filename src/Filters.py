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
    
def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

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



