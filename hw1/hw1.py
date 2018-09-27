from PIL import Image

def upside_down(pic):
    width, height = pic.size
    pic_ud = Image.new(pic.mode, pic.size)
    pic_load = pic.load()
    pic_ud_load = pic_ud.load()
    for i in range(0, height):
        for j in range(0, width):
            pic_ud_load[i, j] = pic_load[i, height-1-j]
    try:
        pic_ud.save('./result/upside_down.bmp')
    except:
        print('Error! 請確認含 hw1.py 的目錄下存在 result 目錄!')
        exit()

def right_side_left(pic):
    width, height = pic.size
    pic_rsl = Image.new(pic.mode, pic.size)
    pic_load = pic.load()
    pic_rsl_load = pic_rsl.load()
    for i in range(0, height):
        for j in range(0, width):
            pic_rsl_load[i, j] = pic_load[width-1-i, j]
    try:
        pic_rsl.save('./result/right_side_left.bmp')
    except:
        print('Error! 請確認含 hw1.py 的目錄下存在 result 目錄!')
        exit()

def diagonally_mirrored(pic):
    width, height = pic.size
    pic_dm = Image.new(pic.mode, pic.size)
    pic_load = pic.load()
    pic_dm_load = pic_dm.load()
    for i in range(0, height):
        for j in range(0, width):
            pic_dm_load[i, j] = pic_load[j, i]
    try:
        pic_dm.save('./result/diagonally_mirrored.bmp')
    except:
        print('Error! 請確認含 hw1.py 的目錄下存在 result 目錄!')
        exit()

if(__name__ == "__main__"):
    try:
        wife = Image.open('lena.bmp')
    except:
        print("Error! 請確認含 hw1.py 的目錄下存在 lena.bmp !")
        exit()
    upside_down(wife)
    right_side_left(wife)
    diagonally_mirrored(wife)
