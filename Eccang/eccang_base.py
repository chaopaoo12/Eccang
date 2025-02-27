import time
import hashlib
import json
import requests
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


def mk_sign(params, Secret_Key):
    sign_str = mk_str(params, Secret_Key)
    params = md5_sign(params, sign_str)
    return (sign_str, params)


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


    def get_data(self, interface_name, biz_content, to_json=None, data_format='json', silence=True):

        biz_content = {k:v for k,v in biz_content.items() if len(str(v)) > 0 and v is not None}

        if len(biz_content) > 0:
            page = int(biz_content.get('page'))
            page_size = int(biz_content.get('page_size'))
        else:
            page = 1
            page_size = 100

        target_page = 2
        result = []
        retry_count = 0
        max_retry_count = 99999

        while page <= target_page and retry_count < max_retry_count:
            print("page: ", page)
            biz_content['page'] = page
            self.build_connect(interface_name, biz_content)

            sign_str, params1 = mk_sign(self.params, self.Secret_Key)

            data = post_request(params1)

            if silence == False and page == 1:
                try:
                    print("加密串: ", sign_str)
                    print("参数列表: ", params1)
                    print("respose_data: ", data.text)
                    print("request_body: ", data.request.body)
                except:
                    pass

            try:
                data = data.json()
            except:
                #print(data.text)
                data = {'code': data.text}

            if data.get('code') == '<h3 align="center">请求频率超限，请控制请求速度</h3>\n':
                print("请求频率超限，请控制请求速度")
                retry_count += 1
                time.sleep(10)
                continue
            elif data.get('code') == "common.error.code.9999":
                try:
                    print("加密串: ", sign_str)
                    print("参数列表: ", params1)
                    print("request_body: ", data.request.body)
                    print("Error: ", data.text)
                    print("系统异常")
                except:
                    pass
                retry_count += 1
                time.sleep(10)
                continue
            elif data.get('code') == "300":
                try:
                    print("加密串: ", sign_str)
                    print("参数列表: ", params1)
                    print("Error: ", data)
                    print("request_body: ", data.request.body)
                except:
                    pass
                retry_count += 1
                time.sleep(10)
                continue
            elif data.get('code') == "common.error.code.0028":
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
            elif data.get('code') == "saas.api.error.code.0049":
                print('加密过期')
                print("加密串: ", sign_str)
                print("参数列表: ", params1)
                print("respose_data: ", data)
                print("request_body: ", data.request.body)
                print("Error: ", data.text)
                continue
            else:

                res = json.loads(data['biz_content'])
                retry_count = 0
                if isinstance(res, list):
                    record_num = len(res)
                    target_page = 1
                else:
                    if page == 1:
                        try:
                            try:
                                record_num = int(data['total'])
                            except:
                                pass

                            try:
                                record_num = int(res['total'])
                            except:
                                pass

                            try:
                                record_num = int(data['count'])
                            except:
                                pass

                            try:
                                record_num = int(res['count'])
                            except:
                                pass

                            try:
                                record_num = int(data['total_count'])
                            except:
                                pass

                            try:
                                record_num = int(res['total_count'])
                            except:
                                pass

                            target_page = ceil(record_num/page_size)
                        except:
                            print("No total/count/total_count")
                            if interface_name == 'getPutAwayList':
                                record_num = len(res['data_list'])
                            else:
                                record_num = len(res['data'])
                            target_page = 1
                        print("Total page: ", target_page)
                try:
                    if isinstance(res, list):
                        result.append(res)
                    elif interface_name == 'getPutAwayList':
                        result.append(res['data_list'])
                    elif isinstance(res['data'], dict):
                        result.append(res['data'])
                    else:
                        result.extend(res['data'])
                except:
                    print(res)

                page += 1

        if record_num == len(result):
            print("Total: ", len(result), " Success!")
        else:
            print("result: ", len(result), "target_page: ", record_num, " Error!")

        if data_format == 'json':
            return result
        elif data_format == 'dataframe':

            if len(result) > 1 and isinstance(result, list):
                result = pd.DataFrame(result)
            elif len(result) == 1 and isinstance(result, list):
                try:
                    result = pd.DataFrame(result[0])
                except:
                    result = pd.DataFrame([list(result[0].values())], columns=list(result[0].keys()))
            elif len(result) == 1 and isinstance(result, dict):
                result = pd.DataFrame([list(result.values())], columns=list(result.keys()))
            elif len(result) == 1:
                result = pd.DataFrame(result)
            else:
                result = pd.DataFrame(result)

            if to_json is not None and len(to_json) > 0 and data_format == 'dataframe' and result.shape[0] > 0:
                for i in to_json:
                   result[i] = result[i].apply(lambda x: json.dumps(x,indent=2,ensure_ascii=False))

            return result
