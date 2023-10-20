# color segment

import numpy as np
import cv2
# from matplotlib import pyplot as plt
from PIL import ImageFont, ImageDraw, Image

# seg = [[x, y], [x, y], ...]
def label(img, text, size, color, org, alpha):


    font = ImageFont.truetype('malgunbd.ttf', size)

    # labeling
    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)

    # size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 20, 10)
    text_bbox = draw.textbbox((0, 0), text, font=font)

    size = (int((text_bbox[2] - text_bbox[0])),
            int((text_bbox[3] - text_bbox[1]) * 1.5))
    if org[0] < 0:
        org = (0, org[1])
    if org[1] < 0:
        org = (org[0], 0)

    width, height = pil_img.size
    if org[0] + size[0] > width:
        org = (width - size[0], org[1])
    if org[1] + size[1] > height:
        org = (org[0], height - size[1])

    top_left = (int(org[0]), int(org[1]))
    bottom_right = (int(org[0] + size[0]), int(org[1] + size[1]))

    sub_img = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) *255
    result = cv2.addWeighted(sub_img, 1-alpha, white_rect, alpha, 1.0)

    img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = result

    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)

    draw.text(top_left, text, color, font=font)
    result = np.array(img)

    return result

def gen_newline(line, width):
    length = width
    if len(line) > length:
        return_line = ''
        while line:
            try:
                return_line = return_line + line[:length] + '\n'
                line = line[length:]
            except:
                return_line = return_line + line
                line = ''
    
        return return_line

    return line

def gen_paragraph(line_list, width):
    
    return_str = ''
    for line in line_list:
        return_str += gen_newline(line, width) + '\n'

    return return_str

def paragraph(img_cv2, line_list, size, color, org, width):

    font = ImageFont.truetype('malgunbd.ttf', size)

    img_pil = Image.fromarray(img_cv2)
    img_draw = ImageDraw.Draw(img_pil)

    img_draw.text(org, gen_paragraph(line_list, width), color, font=font)

    img_cv2 = np.array(img_pil)

    return img_cv2

if __name__ == '__main__':
    img_path = './sample_file/1. 원천데이터/2. 편장석 비율 비 분석 데이터/101-fe-002.png'
    
    img_arr = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    result = label(img, "good")

    plt.imshow(result)
    plt.show()