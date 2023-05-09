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
            print(row)
            p = Product(id=row['ID'], type=row['Type'], sku=row['SKU'], name=row['Name'],
                        description=row['description'], images=row['Images'], size=row['Attribute 1 value(s)'],
                        color=row['Attribute 2 value(s)'], price=row['Regular price'], inventory_quantity=row['Stock'],
                        parent=row['Parent'],
                        attribute_1_name=row["Attribute 1 name"],
                        attribute_2_name=row["Attribute 2 name"],
                        attribute_3_name=row["Attribute 3 name"],
                        attribute_4_name=row[
                            "Attribute 4 name"],
                        attribute_5_name=row[
                            "Attribute 5 name"],
                        attribute_1_values=
                        row["Attribute 1 value(s)"],
                        attribute_2_values=row["Attribute 2 value(s)"],
                        attribute_3_values=row["Attribute 3 value(s)"],
                        attribute_4_values=row["Attribute 4 value(s)"],
                        attribute_5_values=row[
                            "Attribute 5 value(s)"])
            p.save()
