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
                res = response.json()
                res['product']['type'] = modelo.type
                res['product']['price'] = modelo.price
                if modelo.type == 'variation':
                    res['product']['option1'] = modelo.attribute_2_values[0]
                    res['product']['option2'] = modelo.attribute_1_values[0]

                    for i, item in enumerate(res['product']['variants']):

                        if str(item['id']) == str(modelo.id_variant):
                            index = i
                            res['product']['index'] = index
                            break

                    for i, item in enumerate(res['product']['images']):

                        if int(modelo.id_variant) in item['variant_ids']:
                            index = i
                            res['product']['index_image'] = index
                            break

                if modelo.type == 'simple':
                    options_atributtes = []
                    for i in range(5):
                        attr_name = f"attribute_{i + 1}_name"
                        attr_value = f"attribute_{i + 1}_values"
                        obj = {
                            "name": getattr(modelo, attr_name),
                            "value": getattr(modelo, attr_value),
                        }

                        options_atributtes.append(obj)

                    res['product']['options_atributtes'] = options_atributtes

            # Devolver la respuesta como un objeto JSON
            return JsonResponse(res)

        else:
            # Manejar la respuesta de error
            print('Error al enviar la petición POST', response.json())

    # Si la solicitud no es POST, devolver un error
    return JsonResponse({'error': 'La solicitud debe ser POST'})
