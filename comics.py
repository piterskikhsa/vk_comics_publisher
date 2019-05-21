import os

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


def get_random_comics_id():
    pass


def get_comment(comics_data):
    return comics_data.get('alt')


def get_comics(comics_id):
    pass


def get_upload_url(VK_TOKEN):
    method = 'photos.getWallUploadServer'
    response = ''
    return response['upload_url']


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


if __name__ == '__main__':
    main()