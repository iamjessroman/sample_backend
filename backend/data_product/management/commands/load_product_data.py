import csv
from django.core.management import BaseCommand

# Import the model
from data_product.models import Product

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from *.csv"

    def handle(self, *args, **options):

        # Show this if the data already exist in the database
        if Product.objects.exists():
            print('Product data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading Product data")

        # Code to load the data into database
        input_file = csv.DictReader(open('./sample_data.csv'), delimiter=',')
        for row in input_file:
            p = Product(attribute_1_name=row["Attribute 1 name"],
                        attribute_2_name=row["Attribute 2 name"],
                        attribute_3_name=row["Attribute 3 name"],
                        attribute_4_name=row["Attribute 4 name"],
                        attribute_5_name=row["Attribute 5 name"],
                        description=row['description'],
                        id=row['ID'],
                        images=row['Images'].split(","),
                        inventory_quantity=row['Stock'],
                        name=row['Name'],
                        parent=row['Parent'],
                        price=row['Regular price'],
                        sku=row['SKU'],
                        type=row['Type'])

            for i in range(5):
                attr_value = f"Attribute {i + 1} value(s)"
                attr_name = f"attribute_{i + 1}_values"
                if len(row[attr_value]) != 0:
                    if ',' in row[attr_value]:
                        my_list1 = row[attr_value].split("|")
                        my_list2 = [item.split(",") for item in my_list1]
                        result = [item for sublist in my_list2 for item in sublist]
                        setattr(p, attr_name, result)
                    else:
                        values = list(filter(bool, row[attr_value].split("|")))
                        setattr(p, attr_name, values)

            p.save()
            print("id", row['ID'])
