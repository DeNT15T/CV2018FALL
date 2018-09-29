from PIL import Image


def binarize(pic, T):
    width, height = pic.size
    pic_binarize = Image.new(pic.mode, pic.size)
    pic_load = pic.load()
    pic_binarize_load = pic_binarize.load()
    for i in range(0, height):
        for j in range(0, width):
            if(pic_load[i, j]>=T):
                pic_binarize_load[i, j]=255
            else:
                pic_binarize_load[i, j]=0
    return pic_binarize

if(__name__=='__main__'):
    wife = Image.open('lena.bmp')
    pic_binarize = binarize(wife, 128)
    pic_binarize.show()
    try:
        pic_binarize.save('./result/binarize.bmp')
    except:
        print('Error! 請確認含 binarize.py 的目錄下存在 result 目錄!')
        exit()
