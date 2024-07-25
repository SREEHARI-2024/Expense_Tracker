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

    @classmethod
    def get_transactions(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'],format=cls.FORMAT)
        start_date = datetime.strptime(start_date,cls.FORMAT)
        end_date = datetime.strptime(end_date,cls.FORMAT)

        mask = (df["date"]>=start_date) & (df["date"]<=end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transaction is present in between the entered date")
        else:
            print("Transactions:")
            print(
                filtered_df.to_string(
                    index=False,formatters={"date":lambda x: x.strftime(CSV.FORMAT)}
                    )
                )
            total_income = filtered_df[filtered_df["category"]=="Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()

            print(f"Total income is : {total_income:.2f}")
            print(f"Total expense is : {total_expense:.2f}")

        return filtered_df



def add():
    CSV.initialize()
    date = get_date("Enter the date in the format(dd-mm-yyyy)",allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)

def main():
    while True:
        print("\n1.Add new Transactions:")
        print("\n2.View Transactions and get summery:")
        print("\n3.Exit")

        choice = input()
        if choice=="1":
            add()
        elif choice=="2":
            start_date = get_date("Enter the start date : ")
            end_date = get_date("Enter the end date : ")
            CSV.get_transactions(start_date,end_date)
        elif choice=="3":
            print("Exiting........")
            break
        else:
            print("Invalid choice")

if __name__=="__main__":
    main()
        

