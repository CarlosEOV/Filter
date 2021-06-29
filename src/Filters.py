from PySimpleGUI.PySimpleGUI import Sizer
from Decoder_IMG import update_img
from PIL import Image, ImageFont, ImageDraw

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

def blend(image, image2, alpha):
    pixels = image.load()
    pixels_2 = image2.load()

    w1 = image.size[0]
    w2 = image2.size[0]
    h1 = image.size[1]
    h2 = image2.size[1]

    w = w1 if w1 < w2 else w2
    h = h1 if h1 < h2 else h2
    
    for i in range(w):
        for j in range(h):
            pixel = pixels[i, j]
            pixel2 = pixels_2[i, j]
            if pixel2[3] != 0:
                pixels[i, j] = (int((pixel[0] * alpha) + (pixel2[0] * (1.0 - alpha))), int((pixel[1] * alpha) + (pixel2[1] * (1.0 - alpha))), int((pixel[2] * alpha) + (pixel2[2] * (1.0 - alpha))), 255)
    return update_img(image)

def watermark(image, watermark, position, alpha):
    og_size = (image.size[0], image.size[1])
    watermark_img = Image.new('RGBA', og_size, (255,255,255,0))
    d = ImageDraw.Draw(watermark_img)
    fnt_size = int(og_size[1] * 0.1)
    fnt = ImageFont.truetype("/System/Library/Fonts/arial.ttf", fnt_size)
    if len(watermark) > 60:
        watermark = watermark[:60]

    h = int(og_size[0] * 0.33)
    if position[0] == 0:
        h = int(og_size[0] * 0.05)
    elif position[0] == 2:
        h = int(og_size[0] * 0.66)
    
    v = int(og_size[1] * 0.33)
    if position[1] == 0:
        v = int(og_size[1] * 0.05)
    elif position[1] == 2:
        v = int(og_size[1] * 0.66)         
    
    d.text((h,v), watermark, font=fnt, fill=(0, 0, 0, 255))

    return blend(image, watermark_img, alpha)

def mosaic_img_bw(image, img_grid, w, h):
    num_shades = 32
    shades = create_shades(img_grid, (w, h), num_shades)
    pixels = image.load()

    for j in range(0, image.size[1], h):
        for i in range(0, image.size[0], w):
            average_grid(pixels, i, j, w, h, (image.size[0], image.size[1]), False, True, False, shades)
    
    return update_img(image)

def semitone(image, set_idx, w, h):
    shades = load_shades(set_idx, (w, h))
    pixels = image.load()

    for j in range(0, image.size[1], h):
        for i in range(0, image.size[0], w):
            average_semitone(pixels, i, j, w, h, (image.size[0], image.size[1]), shades)

    return update_img(image)
    
def load_shades(set_idx, size):
    shades = []
    set_img = "img/"
    length = 10
    img_name = ""
    if(set_idx == 0):
        set_img += "a/"
        img_name += "a"
    elif(set_idx == 1):
        set_img += "b/"
        img_name += "b"
    else:
        set_img += "c/" 
        img_name += "c"
        length = 5
    
    for image in range(0, length):
        shade = Image.open(set_img + img_name + str(image) + ".png")
        shades.append(shade.resize(size))

    return shades

def average_semitone(pixels, origin_x, origin_y, x, y, img_size, shades):
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
        
        gray = int((average[0] + average[1] + average[2]) / 3)
        step = int(256 / len(shades))
        shade_idx = 0 
        for idx in range(0, 256, step):
            if idx <= gray <= (idx + step - 1):
                if shade_idx >= len(shades):
                    shade_idx = len(shades) - 1
                shade = shades[shade_idx].copy()
                break
            shade_idx += 1

        pixels_sh = shade.load()
        ri_x = -1        
        for i in range(origin_x, w):
            ri_x += 1
            ri_y = -1
            for j in range(origin_y, h):
                ri_y += 1
                if ri_y < shade.size[1] and ri_x < shade.size[0]:
                    pixel_sh: tuple = pixels_sh[ri_x, ri_y]
                    pixels[i, j] = (pixel_sh[0], pixel_sh[1], pixel_sh[2], 255)

