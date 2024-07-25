import csv
import logging
import pandas as pd
from datetime import datetime
from data_entry import get_date,get_amount,get_category,get_description

class CSV:
    CSV_FILE = "details.csv"
    FORMAT = "%d-%m-%Y"
    COLUMNS = ["date","amount","category","description"]
    

    @classmethod
    def initialize(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE , index=False)
        
    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entry = {
            "date":date,
            "amount":amount,
            "category":category,
            "description":description
        }

        with open(cls.CSV_FILE,"a",newline="") as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

def add():
    CSV.initialize()
    date = get_date("Enter the date in the format(dd-mm-yyyy)",allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)

add()