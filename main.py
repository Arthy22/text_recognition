import pytesseract
import PIL.Image
import re
import pandas as pd
from openpyxl import load_workbook
myconfig =r"--psm 11 --oem 3"
text=pytesseract.image_to_string(PIL.Image.open("billtest4.jpg"),config=myconfig)
print(text)
bill_no_pattern = re.compile(r'\b(?:Invoice No|Bill No)\s*\w*\s*(\w+)', re.IGNORECASE)
bill_date_pattern =  re.compile(r'\b(Bill Date)\s*\w*\s*(\w+/\w+/\w+)', re.IGNORECASE)
bill_amount_pattern=re.compile(r'\b(?:Bill Amount|Net Amount)\s*\w*\s*(\w+\.\w+)',re.IGNORECASE)
bill_company_name_pattern=re.compile(r'\b(?:PALANIAPPA PHARMACEUTICALS|MURUGALAYA AGENCIES|SRI SAI PHARMA)',re.IGNORECASE)


# Search for the pattern in the text
match = bill_no_pattern.search(text)
match2=bill_date_pattern.search(text)
match3=bill_amount_pattern.search(text)
match4=bill_company_name_pattern.search(text)

if match:
    bill_no = match.group(1)
    print(f'Bill No: {bill_no}')
if match2:
    bill_date=match2.group(2)
    print(f'Bill Date: {bill_date}')
if match3:
    bill_amount=match3.group(1)
    print(f'Bill Amount:{bill_amount}')
if match4:
    bill_company_name=match4.group(0)
    print(f'Bill Name:{bill_company_name}')
    
new_data = pd.DataFrame({
    'Bill No': [bill_no],
    'Bill Date': [bill_date],
    'Bill Amount': [bill_amount],
    'Company Name': [bill_company_name]
})
file_path = 'extracted_data.xlsx'
try:
    existing_data = pd.read_excel(file_path)
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)
except FileNotFoundError:
    combined_data = new_data
combined_data.to_excel(file_path, index=False)
print(f'Data successfully written to {file_path}')