def mosaic_true_colors(image, img_grid, w, h):
    pixels = image.load()
    img_grid = img_grid.resize(size=(w, h))
    for j in range(0, image.size[1], h):
        for i in range(0, image.size[0], w):
            average_grid(pixels, i, j, w, h, (image.size[0], image.size[1]), is_for_txt=False, rep_img_bnw=False, rep_img=True, shades_or_img=img_grid)
    
    return update_img(image)

def create_shades(image, size, num_shades):
    shades = []
    image = image.resize(size=size)
    grayscale(image)
    
    jump = int(256 / num_shades)
    for bright in range(-127, 127, jump):
        new_img = image.copy()
        brightness(new_img, bright)
        shades.append(new_img)

    return shades

def mosaic(image, w, h, method_id=0, sign='CARLOS'):
    pixels = image.load()
    size = (image.size[0], image.size[1])
    sign_len = len(sign)
    if sign_len > 20:
        sign = sign[:20]
        sign_len = 20
    sign_idx = 0
    d = ImageDraw.Draw(image)
    fnt = ImageFont.truetype("/System/Library/Fonts/arial.ttf", h)
    lasvb = ImageFont.truetype("fonts/Lasvbld.ttf", h) 
    lasvw = ImageFont.truetype("fonts/Lasvwd.ttf", h)
    plcrds = ImageFont.truetype("fonts/PLAYCRDS.TTF", h+5)

    for j in range(0, size[1], h):
        for i in range(0, size[0], w):    
            if method_id == 0: 
                average_grid(pixels, i, j, w, h, size)

            if method_id == 1 or method_id == 9:
                average = average_grid(pixels, i, j, w, h, size, is_for_txt=True)
                if method_id == 9:
                    d.text((i,j), sign[sign_idx], font=fnt, fill=(average[0], average[1], average[2], 255))
                    sign_idx = ( sign_idx + 1 ) % sign_len
                else:
                    d.text((i,j), "M", font=fnt, fill=(average[0], average[1], average[2], 255))


            if method_id == 2:
                average = average_grid(pixels, i, j, w, h, size, is_for_txt=True)
                gray = int((average[0] + average[1] + average[2]) / 3)
                d.text((i,j), "M", font=fnt, fill=(gray, gray, gray, 255))
            
            if method_id == 3 or method_id == 4 or method_id == 5:
                fill_color = (0,0,0,255)
                average = average_grid(pixels, i, j, w, h, size, is_for_txt=True)
                gray = int((average[0] + average[1] + average[2]) / 3)
                if method_id == 4:
                    fill_color = (average[0], average[1], average[2], 255)
                if method_id == 5:
                    fill_color = (gray, gray, gray, 255)
                if  0 <= gray <= 15:
                    d.text((i,j), "M", font=fnt, fill=fill_color)
                if  16 <= gray <= 31:
                    d.text((i,j), "N", font=fnt, fill=fill_color)
                if  32 <= gray <= 47:
                    d.text((i,j), "H", font=fnt, fill=fill_color)
                if  48 <= gray <= 63:
                    d.text((i,j), "#", font=fnt, fill=fill_color)
                if  64 <= gray <= 79:
                    d.text((i,j), "Q", font=fnt, fill=fill_color)
                if  80 <= gray <= 95:
                    d.text((i,j), "U", font=fnt, fill=fill_color)
                if  96 <= gray <= 111:
                    d.text((i,j), "A", font=fnt, fill=fill_color)
                if  112 <= gray <= 127:
                    d.text((i,j), "D", font=fnt, fill=fill_color)
                if  128 <= gray <= 143:
                    d.text((i,j), "O", font=fnt, fill=fill_color)
                if  144 <= gray <= 159:
                    d.text((i,j), "Y", font=fnt, fill=fill_color)
                if  160 <= gray <= 175:
                    d.text((i,j), "2", font=fnt, fill=fill_color)
                if  176 <= gray <= 191:
                    d.text((i,j), "$", font=fnt, fill=fill_color)
                if  192 <= gray <= 209:
                    d.text((i,j), "%", font=fnt, fill=fill_color)
                if  210 <= gray <= 225:
                    d.text((i,j), "+", font=fnt, fill=fill_color)
                if  226 <= gray <= 239:
                    d.text((i,j), ".", font=fnt, fill=fill_color)
                if  240 <= gray <= 255:
                    d.text((i,j), " ", font=fnt, fill=fill_color)
            
            if method_id == 6:
                average = average_grid(pixels, i, j, w, h, size, is_for_txt=True)
                gray = int((average[0] + average[1] + average[2]) / 3)
                
                if  0 <= gray <= 25:
                    d.text((i,j), "0", font=lasvb, fill=(0,0,0,255))
                if  26 <= gray <= 50:
                    d.text((i,j), "1", font=lasvb, fill=(0,0,0,255))
                if  51 <= gray <= 75:
                    d.text((i,j), "2", font=lasvb, fill=(0,0,0,255))
                if  76 <= gray <= 100:
                    d.text((i,j), "3", font=lasvb, fill=(0,0,0,255))
                if  101 <= gray <= 125:
                    d.text((i,j), "4", font=lasvb, fill=(0,0,0,255))
                if  126 <= gray <= 150:
                    d.text((i,j), "5", font=lasvb, fill=(0,0,0,255))
                if  151 <= gray <= 175:
                    d.text((i,j), "6", font=lasvb, fill=(0,0,0,255))
                if  176 <= gray <= 200:
                    d.text((i,j), "7", font=lasvb, fill=(0,0,0,255))
                if  201 <= gray <= 225:
                    d.text((i,j), "8", font=lasvb, fill=(0,0,0,255))
                if  226 <= gray <= 255:
                    d.text((i,j), "9", font=lasvb, fill=(0,0,0,255))
            
            if method_id == 7:
                average = average_grid(pixels, i, j, w, h, size, is_for_txt=True)
                gray = int((average[0] + average[1] + average[2]) / 3)
                
                if  0 <= gray <= 25:
                    d.text((i,j), "9", font=lasvw, fill=(0,0,0,255))
                if  26 <= gray <= 50:
                    d.text((i,j), "8", font=lasvw, fill=(0,0,0,255))
                if  51 <= gray <= 75:
                    d.text((i,j), "7", font=lasvw, fill=(0,0,0,255))
                if  76 <= gray <= 100:
                    d.text((i,j), "6", font=lasvw, fill=(0,0,0,255))
                if  101 <= gray <= 125:
                    d.text((i,j), "5", font=lasvw, fill=(0,0,0,255))
                if  126 <= gray <= 150:
                    d.text((i,j), "4", font=lasvw, fill=(0,0,0,255))
                if  151 <= gray <= 175:
                    d.text((i,j), "3", font=lasvw, fill=(0,0,0,255))
                if  176 <= gray <= 200:
                    d.text((i,j), "2", font=lasvw, fill=(0,0,0,255))
                if  201 <= gray <= 225:
                    d.text((i,j), "1", font=lasvw, fill=(0,0,0,255))
                if  226 <= gray <= 255:
                    d.text((i,j), "0", font=lasvw, fill=(0,0,0,255))
            
            if method_id == 8:
                average = average_grid(pixels, i, j, w, h, size, is_for_txt=True)
                gray = int((average[0] + average[1] + average[2]) / 3)
                
                if  0 <= gray <= 23:
                    d.text((i,j), "k", font=plcrds, fill=(0,0,0,255))
                if  24 <= gray <= 46:
                    d.text((i,j), "j", font=plcrds, fill=(0,0,0,255))
                if  47 <= gray <= 69:
                    d.text((i,j), "i", font=plcrds, fill=(0,0,0,255))
                if  70 <= gray <= 92:
                    d.text((i,j), "h", font=plcrds, fill=(0,0,0,255))
                if  93 <= gray <= 115:
                    d.text((i,j), "g", font=plcrds, fill=(0,0,0,255))
                if  116 <= gray <= 138:
                    d.text((i,j), "f", font=plcrds, fill=(0,0,0,255))
                if  139 <= gray <= 161:
                    d.text((i,j), "e", font=plcrds, fill=(0,0,0,255))
                if  162 <= gray <= 184:
                    d.text((i,j), "d", font=plcrds, fill=(0,0,0,255))
                if  185 <= gray <= 207:
                    d.text((i,j), "c", font=plcrds, fill=(0,0,0,255))
                if  208 <= gray <= 230:
                    d.text((i,j), "b", font=plcrds, fill=(0,0,0,255))
                if  231 <= gray <= 255:
                    d.text((i,j), "a", font=plcrds, fill=(0,0,0,255))

    return update_img(image)

