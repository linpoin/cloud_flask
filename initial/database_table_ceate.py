
from sqlalchemy import create_engine
import sqlalchemy
import sqlalchemy.ext.automap
import sqlalchemy.orm
import sqlalchemy.schema
import urllib
from flask_bcrypt import Bcrypt


def run():
    sql_user = 'root'
    sql_ip = 'localhost'
    sql_password = urllib.parse.quote_plus('qazWSX!@#52643567')
    # 資料庫連線
    mysql_engine = create_engine(
        "mysql+pymysql://{}:{}@{}:3306".format(sql_user, sql_password, sql_ip))
    # 建立通道
    mysql_session = sqlalchemy.orm.Session(mysql_engine)

    # 建DataBase
    try:  # Uesr
        mysql_session.execute("CREATE DATABASE User")  # 建立database
        mysql_session.execute(
            "alter database User character set utf8;")  # 設定datebase字串編碼
        mysql_session.commit()
    except:
        pass
    try:  # admin_member
        mysql_session.execute("CREATE DATABASE Shopping_Area")  # 建立database
        mysql_session.execute(
            "alter database Shopping_Area character set utf8;")  # 設定datebase字串編碼
        mysql_session.commit()
    except:
        pass

    # 建立使用者相關Table
    Uesr_engine = create_engine(
        "mysql+pymysql://{}:{}@{}:3306/User".format(sql_user, sql_password, sql_ip))
    Uesr_session = sqlalchemy.orm.Session(Uesr_engine)
    Uesr_session.execute(
        'create table users( id serial not null primary key,name varchar(20) not null,password varchar(80) not null,phone varchar(20) not null,user_id varchar(20) not null,user_qrcode longblob not null);')
    Uesr_session.execute(
        'create table user_get_prize( id serial not null primary key, phone varchar(20) not null, shopping_area_en_name varchar(20) not null, prize varchar(80) not null, prize_id varchar(255) not null);')
    Uesr_session.execute(
        'create table run_level( id serial not null primary key, user_id varchar(20) not null, shop_id varchar(80) not null);')
    Uesr_session.execute(
        'create table run_level_number( id serial not null primary key, user_id varchar(20) not null);')

    # 建立商圈管理相關Table
    admin_engine = create_engine(
        "mysql+pymysql://{}:{}@{}:3306/Shopping_Area".format(sql_user, sql_password, sql_ip))
    admin_session = sqlalchemy.orm.Session(admin_engine)
    admin_session.execute('create table shopping_area_infor( id serial not null primary key,shopping_area_name varchar(20) not null,shopping_area_eg_name varchar(20) not null,shopping_logo longblob not null,shopping_banner longblob not null, welcome_text varchar(300) not null, activity_rule varchar(300) not null, convert_prize_rule varchar(300) not null, lottery_level_num int(10) not null, repeat_pass int(10) not null, verification_method int(10) not null, lottery_method int(10) not null);')
    admin_session.execute(
        'create table admin_member( id serial not null primary key,account varchar(20) not null,password varchar(80) not null, control INT(20) not null, token varchar(300));')

    root_id = 'root'
    root_password = 'qazWSX!@#52643567'
    bcrypt = Bcrypt()
    hashed_password = bcrypt.generate_password_hash(password=root_password).decode()
    #創建管理者帳號
    admin_session.execute(
        f"INSERT INTO admin_member (account, password, control) VALUES ('{root_id}','{hashed_password}','{0}')"
    )
