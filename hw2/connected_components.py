from PIL import Image
import binarize # 匯入binarize.py檔

def ComponentInitial(pic):
    width, height = pic.size
    pic_load = pic.load()
    init_component = [[0 for J in range(512)] for I in range(512)]
    label = 1   # 初始化，若pixil超過閥值，即以label值讀入pic_component陣列中對應的位置
    for I in range(width):
        for J in range(height):
            if(pic_load[I, J] >=128):
                init_component[J][I] = label
                label += 1
    return init_component

def ComponentSort(init_component):
    recursive = 0
    check = 0
    while True:     # 使用上下迴圈、下上迴圈使同component的label單一化
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
        if(check == check_tmp):  # 若做完迴圈的圖與原本的圖相同，代表label單一化完成
            break
        recursive +=1
    print(recursive) # 迴圈次數

    component_labels = []
    for I in range(512):    # 使用component_labels紀錄label不為0的pixel
        for J in range(512):
            if(init_component[I][J]>0):
                component_labels.append(init_component[I][J])

    component_labels_dict = {}
    for label in component_labels:
        if(label not in component_labels_dict):
            component_labels_dict[label] = 1
        else:
            component_labels_dict[label] += 1

    component_label_filter = {}
    for key, value in component_labels_dict.items():  # 過濾出pixel總數>=500的component
        if(value >= 500):
            component_label_filter[key] = value
    print(component_label_filter)


    Component = {}
    for key, value in component_label_filter.items():
        check = False
        for I in range(512):
            for J in range(512):
                if(init_component[I][J]==key and check == False):
                    min_x = J
                    max_x = J
                    min_y = I
                    max_y = I
                    check = True
                if(init_component[I][J]==key and check == True):
                    min_x = min(J, min_x)
                    max_x = max(J, max_x)
                    min_y = min(I, min_y)
                    max_y = max(I, max_y)
        Component['ComponentNo%d' % key] = [min_x, max_x, min_y, max_y, value]
    return Component

def DrawComponent(pic, Component):
    # 先畫出Threshold = 128的pic
    # 再以pic為底，以雙層迴圈畫出Component border
    pic = binarize.binarize(pic, 128).convert('RGB')  # 使用binarize.py的binarize函式得到binarize化的圖片
    pic_load = pic.load()
    print(pic_load[0,0])
    for key, value in Component.items():    # 畫出border
        for I in range(value[0], value[1]):
            pic_load[I, value[2]] = (255, 0, 0)
            pic_load[I, value[2]+1] = (255, 0, 0)
            pic_load[I, value[3]] = (255, 0, 0)
            pic_load[I, value[3]-1] = (255, 0, 0)
        for I in range(value[2], value[3]):
            pic_load[value[0], I] = (255, 0, 0)
            pic_load[value[0]+1, I] = (255, 0, 0)
            pic_load[value[1], I] = (255, 0, 0)
            pic_load[value[1]-1, I] = (255, 0, 0)
    pic.show()



if __name__ == '__main__':
    wife = Image.open('lena.bmp')
    init_component = ComponentInitial(wife) # 將label標記在各個component上
    Component = ComponentSort(init_component)   # 整理出各component的角落位置
    DrawComponent(wife, Component)
    print(Component)
