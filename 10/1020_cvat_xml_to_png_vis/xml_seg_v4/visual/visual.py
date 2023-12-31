# color segment

from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
# from matplotlib import pyplot as plt
# import os

# seg = [[x, y], [x, y], ...]
def seg(img, seg, thickness, color, alpha=None):

    if thickness != -1:
        if alpha is None:
            np_array = np.array(seg, np.int32)

            # seg_on = np.zeros_like(img, np.uint8)
            result = cv2.polylines(img, [np_array], True, color, thickness, lineType=cv2.LINE_AA)
        
        else:
            np_array = np.array(seg, np.int32)

            seg_on = np.zeros_like(img, np.uint8)
            cv2.fillPoly(seg_on, [np_array], color)

            result = img.copy()
            mask = seg_on.astype(bool)
            result[mask] = cv2.addWeighted(img, alpha, seg_on, 1-alpha, 1.0)[mask]

    else:
        if alpha is None:
            np_array = np.array(seg, np.int32)

            # seg_on = np.zeros_like(img, np.uint8)
            result = cv2.fillPoly(img, [np_array], color, lineType=cv2.LINE_AA)
        
        else:
            np_array = np.array(seg, np.int32)

            seg_on = np.zeros_like(img, np.uint8)
            cv2.fillPoly(seg_on, [np_array], color)

            result = img.copy()
            mask = seg_on.astype(bool)
            result[mask] = cv2.addWeighted(img, alpha, seg_on, 1-alpha, 1.0)[mask]

    return result

def bbox(img, tl, br, thickness, color):

    # seg_on = np.zeros_like(img, np.uint8)
    tl = (int(tl[0]), int(tl[1]))
    br = (int(br[0]), int(br[1]))
    result = cv2.rectangle(img, tl, br, color, thickness, lineType=cv2.LINE_AA)
    return result

def point(img, center, radius, thickness, color):

    # seg_on = np.zeros_like(img, np.uint8)
    center = (int(center[0]), int(center[1]))
    result = cv2.circle(img, center, radius, color, thickness, lineType=cv2.LINE_AA)
    return result

def place_image(bg_cv2, img_cv2, org):

    img_pil = Image.fromarray(img_cv2)
    bg_pil = Image.fromarray(bg_cv2)

    bg_pil.paste(img_pil, org)
    result_cv2 = np.array(bg_pil)

    return result_cv2

