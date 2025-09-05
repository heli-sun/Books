import requests
import time
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    return session

def fetch_books_by_query(query, max_results=400):
    print(f"📚 Fetching books for query: '{query}'")
    base_url = "https://www.googleapis.com/books/v1/volumes"
    all_books = []
    session = create_session()

    for i in range(0, min(max_results, 1000), 40):  # Google API limit workaround
        params = {
            'q': query,
            'maxResults': 40,
            'startIndex': i
        }
        try:
            response = session.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if 'items' in data:
                all_books.extend(data['items'])
            time.sleep(1.5)
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching data: {e}")
            continue
    return all_books

def process_and_save_books(books):
    data = []
    for item in books:
        volume_info = item.get('volumeInfo', {})
        if volume_info.get('description') and volume_info.get('title'):
            data.append({
                'title': volume_info.get('title'),
                'authors': volume_info.get('authors', ['N/A']),
                'description': volume_info.get('description'),
                'categories': volume_info.get('categories', ['N/A'])
            })
    df = pd.DataFrame(data).drop_duplicates(subset=['title'])
    df.to_csv('books_data.csv', index=False, encoding='utf-8')
    print(f"✅ Saved {len(df)} books to books_data.csv.")

if __name__ == "__main__":
    queries = [
        "sci-fi novels", "fantasy books", "historical fiction", "mystery thriller", "classic literature", 
        "modern poetry", "young adult fantasy", "children's books", "biography", "science books", 
        "Harry Potter", "The Lord of the Rings", "The Chronicles of Narnia", "George R.R. Martin", 
        "Agatha Christie", "Stephen King", "J.K. Rowling", "Jane Austen"
    ]

    all_books_data = []
    for q in queries:
        books = fetch_books_by_query(q, max_results=400)
        all_books_data.extend(books)

    process_and_save_books(all_books_data)
