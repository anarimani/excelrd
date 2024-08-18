from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
import requests
import jdatetime
from jalali_date import datetime2jalali, date2jalali

@login_required
def login(request):
    return redirect('excelapp:select_date')

@login_required
def select_date(request):
    if request.method == 'POST':
        shamsi_date_str = request.POST.get('date')
        shamsi_date = jdatetime.datetime.strptime(shamsi_date_str, '%Y/%m/%d').date()
        gregorian_date = shamsi_date.togregorian()
        return redirect('excelapp:command_selector', date=gregorian_date.isoformat())
    return render(request, 'select_date.html')

@login_required
def command_selector(request, date):
    if request.method == 'POST':
        command = request.POST.get('command')
        if command == 'customer_product' or command == 'customer_best_product':
            return redirect('excelapp:select_customer', date=date, command=command)
        return redirect('excelapp:results', date=date, command=command)
    return render(request, 'command_selector.html', {'date': date})

@login_required
def select_customer(request, date, command):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        if command == 'customer_product':
            return redirect('excelapp:select_product', date=date, command=command, customer=customer)
        return redirect('excelapp:results', date=date, command=command, customer=customer)
    return render(request, 'select_customer.html', {'date': date, 'command': command})

@login_required
def select_product(request, date, command, customer):
    if request.method == 'POST':
        product = request.POST.get('product')
        return redirect('excelapp:results', date=date, command=command, customer=customer, product=product)
    return render(request, 'select_product.html', {'date': date, 'command': command, 'customer': customer})

@login_required
def results(request, date, command, customer=None, product=None):
    excel_file_url = 'https://app1.sae-net.net/sae.xlsx'
    
    try:
        response = requests.get(excel_file_url)
        response.raise_for_status()
        df = pd.read_excel(response.content, engine='openpyxl')
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        filtered_df = df[pd.to_datetime(df['تاریخ'], errors='coerce').dt.year == pd.to_datetime(date).year]

        if command == 'best_customer':
            best_customer = filtered_df['خریدار'].value_counts().idxmax()
            result = best_customer
        elif command == 'customer_product':
            filtered_df = filtered_df[filtered_df['نام_کالا'] == product]
            best_customer = filtered_df['خریدار'].value_counts().idxmax()
            result = best_customer
        elif command == 'best_seller':
            best_seller = filtered_df['نام_کالا'].value_counts().idxmax()
            result = best_seller
        elif command == 'customer_best_product':
            filtered_df = filtered_df[filtered_df['خریدار'] == customer]
            best_product = filtered_df['نام_کالا'].value_counts().idxmax()
            result = best_product
        else:
            result = "فرمان نامعتبر است"

    except Exception as e:
        result = f"داده‌ای موجود نیست: {e}"

    return render(request, 'results.html', {'result': result, 'date': date, 'command': command, 'customer': customer, 'product': product})
