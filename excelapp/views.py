from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
import requests
import jdatetime
from jalali_date import datetime2jalali, date2jalali
from django.contrib.auth.views import LoginView
from .forms import EventForm
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
# from django.contrib.auth import authenticate, login
# class CustomLoginView(LoginView):
# template_name = 'login.html'  # Adjusted path


def convert_jalali_to_datetime(jalali_date_str):
    # Assume jalali_date_str is in the format 'YYYY/MM/DD'

    year, month, day = map(int, jalali_date_str.split("-"))

    # Create a JalaliDate object
    jalali_date = jdatetime.datetime(year, month, day)

    # Get the corresponding Gregorian date
    gregorian_date = jalali_date.togregorian()

    return gregorian_date


@login_required
def login(request):
    return redirect("excelapp:select_date")


@login_required
def select_date(request):
    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            start_shamsi_date = form.cleaned_data["start_date"]
            end_shamsi_date = form.cleaned_data["end_date"]

            # Ensure end date is greater than or equal to start date
            if end_shamsi_date < start_shamsi_date:
                error_message = "End date must be greater than or equal to start date."
                return render(
                    request, "select_date.html", {"form": form, "error": error_message}
                )

            # Redirect to command_selector view with converted dates
            return redirect(
                "excelapp:command_selector",
                start_date=start_shamsi_date.strftime("%Y-%m-%d"),
                end_date=end_shamsi_date.strftime("%Y-%m-%d"),
            )
        else:
            # Handle form errors by re-rendering the form with its existing data
            return render(request, "select_date.html", {"form": form})

    else:
        form = EventForm()  # Instantiate an empty form for GET requests

    return render(request, "select_date.html", {"form": form})


@login_required
def command_selector(request, start_date, end_date):
    if request.method == "POST":
        command = request.POST.get("command")
        if command == "customer_product" or command == "customer_best_product":
            return redirect(
                "excelapp:select_customer",
                start_date=start_date,
                end_date=end_date,
                command=command,
            )
        return redirect(
            "excelapp:results",
            start_date=start_date,
            end_date=end_date,
            command=command,
        )
    return render(
        request,
        "command_selector.html",
        {"start_date": start_date, "end_date": end_date},
    )


@login_required
def select_customer(request, start_date, end_date, command):
    if request.method == "POST":
        customer = request.POST.get("customer")
        if command == "customer_product":
            return redirect(
                "excelapp:select_product",
                start_date=start_date,
                end_date=end_date,
                command=command,
                customer=customer,
            )
        return redirect(
            "excelapp:results",
            start_date=start_date,
            end_date=end_date,
            command=command,
            customer=customer,
        )
    return render(
        request,
        "select_customer.html",
        {"start_date": start_date, "end_date": end_date, "command": command},
    )


@login_required
def select_product(request, start_date, end_date, command, customer):
    if request.method == "POST":
        product = request.POST.get("product")
        return redirect(
            "excelapp:results",
            start_date,
            end_date,
            command=command,
            customer=customer,
            product=product,
        )
    return render(
        request,
        "select_product.html",
        {
            "start_date": start_date,
            "end_date": end_date,
            "command": command,
            "customer": customer,
        },
    )


@login_required
def results(request, start_date, end_date, command, customer=None, product=None):
    excel_file_url = "https://app1.sae-net.net/sae.xlsx"

    try:
        # response = requests.get(excel_file_url)
        # response.raise_for_status()
        # df = pd.read_excel(response.content, engine="openpyxl")
        df = pd.read_excel("instance\mydata.xlsx", engine="openpyxl")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df["Gregorian_Date"] = df["تاریخ"].apply(convert_jalali_to_datetime)
        filtered_df = df[
            (df["Gregorian_Date"] >= pd.to_datetime(start_date))
            & (df["Gregorian_Date"] <= pd.to_datetime(end_date))
        ]
        # print(filtered_df)
        if command == "best_customer":
            best_customer = filtered_df["خریدار"].value_counts().idxmax()
            result = best_customer
        elif command == "customer_product":
            filtered_df = filtered_df[filtered_df["نام_کالا"] == product]
            best_customer = filtered_df["خریدار"].value_counts().idxmax()
            result = best_customer
        elif command == "most_sold":
            most_sold = filtered_df["نام_کالا"].value_counts().idxmax()
            result = most_sold
        elif command == "profit_gained":
            profit_gained = filtered_df['profit'].sum()
            result = profit_gained
        elif command == "customer_best_product":
            filtered_df = filtered_df[filtered_df["خریدار"] == customer]
            best_product = filtered_df["نام_کالا"].value_counts().idxmax()
            result = best_product
        else:
            result = "فرمان نامعتبر است"

    except Exception as e:
        result = f"داده‌ای موجود نیست: {e}"

    return render(
        request,
        "results.html",
        {
            "result": result,
            "start_date": date2jalali(
                jdatetime.datetime.strptime(start_date, "%Y-%m-%d")
            ),
            "end_date": date2jalali(jdatetime.datetime.strptime(end_date, "%Y-%m-%d")),
            "command": command,
            "customer": customer,
            "product": product,
        },
    )
