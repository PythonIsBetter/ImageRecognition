from PIL import Image
from PIL import ImageEnhance
import pytesseract
import cv2 as cv


def way_1(path, lan):
    text = pytesseract.image_to_string(Image.open(path), lang=lan)
    print('-----------------------WAY 1---------------------------\n')
    print(text)
    print('--------------------------------------------------\n\n\n')


# 灰度处理
def way_2(path, lan):
    img = Image.open(path)
    img = img.convert('RGB')  # 这里也可以尝试使用L
    enhancer = ImageEnhance.Color(img)
    enhancer = enhancer.enhance(0)
    enhancer = ImageEnhance.Brightness(enhancer)
    enhancer = enhancer.enhance(2)
    enhancer = ImageEnhance.Contrast(enhancer)
    enhancer = enhancer.enhance(8)
    enhancer = ImageEnhance.Sharpness(enhancer)
    img = enhancer.enhance(20)
    text = pytesseract.image_to_string(img, lang=lan)
    print('-----------------------WAY 2---------------------------\n')
    print(text)
    print('--------------------------------------------------\n\n\n')


# 识别前处理
# 图片二值化
def way_3(path, lan):
    img = Image.open(path)
    # 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    Img = img.convert('L')

    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = 200

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    # 图片二值化
    photo = Img.point(table, '1')
    # photo.save("test2.png")
    # # 识别图片内容
    # img_path = 'test2.png'
    text = pytesseract.image_to_string(photo, lang=lan)
    print('-----------------------WAY 3---------------------------\n')
    print(text)
    print('--------------------------------------------------\n\n\n')


# 用了opencv
def way_4(path, lan):
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    # 此处可根据图像效果进行相应的形态学处理，再进行识别，提升准确率
    cv.bitwise_not(binary, binary)

    textImg = Image.fromarray(binary)
    text = pytesseract.image_to_string(textImg, lang=lan)
    print('-----------------------WAY 4---------------------------\n')
    print(text)
    print('--------------------------------------------------\n\n\n')


def run(path, lan):
    way_1(path, lan)
    way_2(path, lan)
    way_3(path, lan)
    way_4(path, lan)


run('img/car.png', 'chi_sim+jpn+eng+kor')
