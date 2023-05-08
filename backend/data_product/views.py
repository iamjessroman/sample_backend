from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from data_product.models import Product
import json
import requests
from data_product.constants import BASE_URL, ACCESS_TOKEN


# Create your views here.


@csrf_exempt
def get_product_identificator(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            # Obtener el contenido de la solicitud POST como una cadena de bytes
            body = request.body

            # Decodificar la cadena de bytes a una cadena de texto
            body_text = body.decode('utf-8')

            # Analizar la cadena de texto como un objeto JSON
            data = json.loads(body_text)

            # Obtener el objeto Modelo usando los datos enviados en la solicitud POST
            modelo = Product.objects.get(sku=data['sku'])

            url = BASE_URL + "admin/api/2022-10/products/" + modelo.id_product + ".json"
            headers = {'Content-Type': 'application/json', 'X-Shopify-Access-Token': ACCESS_TOKEN}

            response = requests.get(url, headers=headers)
            if response.ok:
                # Manejar la respuesta exitosa
                # print('Petición POST exitosa', response.json())
                # Devolver la respuesta como un objeto JSON
                return JsonResponse(response.json())

            else:
                # Manejar la respuesta de error
                print('Error al enviar la petición POST', response.json())

        # Si la solicitud no es POST, devolver un error
        return JsonResponse({'error': 'La solicitud debe ser POST'})
