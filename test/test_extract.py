import unittest
from unittest.mock import patch, Mock
from utils.extract import scrape_main

class TestExtract(unittest.TestCase):
    
    @patch('utils.extract.requests.get')
    def test_scrape_main_basic(self, mock_get):
       
        html = '''
        <div class="collection-card">
            <h3 class="product-title">Product A</h3>
            <span class="price">$10</span>
            <p style="font-size: 14px; color: #777;">Rating ⭐4.5 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Men</p>
        </div>
        '''

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = html.encode('utf-8')
        mock_get.return_value = mock_response

        data = scrape_main("https://fashion-studio.dicoding.dev/products?page=1")
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn('Title', data[0])
        self.assertEqual(data[0]['Title'], 'Product A')

if __name__ == '__main__':
    unittest.main()
