import hashlib

from sqlalchemy import func
from flask import session
from app import db, utils
from app.models import SanBay, TuyenBay, ChuyenBay, HangVe, NguoiDung, HanhKhach, Ve, HoaDon, QuyDinh, Ghe, DungChan
from cloudinary import uploader


def get_flight_by_id(id=None):
    return ChuyenBay.query.get(id)


def get_flights(ready=False):
    return ChuyenBay.query.filter(ChuyenBay.san_sang.__eq__(ready)).all()


def get_routes():
    return TuyenBay.query.all()


def search_flight(from_code, to_code, date=None, ready=False):
    t = TuyenBay.query.filter(TuyenBay.sanBayKhoiHanh_id.__eq__(from_code),
                              TuyenBay.sanBayDen_id.__eq__(to_code))
    if t.first():
        if date:
            ds_chuyenbay = ChuyenBay.query.filter(ChuyenBay.san_sang == True,
                                                  ChuyenBay.tuyenbay_id.__eq__(t.first().id),
                                                  func.DATE(ChuyenBay.gio_bay) == date)
            return ds_chuyenbay.all()
        else:
            ds_chuyenbay = ChuyenBay.query.filter(ChuyenBay.san_sang == True,
                                                  ChuyenBay.tuyenbay_id.__eq__(t.first().id))
            return ds_chuyenbay.all()
    else:
        return []


def get_user_by_id(user_id):
    return NguoiDung.query.get(user_id)


def check_exist_user(username):
    user = NguoiDung.query.filter(NguoiDung.username.__eq__(username.strip())).first()
    if user:
        return True
    else:
        return False


def create_user(username, email, password, name, avatar=None):
    u = NguoiDung()
    u.name = name
    u.email = email
    u.username = username
    u.password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    if avatar:
        avatar_result = uploader.upload(avatar)
        u.avatar = avatar_result['secure_url']

    db.session.add(u)
    db.session.commit()


def check_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = NguoiDung.query.filter(NguoiDung.username.__eq__(username.strip())).first()

    if u:
        if u.password == password:
            return u
        else:
            raise Exception("Sai mật khẩu!!!")
    else:
        raise Exception("Người dùng không tồn tại")
