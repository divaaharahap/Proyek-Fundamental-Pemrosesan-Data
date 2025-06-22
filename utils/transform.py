import pandas as pd

def transform_data(data):
    df = pd.DataFrame(data)
    print(f"Nama kolom: {df.columns.tolist()}")

    # 1. Menghapus baris dengan nilai default dari proses extract
    df = df[
        (df['Title'] != 'No Title') &
        (df['Price'] != 'No Price') &
        (df['Rating'] != 'Invalid Rating') &
        (df['Colors'] != '0') &
        (df['Size'] != 'No Size') &
        (df['Gender'] != 'No Gender')
    ]

    # 2. Konversi 'Price' ke Rupiah
    df['Price'] = df['Price'].apply(
        lambda x: float(x.replace('$', '').replace(',', '')) * 16000 if isinstance(x, str) and '$' in x else 0
    )

    # 3. Konversi 'Rating' dari teks ke angka float
    def safe_parse_rating(x):
        try:
            if isinstance(x, str) and '⭐' in x:
                return float(x.split('⭐')[1].split('/')[0].strip())
        except:
            pass
        return 0

    df['Rating'] = df['Rating'].apply(safe_parse_rating)

    # 4. Ekstraksi angka dari 'Colors'
    df['Colors'] = df['Colors'].apply(
        lambda x: int(x.split()[0]) if isinstance(x, str) and x.split()[0].isdigit() else 0
    )

    # 5. Membersihkan teks 'Size' dan 'Gender'
    df['Size'] = df['Size'].apply(lambda x: x.replace('Size: ', '') if isinstance(x, str) else 'Unknown Size')
    df['Gender'] = df['Gender'].apply(lambda x: x.replace('Gender: ', '') if isinstance(x, str) else 'Unknown Gender')

    # 6. Hapus nilai tidak masuk akal
    df = df[
        (df['Price'] > 0) &
        (df['Rating'] > 0) &
        (df['Colors'] > 0) &
        (df['Size'] != 'Unknown Size') &
        (df['Gender'] != 'Unknown Gender')
    ]

    # 7. Hapus duplikat
    df = df.drop_duplicates()

    return df
