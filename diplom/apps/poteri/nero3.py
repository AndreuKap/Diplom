from pickletools import optimize
from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from PIL import Image
import random
import numpy as np


class Imeges:
    def __init__(self, tile_size, imege_name):
        self.tile_size = tile_size
        self.imege_name = imege_name
        self.inpul_list = []
        self.image = None  # Initialize the image attribute

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.image:
            self.image.close()

    def get_img(self):
        self.image = Image.open(self.imege_name)
        return self.image
    
    def img_data(self):
        # Получаем размеры изображения
        self.width, self.height = self.image.size
        return self.width, self.height, self.tile_size

    def split_img(self):
        self.get_img()
        self.img_data()

        # Размеры квадратиков
        i, j = 0, 0
        # Цикл для разрезания изображения
        for y in range(0, self.height, self.tile_size):
            for x in range(0, self.width, self.tile_size):
                # Вырезаем квадратик  
                box = (x, y, x + self.tile_size, y + self.tile_size)
                tile = self.image.crop(box)
        
                control_sum = 0
                for item in tile.getdata():
                    if item[3] < 200:
                        control_sum += 1

                pixels = list(tile.convert('L').getdata())
                string = ' '.join(map(str, pixels))

                # проверяем степень пустоты квадрата
                if control_sum < self.tile_size * self.tile_size * 0.2:   
                    # Сохраняем каждый квадратик в отдельный файл
                    self.inpul_list.append(string)
                else:
                    self.inpul_list.append('FF')

                i += 1
            j += 1
        return self.inpul_list

class CNN:
    def __init__(self, model_text, input_mas, tile_size, width):
        self.model = keras.models.load_model(model_text)
        self.input_mas = input_mas
        self.tile_size = tile_size
        self.width = width

    def trainCNN(self):
        def sum_numbers_in_list(lst):
            total = 0
            for item in lst:
                if item != 'FF':
                    total += item
            return total 
        
        def split_list(input_list, chunk_size):
            return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

        itog_mas_line = []
        for i in range(0, len(self.input_mas)-1):
            if  self.input_mas[i] == 'FF':
                itog_mas_line.append('FF')
            else:
                element_list = self.input_mas[i].split()
                element_list_int = []
                for element in element_list:
                    element_list_int.append(int(element)/255)
                x_element_cat = np.array(element_list_int)
                itog_mas_line.append(np.argmax(self.model.predict(x_element_cat.reshape(-1, self.tile_size, self.tile_size, 1))))
                self.itog_mas = split_list(itog_mas_line, int(self.width / self.tile_size))
        print(f'Сумарна кількість аномалій на збереженій частині {sum_numbers_in_list(itog_mas_line)}') 
        return self.itog_mas, sum_numbers_in_list(itog_mas_line)

    
class Learn:
    def __init__(self, input_mas):
        self.itog_mas = input_mas


    def learning(self):
        x_train2 = []
        y_train2 = []
        itog_mas = self.itog_mas

        for i in range(len(itog_mas)-1, 2, -1):
            for j in range(len(itog_mas[0])-1, 2, -1):
                if 1 <= i < len(itog_mas)-2 and 1 <= j < len(itog_mas[0])-2:
                    lioning_x = []
                    kordinats = []
                    kordinats.append(i)
                    kordinats.append(j)
                    lioning_y = 0
                    lioning_x.append(itog_mas[i][j+1])
                    lioning_x.append(itog_mas[i+1][j])
                    lioning_x.append(itog_mas[i-1][j-1])
                    lioning_x.append(itog_mas[i][j-1])
                    lioning_x.append(itog_mas[i+1][j+1])
                    lioning_x.append(itog_mas[i-1][j])
                    lioning_x.append(itog_mas[i+1][j-1])
                    lioning_x.append(itog_mas[i-1][j+1])

                    lioning_y = itog_mas[i][j]

                # Генерируем 4 случайных числа от 0 до 7

                    for _ in range(8):
                        x_train2_element = []
                        random_numbers = random.sample(range(8), 4)
                        for index in random_numbers:
                            if lioning_x[index] == 'FF':
                                break
                            else:
                                x_train2_element.append(lioning_x[index]/15)
                                x_train2_element.append(index/8)
                        x_train2_element.append(kordinats[0]/34)
                        x_train2_element.append(kordinats[1]/22)

                        if lioning_y == 'FF':
                            break
                        else:
                            if x_train2_element != [] and len(x_train2_element) == 10:
                                x_train2.append(x_train2_element)
                                y_train2.append(lioning_y)


        x_train_cat2 = np.array(x_train2)
        y_train_cat2 = keras.utils.to_categorical(y_train2, 16)

        model = keras.Sequential([
            Dense(1024, input_shape=(10,), activation='relu'),
            Dropout(0.50),
            Dense(1024, activation='relu'),
            Dropout(0.5),
            Dense(16, activation='linear')
            ])

        model.compile(optimizer = 'adam' ,
                loss = 'mean_squared_error',
                metrics = ['accuracy'])

        model.fit(x_train_cat2, y_train_cat2, batch_size=1, epochs=5, validation_split = 0.3)
        return model


class Dans:
    def __init__(self, model, data_mas):
        self.model = model
        self.itog_mas = data_mas
        
    def result(self):
        itog_mas = self.itog_mas
        lioning_x = []
        for _ in range(2):
            for i in range(len(itog_mas)-1, 0, -1):
                for j in range(len(itog_mas[0])-1, 0, -1):
                    if 1 <= i < len(itog_mas)-1 and 1 <= j < len(itog_mas[0])-1 and itog_mas[i][j] == 'FF':
                        lioning_x.clear()
                        lioning_x.append(itog_mas[i][j+1])
                        lioning_x.append(itog_mas[i+1][j])
                        lioning_x.append(itog_mas[i-1][j-1])
                        lioning_x.append(itog_mas[i][j-1])
                        lioning_x.append(itog_mas[i+1][j+1])
                        lioning_x.append(itog_mas[i-1][j])
                        lioning_x.append(itog_mas[i+1][j-1])
                        lioning_x.append(itog_mas[i-1][j+1])
                        trein2_x_vxod = []
                        for random_index in random.sample(range(8), 8):
                            if lioning_x[random_index] != 'FF':
                                trein2_x_vxod.append(lioning_x[random_index])
                                trein2_x_vxod.append(random_index/8)
                                if len(trein2_x_vxod) == 8:
                                    break
                        if len(trein2_x_vxod) == 8:
                            trein2_x_vxod.append(i)
                            trein2_x_vxod.append(j)
                            itog_mas[i][j] = np.argmax(self.model.predict(np.array(trein2_x_vxod).reshape(1, 10)))

        # прверяем выходной блок, если нужно добавляем рамку из 0 и запускаем процесс заново
            control = False
            for i in itog_mas:
                for j in i:
                    if j == 'FF':
                        control = True
            if control:
                for i in range(len(itog_mas)):
                    if i == 0 or i == len(itog_mas) - 1:
                        for j in range(len(itog_mas[i])):
                            if itog_mas[i][j] == 'FF':
                                itog_mas[i][j] = 0
                    else:
                        if itog_mas[i][0] == 'FF':
                            itog_mas[i][0] = 0
                        if itog_mas[i][len(itog_mas[0])-1] == 'FF':
                            itog_mas[i][len(itog_mas[0])-1] = 0
            else:
                break
        summas = 0
        for _ in itog_mas:
            summas += sum(_)
        return summas    


