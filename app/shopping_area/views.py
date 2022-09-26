from flask import request
from flask import Blueprint
from .def_shopping_area import *

shopping_area = Blueprint('shopping_area', __name__)


@shopping_area.route('/')
def index():
    return 'shopping_area.hello'

# 商圈註冊
@shopping_area.route('/signup', methods=['POST'])
def shopping_area_signup():
    if request.method == 'POST':
        body_json = request.get_json()
        if 'shopping_area_name' in body_json.keys() and 'shopping_area_eg_name' in body_json.keys() and 'shopping_logo' in body_json.keys() and 'shopping_banner' in body_json.keys() and 'welcome_text' in body_json.keys() and 'activity_rule' in body_json.keys() and 'convert_prize_rule' in body_json.keys() and 'lottery_method' in body_json.keys() and 'shop_list' in body_json.keys() and 'lottery_level_num' in body_json.keys() and 'repeat_pass' in body_json.keys() and 'verification_method' in body_json.keys() and 'prize_list' in body_json.keys():
            name = body_json['shopping_area_name']
            eg_name = body_json['shopping_area_eg_name']
            logo = body_json['shopping_logo']
            banner = body_json['shopping_banner']
            welcome = body_json['welcome_text']
            activity_rule = body_json['activity_rule']
            convert_prize_rule = body_json['convert_prize_rule']
            lottery_method = body_json['lottery_method']
            shop_list = body_json['shop_list']
            lottery_level_num = body_json['lottery_level_num']
            repeat_pass = body_json['repeat_pass']
            verification_method = body_json['verification_method']
            prize_list = body_json['prize_list']

            return_me = shopping_area_create(name, eg_name, logo, banner, welcome, activity_rule, convert_prize_rule,
                                             lottery_method, shop_list, lottery_level_num, repeat_pass, verification_method, prize_list)
            return return_me
        else:
            error = {'code': 400,
                     'message': '請輸入完整資訊',
                     }
            return error, 400

# 商圈列表
@shopping_area.route('/list', methods=['GET'])
def shopping_area_list():
    if request.method == 'GET':
        return_me = select_shopping_area_list()
        return return_me

# 商圈資訊
@shopping_area.route('/<shop_area_en_name>', methods=['GET'])
def shopping_area_info(shop_area_en_name):
    if request.method == 'GET':
        return_me = select_shopping_area_info(shop_area_en_name)
        return return_me

# 修改商圈基本資訊
@shopping_area.route('/update/shopping_area_info', methods=['POST'])
def update_shopping_area_info():
    if request.method == 'POST':
        body_json = request.get_json()
        if 'name' in body_json.keys() and 'en_name' in body_json.keys() and 'banner' in body_json.keys() and 'welcome' in body_json.keys() and 'activity_rule' in body_json.keys() and 'convert_prize_rule' in body_json.keys() and 'lottery_level_num' in body_json.keys():
            name = body_json['name']
            en_name = body_json['en_name']
            banner = body_json['banner']
            welcome = body_json['welcome']
            activity_rule = body_json['activity_rule']
            convert_prize_rule = body_json['convert_prize_rule']
            lottery_level_num = body_json['lottery_level_num']
            return_me = update_shopping_area_info_f(
                name, en_name, banner, welcome, activity_rule, convert_prize_rule, lottery_level_num)
            return return_me
        else:
            return {'message': '傳送資料不完全'}, 400

# 當前商圈獎品列表
@shopping_area.route('/<shop_area_en_name>/prize_list', methods=['GET'])
def shopping_area_prize_list(shop_area_en_name):
    if request.method == 'GET':
        return_me = select_shopping_area_prize_list(shop_area_en_name)
        return return_me