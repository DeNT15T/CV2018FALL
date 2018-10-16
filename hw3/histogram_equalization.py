from PIL import Image
import matplotlib.pyplot as plt
def div3(pic):
    width, height = pic.size
    pic_div3 = Image.new(pic.mode, pic.size)
    pic_load = pic.load()
    pic_div3_load = pic_div3.load()
    for i in range(0, height):
        for j in range(0, width):
            pic_div3_load[i, j] = int(pic_load[i, j]/3)
    pic_div3.show()
    return pic_div3

def histogram(pic):
    width, height = pic.size
    pic_load = pic.load()
    log = []
    for I in range(0, height):
        for J in range(0, width):
            log.append(pic_load[I, J])
    return log

def equalization(pic):
    width, height = pic.size
    pic_he = Image.new(pic.mode, pic.size)
    pic_load = pic.load()
    pic_he_load = pic_he.load()
    old_intensity = [0 for i in range(256)]
    total_num = width * height
    intensity_num = [0 for i in range(256)]
    for I in range(0, width):
        for J in range(0, height):
            old_intensity[ pic_load[I, J] ] += 1

    intensity_num[0]=old_intensity[0]
    for I in range(1, 256):
        intensity_num[I] = intensity_num[I-1] + old_intensity[I]

    for I in range(0, height):
        for J in range(0, width):
            pic_he_load[I, J] = round(255*intensity_num[ pic_load[I, J] ]/total_num)

    return pic_he

if __name__ == '__main__':
    wife = Image.open('lena.bmp')
#    pic_div3 = div3(wife)
    pic_he = equalization(wife)
    pic_he_hist = histogram(pic_he)
    plt.hist(pic_he_hist , bins = [i for i in range(256)])
    try:
        plt.savefig('result/histogram.png')
        pic_he.save('./result/pic_he.bmp')
    except:
        print('Error! 請確認含 histogram.py 的目錄下存在 result 目錄!')
    pic_he.show()
    plt.show()
