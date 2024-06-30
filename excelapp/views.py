from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
import requests

@login_required
def login(request):
    return redirect('excelapp:select-year')

@login_required
def select_year(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        return redirect('excelapp:command-selector', year=year)
    return render(request, 'select_year.html')

@login_required
def command_selector(request, year):
    if request.method == 'POST':
        command = request.POST.get('command')
        return redirect('excelapp:results', year=year, command=command)
    return render(request, 'command_selector.html')

def find_columns(df):
    columns = {
        'year': None,
        'product': None,
        'cost': None,
        'profit': None
    }
    
    for col in df.columns:
        col_lower = col.lower()
        if 'year' in col_lower:
            columns['year'] = col
        elif 'product' in col_lower:
            columns['product'] = col
        elif 'cost' in col_lower:
            columns['cost'] = col
        elif 'profit' in col_lower:
            columns['profit'] = col
            
    return columns

@login_required
def results(request, year, command):
    excel_file_url = 'https://arminnarimani.ir/excel/mydata.xlsx'
    
    try:
        response = requests.get(excel_file_url)
        response.raise_for_status()
        df = pd.read_excel(response.content, engine='openpyxl')
        
        columns = find_columns(df)
        if None in columns.values():
            raise ValueError("Required columns not found in the Excel file.")
        
        df['Year'] = df[columns['year']]
        filtered_df = df[df['Year'] == int(year)]
        
        if command == 'best_seller':
            result = filtered_df[columns['product']].value_counts().idxmax()
        elif command == 'most_expensive':
            result = filtered_df.loc[filtered_df[columns['cost']].idxmax(), columns['product']]
        elif command == 'cheapest':
            result = filtered_df.loc[filtered_df[columns['cost']].idxmin(), columns['product']]
        elif command == 'most_profitable':
            result = filtered_df.loc[filtered_df[columns['profit']].idxmax(), columns['product']]
        else:
            result = "Invalid command"
    except Exception as e:
        result = f"No data available: {e}"
    
    return render(request, 'results.html', {'result': result, 'year': year, 'command': command})