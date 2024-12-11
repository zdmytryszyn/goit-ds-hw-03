import json

import requests
from bs4 import BeautifulSoup


def parse_quote(page_url):
    list_of_quotes = []
    set_of_authors = set()
    while True:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")

        all_quotes = soup.find_all('span', class_='text')
        all_authors = soup.find_all('small', class_='author')
        all_tags = soup.find_all('div', class_='tags')

        for i in range(0, len(all_quotes)):
            quote = all_quotes[i].text
            author = all_authors[i].text
            tags_for_quote = all_tags[i].find_all('a', class_='tag')
            tags = [tag.text for tag in tags_for_quote]

            list_of_quotes.append({
                "tags": tags, "autor": author, "quote": quote
            })

            author_url = "https://quotes.toscrape.com" + all_authors[i].find_next('a')['href']
            set_of_authors.add(author_url)

        next_link = soup.find('li', class_='next')

        if next_link:
            next_page_url = next_link.find('a')['href']
            page_url = 'https://quotes.toscrape.com' + next_page_url
        else:
            break

    return list_of_quotes, set_of_authors


def parse_author(authors_urls):
    list_of_authors = []

    for author_url in authors_urls:
        response = requests.get(author_url)
        soup = BeautifulSoup(response.text, "html.parser")

        fullname = soup.find('h3', class_='author-title').text.strip()
        born_date = soup.find('span', class_='author-born-date').text.strip()
        born_location = soup.find('span', class_='author-born-location').text.strip()
        description = soup.find('div', class_='author-description').text.strip()

        list_of_authors.append({
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        })

    return list_of_authors


if __name__ == "__main__":
    url = 'https://quotes.toscrape.com/'

    parsed_quotes, all_authors = parse_quote(url)
    parsed_authors = parse_author(all_authors)

    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_quotes, f, ensure_ascii=False, indent=4)

    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_authors, f, ensure_ascii=False, indent=4)
