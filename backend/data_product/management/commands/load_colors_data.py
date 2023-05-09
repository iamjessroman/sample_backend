from django.core.management import BaseCommand

from PIL import Image
import colorgram
import urllib.request
import webcolors
import math

class Command(BaseCommand):
    # Show this when the user types help
    help = "Colors Image"

    def handle(self, *args, **options):

        # Nombre del color que deseas convertir
        color_name = 'Blue'

        # Obtener el valor hexadecimal del color
        hex_value = webcolors.name_to_hex(color_name)

        # Valores hexadecimales de los dos colores que deseas comparar
        hex_color_1 = hex_value

        # Descargar la imagen desde la URL
        img_file = urllib.request.urlopen("https://cdn.shopify.com/s/files/1/0755/5442/3062/files/wsh05-blue_main_8a6d4932-4ac8-40b3-981a-62932bc8e11b.jpg?v=1683665626")

        # Cargar la imagen en PIL
        img = Image.open(img_file)

        # Extraer los colores de la imagen con colorgram.py
        colors = colorgram.extract(img, 10)

        # Ordenar la lista por porcentaje (de mayor a menor)
        colors_sorted = sorted(colors, key=lambda c: c.proportion, reverse=True)

        for color in colors_sorted:
            hex_color_2 = webcolors.rgb_to_hex((color.rgb.r, color.rgb.g, color.rgb.b))

            # Convertir los valores hexadecimales a valores RGB
            rgb_color_1 = tuple(int(hex_color_1[i:i + 2], 16) for i in (1, 3, 5))
            rgb_color_2 = tuple(int(hex_color_2[i:i + 2], 16) for i in (1, 3, 5))

            # Calcular la distancia Euclidiana entre los colores
            distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(rgb_color_1, rgb_color_2)]))

            # Definir un umbral de parentesco (por ejemplo, 50)
            threshold = 200  #ir apliando el umbral

            # Verificar si los colores son parecidos
            if distance < threshold:
                print('Los colores', hex_color_1, 'y', hex_color_2, 'son parecidos.')

