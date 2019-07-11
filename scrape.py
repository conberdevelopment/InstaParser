from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re
import json
import urllib.request
import time

users = ['apple', '1', '2', '3', '4']


def gather_links(url, browser):
    start1 = time.time()
    browser.get(url)
    print(time.time() - start1)
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
        try:
            top_comment = parsed_string['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges'][0]['node']['text']
        except:
            top_comment = ''
        result = {
            "description": post_text,
            "likes": likes,
            "id": id,
            "top comment": top_comment
        }
        json_result = json.dumps(result)
        json_result = json.loads(json_result)
        print(json_result)


if __name__ == "__main__":
    try:
        browser = webdriver.Chrome('/Users/constantine/Downloads/chromedriver')
    except UnboundLocalError:
        print('Driver is not found')
    try:
        urllib.request.urlopen('https://instagram.com', timeout=5)
    except urllib.request.URLError:
        print('Instagram is not available')
    for user in users:
        url = 'https://www.instagram.com/' + user
        gather_links(url, browser)






