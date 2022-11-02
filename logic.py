import requests
from bs4 import BeautifulSoup


def get_list_of_films(username):
    page_number = 1
    list_of_films = []

    while True:
        r = requests.get(
            f'https://letterboxd.com/{username}/watchlist/page/{page_number}')
        page_number += 1
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')

        # check if user exist
        if soup.body.strong.text == 'Sorry, we can\u2019t find the page you\u2019ve requested.':
            raise ValueError('Not found')

        # get page films
        page_films = soup.findAll('li', class_='poster-container')

        if len(page_films) == 0:
            break

        for i in page_films:
            # get film title
            film_name = i.img['alt']
            list_of_films.append(film_name)

    return list_of_films


def html_construcktor(films):
    html = '<ul>\n'

    for film in films:
        html += f'\t<li>{film}</li>\n'

    html += '</ul>'

    return html


# print(len(max(get_list_of_films('cronenbergman'), key=lambda x: len(x))))
# print(html_construcktor(get_list_of_films('cronenbergman')))
# print(get_list_of_films("ldsjflfmdldmf"))
