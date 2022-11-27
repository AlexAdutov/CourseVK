import time
import requests
from settings import TokenYA, TokenVK
from pprint import pprint
#from tqdm import tqdm
from progress.bar import IncrementalBar

class VK:
    base_host = 'https://api.vk.com/method'

    def __init__(self, token):
        self.TokenVK = TokenVK

    def get_params(self):
        #pass
        return {
            'access_token': {self.TokenVK},
            'v': '5.131',
            'owner_id': 50984240, #input('Введите id пользователя - '),
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': 5 #input('Введите количество копируемых файлов - ')
        }

    def get_users_data(self):
        url = '/photos.get'
        responce = requests.get(self.base_host + url, params=self.get_params()).json()
        return responce

    def preparation_users_data(self):
        source_list=VK.get_users_data(self)['response']['items']
        prepared_list = []
        #json_my=[]
        bar = IncrementalBar('###', max=len(source_list))
        #print(len(source_list))
        for it in source_list:
            _json_my = []
            #time.sleep(0.2)
            bar.next()
            time.sleep(0.2)
            # _json_my={'file name': str(it['likes']['count'])+'.jpg',"size":it['sizes'][-1]['type']}
            # prepared_list.append((it['sizes'][-1]['url'],it['likes']['count'],_json_my))
            prepared_list.append((it['sizes'][-1]['url'],it['likes']['count']))#,_json_my))

        bar.finish()
        return(prepared_list)#,json_my)

class Yandex:

    base_host = 'https://cloud-api.yandex.net/'

    def __init__(self, TokenYA):
        self.TokenYA = TokenYA

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.TokenYA}'
        }

    def check_folder(self):
        folder_name = input("Укажите название папки, в которую необходимо сохранить файлы: ")
        #uri_upload = 'v1/disk/resources/upload'
        uri_folder = 'v1/disk/resources'
        path = {'path': folder_name}
        check_folder = requests.get(self.base_host + uri_folder, params=path)
        if check_folder.status_code == 401:
            folder = requests.put(self.base_host + uri_folder, params=path, headers=self.get_headers())
            #print(folder.status_code)
            #pprint(folder.json())
        return folder_name

    def upload_from_internet(self, prepared_list):
        uri_upload = 'v1/disk/resources/upload'
        folder_name = self.check_folder()
        bar = IncrementalBar('###', max=len(prepared_list))
        for item in prepared_list:
            params = {'url': item[0], 'path': f'/{folder_name}/{item[1]}.jpg'}
            response = requests.post(self.base_host + uri_upload, params=params, headers=self.get_headers())
            bar.next()
            #print(item[2])
            print(response.json())
        bar.finish()
        print('OK')

if __name__ == '__main__':
    vk = VK(TokenVK)
    ya = Yandex(TokenYA)
#    pprint(vk.get_users_data())
#    pprint(vk.preparation_users_data())
    #ya.check_folder()
    ya.upload_from_internet(vk.preparation_users_data())
