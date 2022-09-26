from ..Module import *
from ..db_setting import *

# 商圈註冊
def shopping_area_create(name, eg_name, logo, banner, welcome, activity_rule, convert_prize_rule, lottery_method, shop_list, lottery_level_num, repeat_pass, verification_method, prize_list=None):
    # 搜尋是否以擁有將註冊之商圈英文名字
    select_eg_name_q = f"select shopping_area_eg_name from shopping_area.shopping_area_infor where shopping_area_eg_name = '{eg_name}'"
    have_eg_name = mysql_engine.execute(select_eg_name_q).fetchone()

    if have_eg_name == None:
        sql_cmd = f"INSERT INTO shopping_area_infor (shopping_area_name, shopping_area_eg_name, shopping_logo, shopping_banner, welcome_text, activity_rule, convert_prize_rule, lottery_level_num, repeat_pass, verification_method, lottery_method) VALUES ('{name}','{eg_name}','{logo}','{banner}','{welcome}','{activity_rule}','{convert_prize_rule}','{lottery_level_num}','{repeat_pass}','{verification_method}','{lottery_method}')"
        shopping_engine.execute(sql_cmd)
        mysql_engine.execute(
            f"CREATE DATABASE ShopArea_{eg_name}")  # 建立database
        mysql_engine.execute(
            f"alter database ShopArea_{eg_name} character set utf8;")  # 設定datebase字串編碼
        # 創建商圈資料庫
        globals()[f'{eg_name}_engine'] = create_engine(
            f"mysql+pymysql://{sql_user}:{sql_password}@{sql_ip}:3306/ShopArea_{eg_name}")
        globals()[f'{eg_name}_engine'].execute('create table shop( id serial not null primary key, shop_name varchar(20) not null, shop_id varchar(80) not null, shop_address varchar(255) not null, shop_phone varchar(20) not null, shop_qrcode longblob not null, shop_introduction varchar(300) not null, lineOA_path varchar(255) not null, Engagement INT(255) not null);')
        globals()[f'{eg_name}_engine'].execute(
        'create table run_level( id serial not null primary key, user_id varchar(20) not null, shop_id varchar(80) not null);')
        if lottery_method == '0':
            globals()[f'{eg_name}_engine'].execute(
                'create table lottery_user( id serial not null primary key, user_name varchar(20) not null, user_id varchar(20) not null, lottery_id varchar(20) not null);')
        elif lottery_method == '1':
            globals()[f'{eg_name}_engine'].execute(
                'create table prize( id serial not null primary key, prize varchar(80) not null, prize_probability INT(20) not null, all_quantity INT(20) not null, last_quantity INT(20) not null);')
            globals()[f'{eg_name}_engine'].execute(
                'create table lottery_user( id serial not null primary key, user_id varchar(20) not null, lottery_num INT(20) not null);')
            # 植入獎品至獎品資料庫
            all_probability = 100
            for prizes in prize_list:
                prize = prizes['prize']
                prize_probability = prizes['prize_probability']

                all_probability = all_probability - int(prize_probability)  # 計算全部獎品總和機率是否為100 若不及100須將剩餘機率新增銘謝惠顧選項

                all_quantity = prizes['all_quantity']
                sql_cmd = f"INSERT INTO shoparea_{eg_name}.prize (prize, prize_probability, all_quantity, last_quantity) VALUES ('{prize}','{prize_probability}','{all_quantity}','{all_quantity}')"
                mysql_engine.execute(sql_cmd)
            if prize_probability > 0 :
                sql_cmd = f"INSERT INTO shoparea_{eg_name}.prize (prize, prize_probability, all_quantity, last_quantity) VALUES ('{'銘謝惠顧'}','{all_probability}','{100}','{100}')"
                mysql_engine.execute(sql_cmd)

        sql_cmd = f"ALTER TABLE user.run_level_number ADD COLUMN {eg_name}_num INT(20) not null"
        mysql_engine.execute(sql_cmd)
        # ------------------------------------------

        # 建立商圈管理者帳號密碼 預設密碼：mindnodeair_{ShoppingArea_en_name}
        # password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15) )#亂碼
        hashpassword = hash_password(f'mindnodeair_{eg_name}')
        sql_cmd = f"INSERT INTO shopping_area.admin_member (account, password, control) VALUES ('{eg_name}','{hashpassword}', '{0}')"
        mysql_engine.execute(sql_cmd)

        # 建立商圈logo暫存區 以利qrcode生成
        if not os.path.isdir(shopping_area_data_path):
            os.makedirs(shopping_area_data_path)
        if not os.path.isdir(shopping_area_data_path + '/image'):
            os.makedirs(shopping_area_data_path + '/image')
        if not os.path.isdir(shopping_area_data_path + '/qrcode'):
            os.makedirs(shopping_area_data_path + '/qrcode')

        # 商圈logo暫存
        im = Image.open(BytesIO(base64.b64decode(logo.split(',')[1])))
        im.save(shopping_area_data_path + '/image'+f'/{eg_name}.png')

        # 將商店list增加到商圈裡的shop_Table
        for shop_infor in shop_list:
            shop_address = shop_infor['shop_address']
            shop_id = shop_infor['shop_id']
            shop_name = shop_infor['shop_name']
            shop_phone = shop_infor['shop_phone']
            shop_introduction = shop_infor['shop_introduction']
            lineOA_path = str(shop_infor['lineOA_path'])

            # 生成店家QRcode
            myqr.run(words=f'{shop_id}',  # 可放網址或文字(限英文)
                     picture=shopping_area_data_path + \
                     '/image'+f'/{eg_name}.png',
                     version=5,  # QR Code的邊長，越大圖案越清楚
                     level='H',  # 糾錯水平，預設是H(最高)
                     colorized=True,  # 背景圖片是否用彩色，True為彩色
                     save_name=shopping_area_data_path + '/qrcode' + f'/{eg_name}_qrcode.png')  # 儲存檔案名稱

            with open(shopping_area_data_path + '/qrcode' + f'/{eg_name}_qrcode.png', "rb") as image_file:
                qrcode_base64 = base64.b64encode(image_file.read())

            qrcode_base64 = 'data:image/png;base64,' + \
                qrcode_base64.decode('utf-8')
            sql_cmd = f"INSERT INTO shop (shop_name, shop_id, shop_address, shop_phone,shop_qrcode,shop_introduction,lineOA_path,Engagement) VALUES ('{shop_name}','{shop_id}','{shop_address}','{shop_phone}','{qrcode_base64}','{shop_introduction}','{lineOA_path}','{0}')"
            globals()[f'{eg_name}_engine'].execute(sql_cmd)

        # 清空暫存資料夾
        shutil.rmtree(shopping_area_data_path + '/image')
        shutil.rmtree(shopping_area_data_path + '/qrcode')
        os.mkdir(shopping_area_data_path + '/image')
        os.mkdir(shopping_area_data_path + '/qrcode')

        return {'code': 200, 'message': '已完成註冊'}, 200
    else:
        return {'code': 400, 'message': '商圈英文名字已被註冊'}, 400

