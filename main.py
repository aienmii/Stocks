import requests
from dotenv import load_dotenv
import os
import tkinter as tk
from datetime import datetime, timedelta
import pandas as pd
from tksheet import Sheet, sheet
from plot import Plot
root = tk.Tk()

canvas = tk.Canvas(root, width=1000, height=1000)
canvas.grid(row=0, column=0, sticky="nsew")

load_dotenv()



def convert_to_frame(data):
    if isinstance(data, dict) and "historical" in data:
        data_list = data["historical"]
    elif isinstance(data, list):
        data_list= data
    else:
        raise ValueError(
            f"Unsupported JSON format or API error. Received structure keys: {list(data.keys()) if isinstance(data, dict) else type(data)}"
        )
    df = pd.DataFrame(data_list)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

    return df


def convert_to_sheet(data):
    df=convert_to_frame(data)

    sheet_data = df.values.tolist()
    sheet_headers = df.columns.tolist()

    sheet = Sheet(
        root,
        data=sheet_data,
        headers=sheet_headers,
        show_row_index=True
    )

    print("\n--- DataFrame Head ---")
    print(df.head())

    print(df)
    sheet.grid(row=0, column=0, sticky="nswe")
    sheet.enable_bindings()

    canvas.delete("all")
    canvas.create_text(10, 10, anchor="nw", text=df.to_string())

    return df


def get_stock_data():
    today=datetime.today().strftime('%Y-%m-%d')
    year_ago=(datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

    api_key = os.getenv("API_KEY")
    parametrs = {
        "from": year_ago,
        "to": today,

    }
    url="https://financialmodelingprep.com/stable/historical-price-eod/full?symbol=AAPL&apikey="+api_key
    r = requests.get(url,params=parametrs)

    print("Status Code:", r.status_code)
    print("Response Data:", r.json())
    print("Requested URL:", r.url)

    data = r.json()
    convert_to_sheet(data)



get_stock_data()
button = tk.Button(root, text="Load API", command=get_stock_data)
button.grid(row=1, column=0, sticky="ew")
canvas.grid(row=0, column=0, sticky="nsew")
root.mainloop()
