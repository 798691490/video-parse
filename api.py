import os
import time

import uuid
from flask import Flask, current_app, make_response,send_from_directory, jsonify, request
from werkzeug.routing import BaseConverter
import win_config

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

@app.after_request
def af_request(resp):
    """
     #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp

@app.route('/view/<regex("[a-zA-Z0-9]+"):uuid>/')
def view(uuid):
    """
    url: /view/1010000000125259/
    result: view uuid:1010000000125259
    """
    return "view uuid: %s" % (uuid)

@app.route('/<regex(".*"):url>')
def not_found(url):
    """
    url: /hello
    result: not found: 'hello'
    """
    print('----',url,'----')
    if '.html' in url:
        url = url
        path = os.getcwd()
        if url == 'index.html' or url == ' ' or url == '' or url == '  ':
            url = 'index.html'
            path = os.getcwd()
    else:
        try:
            url = url.split('/')[1]
        except:
            url = url
        path = os.path.join(os.getcwd(), 'tools\\')
    return send_from_directory(path, url)



# @app.route('/Buy', methods=['GET', 'POST'])
# def Buy():
#     phone = request.values.get('phone')
#     MD5 = request.values.get('MD5')
#     YZM = win_config.send_YZM(phone)
#     win_config.Upload_the_infoid(MD5, YZM)
#     return jsonify({
#             "msg": 'success',
#             "code": 0
#         })

@app.route('/Get_info', methods=['GET', 'POST'])
def Get_info():
    USERNAME = request.values.get('USERNAME')
    MD5 = request.values.get('MD5')
    DDH_NUM = request.values.get('DDH_NUM')
    PHONE_NUM = request.values.get('PHONE_NUM')
    YZM_NUM = request.values.get('YZM_NUM')
    BEIZHU = request.values.get('BEIZHU')
    VX_NUM = request.values.get('VX_NUM')
    QQ_NUM = request.values.get('QQ_NUM')
    if not win_config.DDH_cunzai(DDH_NUM):
        print('订单号不存在！')
        if win_config.duplicate_checking_key11(PHONE_NUM, YZM_NUM):
            print('验证码正确')
            win_config.Update_Download_state(YZM_NUM, PHONE_NUM)
            win_config.Upload_the_info(USERNAME, MD5, DDH_NUM, PHONE_NUM,BEIZHU, VX_NUM, QQ_NUM)
            print(1111)
            return jsonify({
                "msg": 'success',
                "code": 0
            })
        else:
            print('验证码不正确')
            return jsonify({
                    "msg": 'failed',
                    "code": -1
                })
    else:
        print('订单号存在！')
        return jsonify({
            "msg": 'failed',
            "code": -2
        })


@app.route('/Get_dingdan', methods=['GET', 'POST'])
def Get_dingdan():
    phone = request.values.get('PHONE_NUM')
    yanzhengma = request.values.get('YZM_phone')
    if win_config.duplicate_checking_key11(phone, yanzhengma):
        win_config.Update_Download_state(yanzhengma, phone)
        data_list = win_config.Get_dingdan_info(phone)
        return jsonify({
            "data": data_list,
            "msg": 'success',
            "code": 0
        })
    else:
        return jsonify({
            "msg": 'failed',
            "code": -1
        })

@app.route('/Get_YZM', methods=['GET', 'POST'])
def Get_YZM():
    phone = request.values.get('phone')
    YZM = win_config.send_YZM(phone)
    win_config.Upload_the_YZM(phone, YZM)

    return jsonify({
            "msg": 'success',
            "code": 0
        })

@app.route('/Get_shiyong', methods=['GET', 'POST'])
def Get_shiyong():
    phone = request.values.get('PHONE_NUM')
    yanzhengma = request.values.get('YZM_NUM')
    print(yanzhengma)
    print(phone)

    if win_config.duplicate_checking_key11(phone, yanzhengma):
        win_config.Update_Download_state(yanzhengma, phone)
        if win_config.shiyong_user_cunzai(phone):
            return jsonify({
                "msg": 'failed',
                "code": -2
            })
        else:
            win_config.Upload_the_shiyong_user(phone)
            Secret_key = uuid.uuid1().hex
            valid_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()) + 1800))
            whether_to_activate = '1'
            win_config.Upload_the_keyy(Secret_key, valid_time, whether_to_activate)
            return jsonify({
                "data": Secret_key,
                "msg": 'success',
                "code": 0
            })
    else:
        return jsonify({
            "msg": 'failed',
            "code": -1
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10009, debug=True)