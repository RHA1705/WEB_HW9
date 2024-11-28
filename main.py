from models import Author, Quote
import connect


while True:
    user_input = input()
    if user_input == 'exit':
        break

    try:
        command, value = user_input.split(':')
        # print(command, value)
        if command == 'tag':
            result = Quote.objects(tags=value)
            for t in result:
                print(f'{t.quote}')

        if command == 'tags':
            values = value.split(',')
            result = Quote.objects(tags__in=values)
            for t in result:
                print(f'{t.quote}')

        if command == 'name':
            author = Author.objects(fullname=value).first()
            result = Quote.objects(author=author)
            for t in result:
                print(f'{t.quote}')
    except ValueError:
        print('Incorrect ask format. Please try again')
