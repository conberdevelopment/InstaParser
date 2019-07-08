from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re
import json
import urllib.request


def gather_links(url):
    try:
        browser = webdriver.Chrome('/Users/constantine/Downloads/chromedriver') #input here the path to your selenium webdriver
    except UnboundLocalError:
        print('Driver is not found')
    try:
        urllib.request.urlopen('https://instagram.com', timeout=1)
    except urllib.request.URLError:
        print('Instagram is not available')
    browser.get(url)
    links=[]
    source = browser.page_source
    data=bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('span')
    try:
        for link in script.findAll('a'):
            if re.match("/p", link.get('href')):
                links.append('https://www.instagram.com'+link.get('href'))
    except:
        print("Account isn't found")
    links_last = links[0:3]
    get_information_about_post(links_last)


def get_information_about_post(posts_list):
    for post_link in posts_list:
        link_j = post_link + '?__a=1'
        json_string = urllib.request.urlopen(link_j).read().decode('UTF-8')
        parsed_string = json.loads(json_string)
        try:
            post_text = parsed_string['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            post_text = ''
        likes = parsed_string['graphql']['shortcode_media']['edge_media_preview_like']['count']
        id = parsed_string['graphql']['shortcode_media']['id']
        result = {
            "description": post_text,
            "likes": likes,
            "id": id
        }
        json_result = json.dumps(result)
        json_result = json.loads(json_result)
        print(json_result)


if __name__ == "__main__":
    username = input("Input a username: ")
    username = str(username)
    url = 'https://www.instagram.com/' + username
    gather_links(url)