if __name__ == '__main__':
    img_path = './sample_file/1. 원천데이터/1. 자갈 암석종류 분석 데이터/102-d-028.png'
    raw_seg = [
                {
                    "x": 412.8051384275761,
                    "y": 597.527122752539
                },
                {
                    "x": 412.8051384275761,
                    "y": 587.624317879447
                },
                {
                    "x": 418.31016516793284,
                    "y": 578.2716688326378
                },
                {
                    "x": 423.81519190828953,
                    "y": 571.1196430909603
                },
                {
                    "x": 434.82524538900304,
                    "y": 559.0162149127367
                },
                {
                    "x": 442.5322828255025,
                    "y": 550.2137216922105
                },
                {
                    "x": 455.193844328323,
                    "y": 537.560137687704
                },
                {
                    "x": 467.3049031571078,
                    "y": 526.5570211620462
                },
                {
                    "x": 478.8654593118569,
                    "y": 517.2043721152372
                },
                {
                    "x": 491.5270208146775,
                    "y": 515.5539046363886
                },
                {
                    "x": 516.8501438203185,
                    "y": 504.55078811073076
                },
                {
                    "x": 521.8046678866395,
                    "y": 496.29845071648737
                },
                {
                    "x": 527.860197301032,
                    "y": 490.24673662737564
                },
                {
                    "x": 548.7792989143876,
                    "y": 478.69346427543496
                },
                {
                    "x": 558.137844372994,
                    "y": 474.2922176651719
                },
                {
                    "x": 564.7438764614221,
                    "y": 473.74206183888896
                },
                {
                    "x": 586.7639834228492,
                    "y": 470.9912827074745
                },
                {
                    "x": 604.3800689919907,
                    "y": 456.1370753978365
                },
                {
                    "x": 604.3800689919907,
                    "y": 448.98504965615894
                },
                {
                    "x": 614.2891171246329,
                    "y": 439.08224478306704
                },
                {
                    "x": 639.6122401302738,
                    "y": 429.179439909975
                },
                {
                    "x": 667.1373738320576,
                    "y": 425.87850495227764
                },
                {
                    "x": 672.0918978983786,
                    "y": 428.6292840836921
                },
                {
                    "x": 704.5715556664834,
                    "y": 429.179439909975
                },
                {
                    "x": 714.4806037991256,
                    "y": 432.4803748676723
                },
                {
                    "x": 734.8492027384456,
                    "y": 440.73271226191565
                },
                {
                    "x": 754.116796329694,
                    "y": 445.13395887217877
                },
                {
                    "x": 765.6773524844432,
                    "y": 447.88473800359316
                },
                {
                    "x": 775.5864006170852,
                    "y": 455.0367637452708
                },
                {
                    "x": 776.136903291121,
                    "y": 482.54455505941513
                },
                {
                    "x": 779.439919335335,
                    "y": 490.24673662737564
                },
                {
                    "x": 779.9904220093707,
                    "y": 521.6056187255002
                },
                {
                    "x": 781.6419300314778,
                    "y": 530.9582677723095
                },
                {
                    "x": 781.0914273574421,
                    "y": 556.2654357813223
                },
                {
                    "x": 781.0914273574421,
                    "y": 563.4174615229998
                },
                {
                    "x": 777.2379086391924,
                    "y": 585.4236945743154
                },
                {
                    "x": 786.0459514237631,
                    "y": 605.2293043204994
                },
                {
                    "x": 782.1924327055134,
                    "y": 620.0835116301374
                },
                {
                    "x": 779.9904220093707,
                    "y": 629.4361606769464
                },
                {
                    "x": 777.2379086391924,
                    "y": 653.0928612071107
                },
                {
                    "x": 775.5864006170852,
                    "y": 681.7009641738208
                },
                {
                    "x": 771.7328818988356,
                    "y": 691.6037690469128
                },
                {
                    "x": 770.0813738767285,
                    "y": 706.4579763565508
                },
                {
                    "x": 768.9803685286572,
                    "y": 735.6162351495441
                },
                {
                    "x": 764.5763471363719,
                    "y": 740.56763758609
                },
                {
                    "x": 756.8693096998725,
                    "y": 742.7682608912215
                },
                {
                    "x": 748.0612669153016,
                    "y": 742.2181050649386
                },
                {
                    "x": 743.6572455230163,
                    "y": 747.1695075014848
                },
                {
                    "x": 735.399705412481,
                    "y": 752.6710657643135
                },
                {
                    "x": 718.8846251914109,
                    "y": 752.6710657643135
                },
                {
                    "x": 711.7280904289471,
                    "y": 745.519040022636
                },
                {
                    "x": 693.5615021857699,
                    "y": 737.2667026283927
                },
                {
                    "x": 680.3494380089138,
                    "y": 736.1663909758269
                },
                {
                    "x": 668.2383791801288,
                    "y": 729.0143652341493
                },
                {
                    "x": 652.2738016330943,
                    "y": 720.2118720136231
                },
                {
                    "x": 648.4202829148445,
                    "y": 716.9109370559257
                },
                {
                    "x": 636.3092240860598,
                    "y": 712.5096904456627
                },
                {
                    "x": 633.0062080418458,
                    "y": 708.6585996616825
                },
                {
                    "x": 612.6376091025259,
                    "y": 701.5065739200048
                },
                {
                    "x": 607.6830850362047,
                    "y": 694.9047040046103
                },
                {
                    "x": 595.0215235333842,
                    "y": 685.552054957801
                },
                {
                    "x": 582.3599620305637,
                    "y": 669.5975359955974
                },
                {
                    "x": 548.7792989143876,
                    "y": 652.5427053808278
                },
                {
                    "x": 529.511705323139,
                    "y": 647.5913029442819
                },
                {
                    "x": 526.2086892789249,
                    "y": 650.3420820756962
                },
                {
                    "x": 510.79461440592604,
                    "y": 647.5913029442819
                },
                {
                    "x": 498.13305290310564,
                    "y": 646.490991291716
                },
                {
                    "x": 480.51696733396403,
                    "y": 641.5395888551701
                },
                {
                    "x": 458.49686037253707,
                    "y": 631.6367839820781
                },
                {
                    "x": 441.43127747743114,
                    "y": 621.1838232827031
                },
                {
                    "x": 438.67876410725273,
                    "y": 616.2324208461572
                },
                {
                    "x": 429.3202186486463,
                    "y": 611.2810184096111
                },
                {
                    "x": 424.3656945823252,
                    "y": 604.6791484942164
                }
            ]
    seg = [[float(p['x']), float(p['y'])] for p in raw_seg]
    img_arr = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    result = color_segment(img, seg, (255, 0, 0))

    proceed, encoded_img = cv2.imencode('.png', result)

    if proceed:
        with open('test.png', mode='w+b') as f:
            encoded_img.tofile(f)
