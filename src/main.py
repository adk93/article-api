import bs4
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, initialize_app
import os

app = Flask(__name__)
CORS(app)

cred = credentials.ApplicationDefault()
initialize_app(cred, {'projectId': 'readabletapi'})


@app.route('/get_article', methods=['GET'])
def scrape_article():
    url = request.json['url']
    response = requests.get(url)

    response.encoding = 'utf-8-sig'

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract article title
    title = extract_title(soup)

    # Extract article body
    body = extract_body(soup)

    # Extract article author
    author = extract_author(soup)

    # Extract article image
    image = extract_image(soup)

    # Return article information as JSON
    print({'title': title, 'body': body, 'author': author, 'image': image})
    return jsonify({'title': title, 'body': body, 'author': author, 'image': image})


def extract_title(soup: bs4.BeautifulSoup) -> str:
    return soup.find('title').text.strip()


def extract_body(soup: bs4.BeautifulSoup) -> str:
    body = ""
    if article := soup.find('article'):
        for paragraph in article.find_all('p'):
            body += paragraph.text + "\n"
    elif section := soup.find('section'):
        for paragraph in section.find_all('p'):
            body += paragraph.text + "\n"
    else:
        pass

    return body.strip()


def extract_author(soup: bs4.BeautifulSoup) -> str:
    author = soup.find('meta', {'name': 'author'})
    if author:
        author = author.get('content')
    else:
        author = ""
    return author.strip()


def extract_image(soup: bs4.BeautifulSoup) -> str:
    image = soup.find('meta', {'property': 'og:image'})
    if image:
        image = image.get('content')
    else:
        image = ""

    return image


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
