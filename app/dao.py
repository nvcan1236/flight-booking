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


def get_airports():
    return SanBay.query.all()


def get_scheduled_fllights():
    scheduled_fllights = ChuyenBay.query.filter(ChuyenBay.san_sang.__eq__(False))
    return scheduled_fllights.all()


def get_airport_by_id(id):
    return SanBay.query.get(id)


def get_ticket_class_by_id(id=None):
    return HangVe.query.get(id)


def create_ticket(flight_id, ticket_class_id, customer_id, bill_id):
    t = Ve(hangve_id=ticket_class_id, chuyenbay_id=flight_id, hanhkhach_id=customer_id, hoadon_id=bill_id)
    flight = get_flight_by_id(flight_id)
    ticket_class = get_ticket_class_by_id(ticket_class_id)
    t.tong_tien_ve = flight.gia + ticket_class.gia

    ghe = Ghe.query.filter(Ghe.chuyenbay_id.__eq__(flight_id),
                           Ghe.hangve_id.__eq__(ticket_class_id)).first()
    ghe.so_luong -= 1
    db.session.add(t)
    db.session.add(ghe)
    db.session.commit()
    return t
