from PIL import Image
import matplotlib.pyplot as plt

def histogram(pic):
    width, height = pic.size
    pic_load = pic.load()
    log = []
    for I in range(512):
        for J in range(512):
            log.append(pic_load[I, J])
    return log


if __name__ == '__main__':
    wife = Image.open('lena.bmp')
    log = histogram(wife)
    plt.hist(log, bins = [i for i in range(256)])
    try:
        plt.savefig('result/histogram.png')
    except:
        print('Error! 請確認含 histogram.py 的目錄下存在 result 目錄!')
    plt.show()
