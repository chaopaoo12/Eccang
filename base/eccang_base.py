import time
import hashlib
import json
import requests
import sys
from random import sample
from string import ascii_letters, digits
import pandas as pd
from math import ceil


def prepare_sign_str(params):
    sign_str = ""

    for i in params.items():
        if len(str(i[1])) > 0:
            if len(sign_str) > 0:
                if i[0] == "sign_type":
                    sign_str += "&" + str(i[0]) + "=" + str(i[1])
                else:
                    sign_str += "&" + str(i[0]) + "=" + str(i[1])
            else:
                sign_str += str(i[0]) + "=" + str(i[1])
    return sign_str.replace(" ", "")


def mk_str(params, Secret_Key):
    sign_str = (prepare_sign_str(params)+Secret_Key).replace("'", '"').replace('/',' ')
    return (sign_str)


def md5_sign(params, sign_str):
    sign_process = hashlib.md5()
    sign_process.update(sign_str.replace("'", '').encode('utf-8'))
    params['sign'] = sign_process.hexdigest().lower()
    return (params)


def post_request(params):

    post_url = 'http://openapi-web.eccang.com/openApi/api/unity'

    header = {
        "Content-Type": "application/json"
        }

    if len(params['biz_content']) > 0:
        params['biz_content'] = json.dumps(params['biz_content']).replace('"', '\"')
    request_body = json.dumps(params, ensure_ascii=False, indent=4, sort_keys=True).replace(' ', '').replace('/',' ').replace('\n', '\n\n')   ##.replace('"{', '{').replace('}"', '}')

    data = requests.post(post_url, headers=header, data=request_body)
    return (data)


class eccang():

    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            setting = json.load(file).get('ECCANG')

        self.app_key = setting.get('app_key')
        self.service_id = setting.get('service_id')
        self.Secret_Key = setting.get('Secret_Key')
        self.version = setting.get('version')


    def build_connect(self, interface_name, biz_content):
        self.params = {
            "app_key": self.app_key,
            "biz_content": biz_content,
            "charset": "UTF-8",
            "interface_method": interface_name,
            "nonce_str": ''.join(sample(ascii_letters+digits, 16)).lower(),
            "service_id": self.service_id,
            "sign_type": "MD5",
            "timestamp": str(int(round(time.time()*1000))),
            "version": self.version
        }


    def get_data(self, interface_name, biz_content, data_format='json'):

        if len(biz_content) > 0:
            page = int(biz_content.get('page'))
            page_size = int(biz_content.get('page_size'))
        else:
            page = 1
            page_size = 100

        target_page = 2
        result = []

        while page <= target_page:
            print("page: ", page)
            biz_content['page'] = page
            self.build_connect(interface_name, biz_content)

            sign_str = mk_str(self.params, self.Secret_Key)

            params1 = md5_sign(self.params, sign_str)
            data = post_request(params1)
            try:
                data = data.json()
            except:
                print("Error: ", data.text)

            if data.get('code') == "common.error.code.0028":
                print("加密串: ", sign_str)
                print("参数列表: ", params1)
                print("request_body: ", data.request.body)
                print("Error: ", data.text)
                break
            elif data.get('code') != "200":
                print("加密串: ", sign_str)
                print("参数列表: ", params1)
                print("respose_data: ", data)
                print("request_body: ", data.request.body)
                print("Error: ", data.text)
                break
            else:
                print(data)
                res = json.loads(data['biz_content'])

                if isinstance(res, list):
                    record_num = len(res)
                    target_page = 1
                else:
                    if page == 1:
                        try:
                            try:
                                record_num = int(res['total'])
                            except:
                                record_num = int(data['total_count'])
                            target_page = ceil(record_num/page_size)
                        except:
                            print("No total/total_count")
                            record_num = len(res['data'])
                            target_page = 1
                        print("Total page: ", target_page)
                if isinstance(res['data'], dict):
                    result.append(res['data'])
                else:
                    result.extend(res['data'])

                page += 1

        if record_num == len(result):
            print("Total: ", len(result), " Success!")
        else:
            print("result: ", len(result), "target_page: ", record_num, " Error!")
        if data_format == 'json':
            return result
        elif data_format == 'dataframe':
            return (pd.DataFrame(result))
