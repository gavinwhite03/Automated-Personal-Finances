import csv
import gspread
import time

YEAR = '2023'

file = f"capital_one{YEAR}.csv"
transactions = []
def capitalOneFin(file):
    transactions = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            date = row[0]
            name = row[3]
            category = row[4]
            if name == 'WM MORRISONS STORE' or name == 'SAINSBURYS S/MKTS' or name == 'WAITROSE 311':
                category = 'Grceries'
            if name == 'ONE STOP 0969':
                category = 'Snacks'
            amount_str = row[5]
            try:
                amount = float(amount_str)
            except ValueError:
                print(f"Skipping row with invalid amount: {row}")
                continue

            transaction = ((date, name, category, amount))
            print(transaction)
            transactions.append(transaction)

    return transactions

        
sa = gspread.service_account(filename= "python-finance-manager-411922-24ef6c04fdcf.json")
sh = sa.open("Personal Finances")

worksheet_title = "2023"
worksheet = None
try:
    worksheet = sh.worksheet(worksheet_title)
except gspread.exceptions.WorksheetNotFound:
    worksheet = sh.add_worksheet(title=worksheet_title, rows="100", cols="20")

rows = capitalOneFin(file)
print(rows)

# Append rows to the worksheet
worksheet.append_rows(rows, value_input_option='USER_ENTERED')
