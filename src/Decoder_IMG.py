import PIL.Image
import io
import base64

def convert_to_bytes(file_or_bytes, resize=None):
    
    if isinstance(file_or_bytes, str) and file_or_bytes != "":
        
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except PIL.UnidentifiedImageError:
            return (None, None)
        except Exception:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        img_data = bio.getvalue()
        return (img, img_data)

def update_img(img):
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        img_data = bio.getvalue()
        return img_data
    
def get_bytes(img):
    return update_img(img)