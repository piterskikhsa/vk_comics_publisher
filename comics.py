import os
import random

import requests
from dotenv import load_dotenv


load_dotenv()

# http://xkcd.com/info.0.json
# http://xkcd.com/614/info.0.json 
# {"month": "5", "num": 2152, "link": "", "year": "2019", "news": "", "safe_title": "Westerns", "transcript": "", 
# "alt": "Sitting here idly trying to figure out how the population of the Old West in the late 1800s compares to the number of Red Dead Redemption 2 players.", 
# "img": "https://imgs.xkcd.com/comics/westerns.png", "title": "Westerns", "day": "20"}



def download_image(image_link, image_name):
    response = requests.get(image_link)
    image_name = f'{image_name}{os.path.splitext(image_link)[-1]}'
    response.raise_for_status()
    with open(image_name, 'wb') as out_file:
        out_file.write(response.content)
    return image_name


def get_json_from_url(url, params={}):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_random_comics_id():
    url = 'http://xkcd.com/info.0.json'
    comics_json = get_json_from_url(url)
    try:
        max_comics_id = comics_json['num']
    except KeyError:
        return
    return random.choice(range(max_comics_id))


def get_comment(comics_data):
    return comics_data.get('alt')


def get_comics(comics_id):
    url = 'http://xkcd.com/{id}/info.0.json'.format(id=comics_id)
    return get_json_from_url(url)


def get_upload_url(VK_TOKEN):
    method = 'photos.getWallUploadServer'
    url = 'https://api.vk.com/method/{}'.format(method)
    params = {'access_token': VK_TOKEN, 'v': 5.95}
    response = get_json_from_url(url, params=params)
    print(response)
    return response['upload_url']


def download_random_comics(img_folder):
    random_id = get_random_comics_id()
    comics_json  = get_comics(random_id)
    output_name = '{}/{}'.format(img_folder, comics_json['title'])
    image_name = download_image(comics_json['img'], output_name)
    return  (image_name, get_comment(comics_json))


def upload_img():
    pass


def save_iamge_on_wall():
    pass


def post_image():
    pass


def remove_upload_image():
    pass
    

def main():
    METHOD_NAME = 'groups.get'
    vk_url = f'https://api.vk.com/method/{METHOD_NAME}'
    playload = {'access_token': os.getenv('VK_TOKEN'), 'v': 5.95}
    response = requests.get(vk_url, params=playload)
    print(download_random_comics('image'))
    print(get_upload_url(os.getenv('VK_TOKEN')))


if __name__ == '__main__':
    main()