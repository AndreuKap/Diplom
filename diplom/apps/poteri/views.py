from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views import View
from django.views.generic import TemplateView
from .models import Statia, Comment
from tensorflow import keras
from keras.preprocessing import image
from io import BytesIO
from PIL import Image
from .nero3 import *
import openpyxl
import json
import numpy as np


def index(request):
	list_index = Statia.objects.order_by('-pub_date')[:3]
	list_stat = Statia.objects.order_by('-pub_date')
	return render(request, 'poteri/index.html', {'list_index': list_index})

def news(request):
	list_index = Statia.objects.order_by('-pub_date')
	list_stat = Statia.objects.order_by('-pub_date')
	return render(request, 'poteri/news.html', {'list_index': list_index})

def schot(request):
	return render(request, 'poteri/poteri_1.html')

def detal(request, statia_id):
    try: 
        a = Statia.objects.get (id = statia_id )
    except:
        raise HttpResponseNotFound('error 404')

    latest_comments_list = a.comment_set.order_by('-id')

    return render(request, 'poteri/detal.html', {'statia': a, 'latest_comments_list': latest_comments_list})
    
def lave_comment(request, statia_id):
    try: 
        a = Statia.objects.get (id = statia_id )
    except:
        raise HttpResponseNotFound('error 404')

    a.comment_set.create(name = request.POST['name'], comment_text = request.POST['text'])

    return HttpResponseRedirect( reverse('poteri:detal', args = (a.id,))) 

class Pro_p(TemplateView):
    template_name = 'poteri/pro_p.html'

def zadacha(request):
    if request.method == 'POST':
        kol_potokt = (request.POST['kol_potok'])
        name_voi = request.POST['name_voi']
        kol_potok =''
        chism = kol_potokt
        for i in range(int(kol_potokt)):
            kol_potok += '1'
        if name_voi == '1':
            tape = 'ricar'
        elif name_voi == '2':
            tape = 'mongol'
        else:
            tape = 'rusich'
    return render(request, 'poteri/poteri_2.html', {'kol_potok': kol_potok, 'tape': tape, 'chism': chism, 'kol_potok_ch': len(kol_potok) }) 


def josn_poteri(request):
    if request.method == 'POST':
        try:
            # Получение данных из JSON-тела запроса
            data = json.loads(request.body.decode('utf-8'))

            # Извлечение трех числовых значений
            number1 = float(data.get('v1', 0))
            number2 = float(data.get('v2', 0))
            number3 = float(data.get('v3', 0))

            # Ваша логика обработки числовых значений здесь
            # ...
            

            pot_model = keras.models.load_model('models/pos_model')
            pot_model.summary()
            predictions = pot_model.predict([[number1, number2, number3*0.001]])[0]
            # Пример ответа
            response_data = {'status': 'success', 'result_nero': float(predictions[0])}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

class Coins(View):
    def get(self, request):
        if request.GET:
            leng = request.GET['leng']   
        else:
            leng = 'ua'  
        return render(request, f'poteri/coins_{leng}.html')
    
def coin_img(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']

        # Check if the uploaded file is an image
        if not uploaded_file.content_type.startswith('image'):
            # Handle the case where the uploaded file is not an image
            return HttpResponse("Invalid file format")

        wb = openpyxl.load_workbook('models/coins/models.xlsx')
        sheet = wb.get_sheet_by_name('Sheet1')

        i = 1
        tile_size = 150
        list_predictions = []

        while True:
            cod_model = sheet[f'A{i}'].value
            if cod_model == 'stop':
                break

            coin_model = keras.models.load_model('models/coins/' + cod_model)
            print(cod_model)

            # Move the cursor to the beginning of the BytesIO object
            uploaded_file.seek(0)
            
            # Use Pillow's Image.open to load the image
            img = Image.open(uploaded_file)
            img = img.convert('L')  # Convert to grayscale if needed
            img = img.resize((tile_size, tile_size))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img /= 255.0  # Preprocess the image if necessary

            predictions = coin_model.predict(img)
            list_predictions.append(predictions[0, 0])
            i += 1

        max_index = list_predictions.index(max(list_predictions))

        if list_predictions[max_index] > 0.5:
            return JsonResponse({'status': 'success', 'max_index': float(list_predictions[max_index]), 'name_coin': sheet[f'B{max_index +1}'].value, 'url_coin': sheet[f'C{max_index +1}'].value, 'str_coin': sheet[f'D{max_index +1}'].value})
        else:
            return JsonResponse({'status': 'success', 'max_index': 0, 'name_coin': '', 'url_coin': '', 'str_coin': ''})
    else:
        return JsonResponse({'status': 'error'})


class Trip(TemplateView):
    template_name = 'poteri/trip.html'

def trip_img(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']

        # Check if the uploaded file is an image
        if not uploaded_file.content_type.startswith('image'):
            # Handle the case where the uploaded file is not an image
            return HttpResponse("Invalid file format")

        # Read the file data
        file_data = uploaded_file.read()

        # Create a BytesIO object to simulate a file-like object
        file_stream = BytesIO(file_data)

        # Create an InMemoryUploadedFile
        in_memory_uploaded_file = InMemoryUploadedFile(
            file_stream, None, uploaded_file.name, uploaded_file.content_type, None, None)

        # Now you can use the Imeges class with the uploaded file
        with Imeges(15, in_memory_uploaded_file) as img_obj:
            input_data = img_obj.split_img()
            cnn_model = 'models/7_model'
            cnn = CNN(cnn_model, input_data, 15, img_obj.width)
            result_matrix, sum_hose = cnn.trainCNN()
            learn = Learn(result_matrix)
            dans = Dans(learn.learning(), result_matrix)
            itog_sum_hose = dans.result()


        return JsonResponse({'status': 'success', 'sum_hose': int(sum_hose), 'itog_sum_hose': int(itog_sum_hose) })
    else:
        return JsonResponse({'status': 'error'})    



