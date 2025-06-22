from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import load_all, load_to_postgres, read_from_postgres  # pastikan import load_all

def main():
    url = "https://fashion-studio.dicoding.dev/"
    
    data = scrape_main(url)
    if not data:
        print("Tidak ada data yang diambil.")
        return
    
    print(f"Jumlah data yang berhasil di-scrape: {len(data)}")

    
    transformed_data = transform_data(data)
    if transformed_data.empty:
        print("Data yang ditransformasi kosong.")
        return
    
    print(f"Jumlah data yang berhasil disimpan ke CSV: {len(transformed_data)}") 

    load_all(
        transformed_data,
        csv_filename='products.csv',
        sheet_name='Products',
        json_keyfile='proyek-pemda-0fbbb0a3090c.json',
        spreadsheet_name='Products',
        db_url="postgresql://postgres@localhost:5432/etl_db",
        table_name="products"
    )

    db_url = "postgresql://postgres@localhost:5432/etl_db"
    load_to_postgres(transformed_data, db_url=db_url, table_name="products")
    
    print("Membaca data dari tabel 'products':")
    df_postgres = read_from_postgres(db_url, "products")
    print(df_postgres.head())  
if __name__ == "__main__":
    main()
