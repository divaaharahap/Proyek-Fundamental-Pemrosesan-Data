import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):

    def test_transform_basic(self):
        raw_data = [
            {
                "Title": "Product A",
                "Price": "$10",
                "Rating": "Rating ⭐4.5 / 5",
                "Colors": "3 Colors",
                "Size": "Size: M",
                "Gender": "Gender: Men"
            },
            {
                "Title": "Unknown Product",
                "Price": "$15",
                "Rating": "Invalid Rating",
                "Colors": "2 Colors",
                "Size": "Size: L",
                "Gender": "Gender: Women"
            },
            {
                "Title": "Product B",
                "Price": "$20",
                "Rating": "Rating ⭐4.0 / 5",
                "Colors": "1 Color",
                "Size": "Size: S",
                "Gender": "Gender: Women"
            }
        ]

        df = transform_data(raw_data)

        # Unknown Product harus terhapus
        self.assertNotIn("Unknown Product", df['Title'].values)
        # Harga sudah dikonversi ke float rupiah (harus > 0)
        self.assertTrue(all(df['Price'] > 0))
        # Rating sudah float dan valid
        self.assertTrue(all(df['Rating'] > 0))
        # Colors sudah angka
        self.assertTrue(pd.api.types.is_integer_dtype(df['Colors']))
        # Size dan Gender sudah bersih tanpa label
        self.assertTrue(all(~df['Size'].str.contains("Size:")))
        self.assertTrue(all(~df['Gender'].str.contains("Gender:")))
        # Tidak ada duplikat
        self.assertEqual(len(df), len(df.drop_duplicates()))

if __name__ == "__main__":
    unittest.main()
