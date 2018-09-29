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

def ComponentInitial(pic):
    # 初始化，若顏色超過閥值，即標記label，並使label遞增
    pic_load = pic.load()
    init_component = [[0 for J in range(512)] for I in range(512)]
    label = 1
    for I in range(512):
        for J in range(512):
            if(pic_load[I, J] >=128):
                init_component[J][I] = label
                label += 1
    return init_component

def ComponentSort(init_component):
    # 1.整理各component的label
    # 2.過濾出不為0的label
    # 3.過濾出出現次數>=500的label
    # 4.整理出必要的資訊、存成dict物件並回傳
    check = 0
    while True:     # 使用多次的上下迴圈、下上迴圈整理各component的label
        check_tmp = check
        for I in range(511):
            for J in range(511):
                if(init_component[I][J] == 0):
                    continue
                if(init_component[I][J+1]>0 and init_component[I][J+1]>init_component[I][J]):
                    init_component[I][J+1] = init_component[I][J]
                    check += 1
                if(init_component[I+1][J]>0 and init_component[I+1][J]>init_component[I][J]):
                    init_component[I+1][J] = init_component[I][J]
                    check += 1

        for I in range(511, 0, -1):
            for J in range(511, 0, -1):
                if(init_component[I][J] == 0):
                    continue
                if(init_component[I][J-1]>0 and init_component[I][J-1]>init_component[I][J]):
                    init_component[I][J-1] = init_component[I][J]
                    check += 1
                if(init_component[I-1][J]>0 and init_component[I-1][J]>init_component[I][J]):
                    init_component[I-1][J] = init_component[I][J]
                    check += 1
        if(check == check_tmp):  # 若此輪完全沒進入if判別式，代表label單一化完成，跳出While迴圈
            break

    component_labels_dict = {}  # 使用component_labels_dict紀錄各label之出現次數（key=label：value=次數）

    for I in range(512):
        for J in range(512):
            if(init_component[I][J]>0):
                if(init_component[I][J] not in component_labels_dict):
                    component_labels_dict[init_component[I][J]] = 1
                else:
                    component_labels_dict[init_component[I][J]] += 1

    component_label_filter = {} # 使用component_label_filter紀錄出現次數>=500的label（key=label：value=次數）
    for key, value in component_labels_dict.items():
        if(value >= 500):
            component_label_filter[key] = value

    Component = {}  # 使用Component紀錄四條邊界的位置（min/max_x/y）、兩個座標值加總（sum_x/y）、label出現次數（value）
    for key, value in component_label_filter.items():
        check = False
        for I in range(512):
            for J in range(512):
                if(init_component[I][J]==key and check == False):
                    min_x = J
                    max_x = J
                    min_y = I
                    max_y = I
                    sum_x = J
                    sum_y = I
                    check = True
                if(init_component[I][J]==key and check == True):
                    min_x = min(J, min_x)
                    max_x = max(J, max_x)
                    min_y = min(I, min_y)
                    max_y = max(I, max_y)
                    sum_x += J
                    sum_y += I
        Component[key] = [min_x, max_x, min_y, max_y, value, sum_x, sum_y]
    return Component

def DrawComponent(pic, Component):
    # 先畫出Threshold = 128的pic
    # 再以pic為底，以雙層迴圈畫出Component border
    pic = binarize(pic, 128).convert('RGB')  # 先求出binarize化的圖片，並轉換成RGB模式
    pic_load = pic.load()
    for key, value in Component.items():    # 畫出border與cross
        for I in range(value[0], value[1]):
            pic_load[I, value[2]] = (50, 50, 255)
            pic_load[I, value[2]+1] = (50, 50, 255)
            pic_load[I, value[3]] = (50, 50, 255)
            pic_load[I, value[3]-1] = (50, 50, 255)
        for I in range(value[2], value[3]):
            pic_load[value[0], I] = (50, 50, 255)
            pic_load[value[0]+1, I] = (50, 50, 255)
            pic_load[value[1], I] = (50, 50, 255)
            pic_load[value[1]-1, I] = (50, 50, 255)
        for I in range(-10,10):
            pic_load[int(value[5]/value[4])+I, int(value[6]/value[4])] = (255, 50, 50)
            pic_load[int(value[5]/value[4])+I, int(value[6]/value[4])-1] = (255, 50, 50)
            pic_load[int(value[5]/value[4])+I, int(value[6]/value[4])+1] = (255, 50, 50)
        for I in range(-10,10):
            pic_load[int(value[5]/value[4]), int(value[6]/value[4])+I] = (255, 50, 50)
            pic_load[int(value[5]/value[4])-1, int(value[6]/value[4])+I] = (255, 50, 50)
            pic_load[int(value[5]/value[4])+1, int(value[6]/value[4])+I] = (255, 50, 50)
    return pic


if __name__ == '__main__':
    wife = Image.open('lena.bmp')
    init_component = ComponentInitial(wife) # 將label標記在各個component上
    Component = ComponentSort(init_component)   # 整理出各component的角落位置
    output = DrawComponent(wife, Component)
    output.show()
    try:
        output.save('./result/connected_components.bmp')
    except:
        print('Error! 請確認含 connected_components.py 的目錄下存在 result 目錄!')
        exit()
