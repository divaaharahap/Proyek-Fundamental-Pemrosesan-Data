import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def scrape_main(url):
    data = []
    current_url = url
    max_pages = 50
    page_count = 1

    while current_url and page_count <= max_pages:
        print(f"Mengambil data dari halaman {page_count}...")
        response = requests.get(current_url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Gagal mengambil halaman {page_count}: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.find_all('div', class_="collection-card")

        if not items:
            print("Tidak ada item ditemukan. Berhenti.")
            break

        for item in items:
            title_tag = item.find('h3', class_="product-title")
            title = title_tag.text.strip() if title_tag else None

            price_tag = item.find('span', class_="price")
            price = price_tag.text.strip() if price_tag else None

            rating_tag = item.find('p', style="font-size: 14px; color: #777;")
            rating = rating_tag.text.strip() if rating_tag and "Rating" in rating_tag.text else None

            colors_tag = item.find('p', string=lambda text: text and "Colors" in text)
            colors = colors_tag.text.strip().split(' ')[0] if colors_tag else None

            size_tag = item.find('p', string=lambda text: text and "Size" in text)
            size = size_tag.text.strip().replace("Size: ", "") if size_tag else None

            gender_tag = item.find('p', string=lambda text: text and "Gender" in text)
            gender = gender_tag.text.strip().replace("Gender: ", "") if gender_tag else None

            data.append({
                'Title': title,
                'Price': price,
                'Rating': rating,
                'Colors': colors,
                'Size': size,
                'Gender': gender
            })


        # Pindah ke halaman berikutnya
        next_button = soup.find('li', class_='page-item next')
        if next_button and next_button.find('a', class_='page-link'):
            next_href = next_button.find('a')['href'] 
            current_url = urljoin(url, next_href)
            page_count += 1
            time.sleep(5)
        else:
            print("Tidak ada halaman berikutnya. Berhenti.")
            break

    return data
