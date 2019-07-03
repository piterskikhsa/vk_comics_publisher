import os
import random
import glob

import requests
from dotenv import load_dotenv


load_dotenv()


def get_output_folder(output_folder_path):
    os.makedirs(output_folder_path, exist_ok=True)
    return output_folder_path


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


def download_random_comics(img_folder):
    random_id = get_random_comics_id()
    comics_json = get_comics(random_id)
    output_name = '{}/{}'.format(img_folder, comics_json['title'])
    image_name = download_image(comics_json['img'], output_name)
    return image_name, get_comment(comics_json)


def get_params(token, version=5.95, **kwargs):
    return {'access_token': token, 'v': version, **kwargs}


def get_url(method):
    return 'https://api.vk.com/method/{}'.format(method)


def get_upload_url(params):
    url = get_url('photos.getWallUploadServer')
    response = get_json_from_url(url, params=params)
    try:
        upload_url = response['response']['upload_url']
    except KeyError:
        raise ValueError(response['error'])
    return upload_url


def upload_img_on_wall(upload_url, image_file_path):
    files = {
        'photo': open(image_file_path, 'rb')
    }
    response = requests.post(upload_url, files=files)
    response.raise_for_status()
    return response.json()


def save_image_on_wall(params):
    url = get_url('photos.saveWallPhoto')
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def post_image(params):
    url = get_url('wall.post')
    response = get_json_from_url(url, params=params)
    return response.get('response')


def post_image_on_wall(token, group_id, image_name, image_description):
    upload_url = get_upload_url(get_params(token))
    upload_data = upload_img_on_wall(upload_url, image_name)
    save_on_wall_data = save_image_on_wall(get_params(token=token, **upload_data))
    attach_data = save_on_wall_data['response'][0]
    some_params = {
        'owner_id': group_id,
        'from_group': 1,
        'attachments': 'photo{}_{}'.format(attach_data['owner_id'], attach_data['id']),
        'message': image_description}
    post = post_image(get_params(token, **some_params))
    return post


def remove_upload_image(dir_path):
    files = glob.glob('{}/*'.format(dir_path))
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
    

def main():
    auth_token = os.getenv('VK_TOKEN')
    group_id = os.getenv('GROUP_ID')
    image_folder = get_output_folder('image')
    image_name, image_description = download_random_comics(image_folder)
    post = post_image_on_wall(auth_token, group_id, image_name, image_description)
    if post:
        remove_upload_image(image_folder)
        print(post)


if __name__ == '__main__':
    main()