def average_grid(pixels, origin_x, origin_y, x, y, img_size, is_for_txt=False, rep_img_bnw=False, rep_img=False, shades_or_img=None):
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
        
        if rep_img_bnw:
            
            gray = int((average[0] + average[1] + average[2]) / 3)
            shade_idx = 0
            shade = None

            for idx in range(0, 256, 8):
                if idx <= gray <= (idx + 7):
                    shade = shades_or_img[shade_idx].copy()
                    break
                shade_idx += 1
            
            pixels_sh = shade.load()
            
            ri_x = -1        
            for i in range(origin_x, w):
                ri_x += 1
                ri_y = -1
                for j in range(origin_y, h):
                    ri_y += 1
                    if ri_y <= shade.size[1] - 1 and ri_x <= shade.size[0] - 1:
                        pixel_sh = pixels_sh[ri_x, ri_y]
                        pixels[i, j] = (pixel_sh[0], pixel_sh[1], pixel_sh[2], 255)
                    
        elif rep_img:
            img_grid = shades_or_img.copy()
            
            RGB_components(img_grid, average[0], average[1], average[2])
            pixels_grid = img_grid.load()
            
            ri_x = -1
            for i in range(origin_x, w):
                ri_x += 1
                ri_y = -1
                for j in range(origin_y, h):
                    ri_y += 1
                    if ri_y <= img_grid.size[1] - 1 and ri_x <= img_grid.size[0] - 1:
                        pixel_grid = pixels_grid[ri_x, ri_y]
                        pixels[i, j] = (pixel_grid[0], pixel_grid[1], pixel_grid[2], 255)

        else:
            for i in range(origin_x, w):
                for j in range(origin_y, h):
                    pixel = pixels[i, j]
                    pixels[i, j] = (average[0], average[1], average[2], 255)
                    if is_for_txt:
                        pixels[i, j] = (255, 255, 255, 255)
    return average

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
            pixels[i, j] = (clamp(r & pixel[0], 0, 255), clamp(g & pixel[1], 0, 255), clamp(b & pixel[0], 0, 255), 255)
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

def find_edges(image):
    find_edges_matrix = [
        [-1,  0,  0,  0,  0],
        [0, -2,  0,  0,  0],
        [0,  0,  6,  0,  0],
        [0,  0,  0, -2,  0],
        [0,  0,  0,  0, -1]
    ]

    find_edges_w = 5
    find_edges_h = 5
    factor = 1.0
    bias = 0.0

    return convolution(image, find_edges_matrix, find_edges_w, find_edges_h, factor, bias)

def sharpen(image):
    sharpen_matrix = [
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ]

    sharpen_w = 3 
    sharpen_h = 3
    factor = 1.0
    bias = 0.0

    return convolution(image, sharpen_matrix, sharpen_w, sharpen_h, factor, bias)

def emboss(image):
    emboss_matrix = [
        [-1, -1, -1, -1, 0],
        [-1, -1, -1, 0, 1],
        [-1, -1, 0, 1, 1],
        [-1, 0, 1, 1, 1],
        [0, 1, 1, 1, 1]
    ]

    emboss_w = 5
    emboss_h = 5
    factor = 1.0
    bias = 128.0

    return convolution(image, emboss_matrix, emboss_w, emboss_h, factor, bias)