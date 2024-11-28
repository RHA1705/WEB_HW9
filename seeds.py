import json
import connect
import models

with open('authors.json', 'r', encoding='utf-8') as a:
    authors_data = json.load(a)

with open('quotes.json', 'r', encoding='utf-8') as q:
    quotes_data = json.load(q)

for author_data in authors_data:
    authors = models.Author(**author_data)
    authors.save()

for quote_data in quotes_data:
    author = models.Author.objects(fullname=quote_data['author']).first()
    quotes = models.Quote(tags=quote_data['tags'], author=author, quote=quote_data['quote'])
    quotes.save()