# 商圈資訊
def select_shopping_area_info(shop_area_en_name):
    if shop_area_en_name != 'all':
        select_en_name_q = f"select * from shopping_area_infor where shopping_area_eg_name = '{shop_area_en_name}'"
        have_en_name = shopping_engine.execute(select_en_name_q).fetchone()
        if have_en_name != None:
            shopping_area_name = have_en_name['shopping_area_name']
            shopping_area_eg_name = have_en_name['shopping_area_eg_name']
            shopping_logo = have_en_name['shopping_logo'].decode('utf-8')
            shopping_banner = have_en_name['shopping_banner'].decode('utf-8')
            welcome_text = have_en_name['welcome_text']
            activity_rule = have_en_name['activity_rule']
            convert_prize_rule = have_en_name['convert_prize_rule']
            lottery_level_num = have_en_name['lottery_level_num']
            lottery_method = have_en_name['lottery_method']
            repeat_pass = have_en_name['repeat_pass']
            verification_method = have_en_name['verification_method']

            # 替代 \n 為 <br/>
            welcome_text = welcome_text.replace('\n', '<br/>')
            activity_rule_html = activity_rule.replace('\n', '<br/>')
            convert_prize_rule_html = convert_prize_rule.replace('\n', '<br/>')

            select_shop_list_q = f"SELECT * FROM shoparea_{shop_area_en_name}.shop;"
            df = pd.read_sql(select_shop_list_q, con=shopping_engine)
            df['shop_qrcode'] = df['shop_qrcode'].map(
                lambda x: x.decode('utf-8'))
            shop_list = df.to_dict(orient='records')
            #shop_list = shopping_engine.execute(select_shop_list_q).mappings().all()
            rejson = {'shopping_area_name': shopping_area_name, 'shopping_area_eg_name': shopping_area_eg_name, 'shopping_logo': shopping_logo, 'shopping_banner': shopping_banner, 'welcome_html': welcome_text, 'activity_rule_html': activity_rule_html, 'convert_prize_rule_html': convert_prize_rule_html,
                      'activity_rule_text': activity_rule, 'convert_prize_rule_text': convert_prize_rule, 'lottery_level_num': lottery_level_num, 'lottery_method': lottery_method, 'repeat_pass': repeat_pass, 'verification_method': verification_method, 'shop_list': shop_list}
            return rejson
        else:
            return {'code': 400, 'message': '無此商圈名稱'}, 400
    elif shop_area_en_name == 'all':
        select_shoparea_list_q = "select * from shopping_area.shopping_area_infor"
        rejson = shopping_engine.execute(select_shoparea_list_q)
        rejson = execute_to_list(rejson)
        data = []
        for i in rejson:
            i = dict(i)
            i['shopping_logo'] = i['shopping_logo'].decode('utf-8')
            i['shopping_banner'] = i['shopping_banner'].decode('utf-8')
            data.append(i)
        return jsonify(data), 200


# 商圈列表
def select_shopping_area_list():
    select_area_list_q = "select shopping_area_name,shopping_area_eg_name from shopping_area_infor"
    rejson = shopping_engine.execute(select_area_list_q)

    return jsonify(execute_to_list(rejson))

# 修改商圈基本資訊
def update_shopping_area_info_f(name, en_name, banner, welcome, activity_rule, convert_prize_rule, lottery_level_num):
    update_shopping_info_q = f"UPDATE shopping_area.shopping_area_infor SET \
        shopping_area_name = '{name}',\
        shopping_banner = '{banner}',\
        welcome_text = '{welcome}',\
        activity_rule = '{activity_rule}',\
        convert_prize_rule = '{convert_prize_rule}',\
        lottery_level_num = '{lottery_level_num}'\
        WHERE \
        shopping_area_eg_name = '{en_name}'"
    print(banner)
    mysql_engine.execute(update_shopping_info_q)
    return {'message': '修改完成'}, 200

def select_shopping_area_prize_list(en_name):
    select_prize_list_q = f"select prize from shoparea_{en_name}.prize"
    prize_list = mysql_engine.execute(select_prize_list_q)
    prize_list = execute_to_list(prize_list)
    return jsonify(prize_list)