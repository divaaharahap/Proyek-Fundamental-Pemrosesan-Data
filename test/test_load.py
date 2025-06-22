import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils import load

class TestLoad(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "title": ["Produk A", "Produk B"],
            "price": [160000, 320000],
            "rating": [4.5, 4.7],
            "colors": [3, 2],
            "size": ["M", "L"],
            "gender": ["Male", "Female"]
        })

        self.empty_df = pd.DataFrame()

        self.csv_filename = "test_products.csv"
        self.sheet_name = "Products"
        self.json_keyfile = "fake-json-keyfile.json"
        self.spreadsheet_name = "TestSpreadsheet"
        self.db_url = "postgresql://user:password@localhost:5432/test_db"
        self.table_name = "products"

    def test_save_to_csv(self):
        try:
            load.save_to_csv(self.df, self.csv_filename)
        except Exception as e:
            self.fail(f"save_to_csv gagal: {e}")

    @patch('utils.load.gspread.authorize')
    @patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name')
    def test_save_to_gsheet(self, mock_credentials, mock_authorize):
   
        mock_client = MagicMock()
        mock_authorize.return_value = mock_client

        mock_spreadsheet = MagicMock()
        mock_client.open.return_value = mock_spreadsheet
        mock_worksheet = MagicMock()
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        
        try:
            load.save_to_gsheet(self.df, self.sheet_name, self.json_keyfile, self.spreadsheet_name)
        except Exception as e:
            self.fail(f"save_to_gsheet gagal: {e}")

    @patch('utils.load.create_engine')
    def test_load_to_postgres(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        try:
            load.load_to_postgres(self.df, self.db_url, self.table_name)
        except Exception as e:
            self.fail(f"load_to_postgres gagal: {e}")

    @patch('utils.load.create_engine')
    def test_read_from_postgres(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        with patch('pandas.read_sql', return_value=self.df):
            df_result = load.read_from_postgres(self.db_url, self.table_name)
            self.assertFalse(df_result.empty)

    @patch('utils.load.save_to_csv')
    @patch('utils.load.save_to_gsheet')
    @patch('utils.load.load_to_postgres')
    def test_load_all(self, mock_load_postgres, mock_save_gsheet, mock_save_csv):
        try:
            load.load_all(
                self.df,
                csv_filename=self.csv_filename,
                sheet_name=self.sheet_name,
                json_keyfile=self.json_keyfile,
                spreadsheet_name=self.spreadsheet_name,
                db_url=self.db_url,
                table_name=self.table_name
            )
            mock_save_csv.assert_called_once()
            mock_save_gsheet.assert_called_once()
            mock_load_postgres.assert_called_once()
        except Exception as e:
            self.fail(f"load_all gagal: {e}")

    def test_load_all_with_empty_df(self):
        with self.assertRaises(Exception):
            load.load_all(
                self.empty_df,
                csv_filename=self.csv_filename,
                sheet_name=self.sheet_name,
                json_keyfile=self.json_keyfile,
                spreadsheet_name=self.spreadsheet_name,
                db_url=self.db_url,
                table_name=self.table_name
            )
