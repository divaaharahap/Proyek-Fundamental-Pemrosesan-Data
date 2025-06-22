import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine

def save_to_csv(df: pd.DataFrame, filename: str = "output.csv") -> None:
    try:
        df.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"Gagal menyimpan ke CSV: {e}")

def authorize_gsheets(json_keyfile: str):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Gagal authorisasi Google Sheets API: {e}")
        return None

def save_to_gsheet(df, sheet_name, json_keyfile, spreadsheet_name):
    client = authorize_gsheets(json_keyfile)
    if client is None:
        print("Client Google Sheets tidak tersedia.")
        return

    try:

        spreadsheet = client.open(spreadsheet_name)
        print(f"Spreadsheet '{spreadsheet_name}' berhasil dibuka.")

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            worksheet.clear()
            print(f"Worksheet '{sheet_name}' ditemukan dan dikosongkan.")
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")
            print(f"Worksheet '{sheet_name}' dibuat.")

        data = [df.columns.values.tolist()] + df.values.tolist()
        worksheet.update(data)
        print(f"Data berhasil diupload ke Google Sheets di worksheet '{sheet_name}'.")
        print(f"Link spreadsheet: {spreadsheet.url}")

    except Exception as e:
        print(f"Error upload ke Google Sheets: {e}")

def load_to_postgres(df: pd.DataFrame, db_url: str, table_name: str):
    try:
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='replace', index=False)  
        print(f"Data berhasil disimpan ke tabel '{table_name}'.")
    except Exception as e:
        print(f"Gagal menyimpan ke PostgreSQL: {e}")

def read_from_postgres(db_url: str, table_name: str) -> pd.DataFrame:
    try:
        engine = create_engine(db_url)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Gagal membaca data dari PostgreSQL: {e}")
        return pd.DataFrame()
        

def load_all(df: pd.DataFrame, 
             csv_filename: str,
             sheet_name: str, 
             json_keyfile: str,
             spreadsheet_name: str,
             db_url: str,
             table_name: str):
    if df.empty:
        raise ValueError("DataFrame kosong tidak bisa diproses")
    print("Mulai menyimpan data ke CSV...")
    save_to_csv(df, csv_filename)
    print("Mulai menyimpan data ke Google Sheets...")
    save_to_gsheet(df, sheet_name, json_keyfile, spreadsheet_name)
    print("Mulai menyimpan data ke PostgreSQL...")
    load_to_postgres(df, db_url, table_name)
    print("Semua proses penyimpanan selesai.")

