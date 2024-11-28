import requests
import json
from bs4 import BeautifulSoup


def scrape_authors(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to retrieve page: {page_url}")
        return [], None

    soup = BeautifulSoup(response.text, 'lxml')
    authors_data = []
    author_links = []

    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        author_link = quote.find('small', class_='author').find_next_sibling('a')['href']
        author_links.append(author_link)

    author_links_not_repeat = set(author_links)
    base_url = "http://quotes.toscrape.com"
    for author_l in author_links_not_repeat:
        new_url = f'{base_url}{author_l}'  # Збираємо  повний URL автора
        new_response = requests.get(new_url)
        if new_response.status_code != 200:
            print(f"Failed to retrieve author page: {new_url}")
            continue
        new_soup = BeautifulSoup(new_response.text, 'lxml')
        author_details = new_soup.find('div', class_='author-details')
        if author_details:
            name = author_details.find('h3', class_='author-title').get_text(strip=True)
            born_date = author_details.find('span', class_='author-born-date').get_text(strip=True)
            born_location = author_details.find('span', class_='author-born-location').get_text(strip=True)
            description = author_details.find('div', class_='author-description').get_text(strip=True)
            authors_data.append({
                'fullname': name,
                'born_date': born_date,
                'born_location': born_location,
                'description': description
            })

    # Перевірка чи є кнопка
    next_button = soup.find('li', class_='next')
    next_page_url = None
    if next_button:
        next_relative_url = next_button.find('a')['href']
        next_page_url = f"{base_url}{next_relative_url}"  # Збираємо урлу для перехода
    return authors_data, next_page_url


def main():
    base_url = "http://quotes.toscrape.com"
    current_url = base_url
    all_authors = []

    while current_url:
        print(f"Scraping {current_url}...")
        authors, next_page_url = scrape_authors(current_url)
        all_authors.extend(authors)
        current_url = next_page_url  # Переходимо на наступну сторінку

    print(f"Total authors collected: {len(all_authors)}")

    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(all_authors, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()