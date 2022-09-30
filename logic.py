import requests
from bs4 import BeautifulSoup


def get_list_of_films(username):
    page_number = 1
    list_of_films = []
    while True:
        r = requests.get(f'https://letterboxd.com/{username}/watchlist/page/{page_number}')
        page_number += 1
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')

        len_buffer = len(list_of_films)

        for i in soup.findAll('li', class_='poster-container'):
            film_name = i.img['alt']
            list_of_films.append(film_name)

        if len_buffer == len(list_of_films):
            break

    return list_of_films


def html_construcktor(films):
    html = '<ul>\n'

    for film in films:
        html += f'\t<li>{film}</li>\n'

    html += '</ul>'

    return html


# print(len(max(get_list_of_films('cronenbergman'), key=lambda x: len(x))))
# print(html_construcktor(get_list_of_films('cronenbergman')))
