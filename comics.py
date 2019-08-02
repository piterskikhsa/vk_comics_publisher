import os
import random
import sys
import tempfile

import requests
from dotenv import load_dotenv


def get_json_from_url(url, params=None):
    params = params or {}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_random_comics_id():
    url = 'http://xkcd.com/info.0.json'
    comics_json = get_json_from_url(url)
    max_comics_id = comics_json.get('num')
    return random.choice(range(max_comics_id))


def get_comics(comics_id):
    url = 'http://xkcd.com/{id}/info.0.json'.format(id=comics_id)
    return get_json_from_url(url)


def get_params(token, version=5.95, **kwargs):
    return {'access_token': token, 'v': version, **kwargs}


def get_url(method):
    return 'https://api.vk.com/method/{}'.format(method)


def get_upload_url(params):
    url = get_url('photos.getWallUploadServer')
    response = get_json_from_url(url, params=params)
    upload_url = response['response']['upload_url']
    return upload_url


def upload_img_on_wall(upload_url, image_file_path):
    with open(image_file_path, 'rb') as file:
        files = {
            'photo': file
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


def main():
    load_dotenv()
    auth_token = os.getenv('VK_TOKEN')
    group_id = os.getenv('GROUP_ID')
    comics_json = get_comics(get_random_comics_id())
    try:
        response = requests.get(comics_json['img'])
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(comics_json['img'])[-1]) as image_file:
            image_file.write(response.content)
            post = post_image_on_wall(auth_token, group_id, image_file.name, comics_json.get('alt'))
        print('Комикс был загружен на стену под id={}'.format(post['post_id']))
    except KeyError:
        sys.exit("Ошибка! Комикс загрузить не удалось.")


if __name__ == '__main__':
    main()
