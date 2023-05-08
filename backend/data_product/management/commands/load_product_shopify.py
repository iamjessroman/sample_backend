from django.core.management import BaseCommand

import requests
import json
from PIL import Image
from io import BytesIO
import urllib.request
import colorgram
import webcolors

# Import the model
from data_product.models import Product
from data_product.constants import BASE_URL, ACCESS_TOKEN

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Load data to Shopify by type"

    def handle(self, *args, **options):

        variables = Product.objects.filter(type="variable")
        for variable in variables:
            # print("Variable ----- ", variable.name)
            variations = Product.objects.filter(parent=variable.sku)
            request = self.generateProductVariable(variable, variations)

            self.addProductShopify(request, variable, variations)
            # self.addProductImageShopify(variable, variations)
            # for varation in variations:
        # print("Varation ", varation.name)

        simples = Product.objects.filter(type="simple")
        # for row in simples:
        # print("Simple ----- ", row.name)

    def generateProductVariable(self, variable, varations):

        # for images of product
        data_images = []
        images = variable.images.split(',')
        for image in images:
            obj = {
                'src': image
            }
            data_images.append(obj)

        # get Colors
        data_colors = []
        images_uniques = varations.values('images').distinct()

        for image_unique in images_uniques:
            image = image_unique['images'].split(',')
            color_hex = self.getColorHexImage(image[0])
            data_colors.append(color_hex)
            varations.filter(images=image_unique['images']).update(color_hex=color_hex)

        # for variants
        data_variants = []
        for varation in varations:
            obj = {
                "title": varation.name,
                "sku": varation.sku,
                "option1": varation.color,
                "option2": varation.size,
                "option3": varation.color_hex,
            }
            data_variants.append(obj)

        # for options
        data_options = []

        obj = {"name": "Color", "values": variable.color.split("|")}
        data_options.append(obj)

        obj = {"name": "Size", "values": variable.size.split("|")}
        data_options.append(obj)

        obj = {"name": "Color Hex", "values": data_colors}
        data_options.append(obj)

        # for product
        data_json = {
            'product': {
                "title": variable.name,
                "body_html": variable.description,
                "images": data_images,
                "variants": data_variants,
                "options": data_options
            }
        }

        print(data_json)

        return data_json

    def addProductShopify(self, data_json, variable, variations):

        url = BASE_URL + "admin/api/2022-10/products.json"
        headers = {'Content-Type': 'application/json', 'X-Shopify-Access-Token': ACCESS_TOKEN}

        response = requests.post(url, headers=headers, data=json.dumps(data_json))
        if response.ok:
            # Manejar la respuesta exitosa
            # print('Petición POST exitosa', response.json())
            self.updateProductfromShopify(variable, variations, json.loads(response.text))

        else:
            # Manejar la respuesta de error
            print('Error al enviar la petición POST', response.json())

    def updateProductfromShopify(self, variable, varations, response):
        variable.id_product = response['product']['id']
        variable.save()

        for variant in response['product']['variants']:
            varation = varations.filter(sku=variant['sku'])

            for v in varation:
                v.id_product = variant['product_id']
                v.id_variant = variant['id']
                v.save()

        self.addProductImageShopify(variable, varations)

    def addProductImageShopify(self, variable, varations):

        # get images uniques of variants
        images_uniques = varations.values('images').distinct()

        for image_unique in images_uniques:

            image = image_unique['images'].split(',')

            variant_ids = list(varations.filter(images=image_unique['images']).values_list('id_variant', flat=True))

            obj = {
                "image": {
                    "variant_ids": variant_ids,
                    "src": image[0]
                }
            }

            print(obj)

            url = BASE_URL + "admin/api/2023-04/products/" + str(variable.id_product) + "/images.json"
            headers = {'Content-Type': 'application/json', 'X-Shopify-Access-Token': ACCESS_TOKEN}

            response = requests.post(url, headers=headers, data=json.dumps(obj))
            if response.ok:
                # Manejar la respuesta exitosa
                print('Petición POST exitosa', response.json())

            else:
                # Manejar la respuesta de error
                print('Error al enviar la petición POST', response.json())

    def getColorHexImage(self, url_image):

        # Descargar la imagen desde la URL
        img_file = urllib.request.urlopen(url_image)

        # Cargar la imagen en PIL
        img = Image.open(img_file)

        # Extraer los colores de la imagen con colorgram.py
        colors = colorgram.extract(img, 10)

        # Ordenar la lista por porcentaje (de mayor a menor)
        colors_sorted = sorted(colors, key=lambda c: c.proportion, reverse=True)

        color = colors_sorted[1]
        hex_color = webcolors.rgb_to_hex((color.rgb.r, color.rgb.g, color.rgb.b))

        return hex_color
