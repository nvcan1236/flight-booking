import hashlib

from sqlalchemy import func
from flask import session
from app import db, utils
from app.models import SanBay, TuyenBay, ChuyenBay, HangVe, NguoiDung, HanhKhach, Ve, HoaDon, QuyDinh, Ghe, DungChan
from cloudinary import uploader

def load_regulation():
    regulations = {
        'Thời gian bay tối thiểu (phút)': 30,
        'Số sân bay trung gian tối đa': 2,
        'Thời gian dừng tối thiểu(phút)': 20,
        'Thời gian dừng tối đa(phút)': 30,
        'Số lượng hạng vé': 2,
        'Giá vé hạng 1': 800,
        'Giá vé hạng 2': 500,
        'Thời gian bán vé trước (giờ)': 4,
        'Thời gian đặt vé trước (giờ)': 12,
        'Số sân bay tối đa': 10
    }

    for (label, value) in regulations.items():
        r = QuyDinh(noi_dung=label, gia_tri=value)
        db.session.add(r)

    db.session.commit()


def get_regulations():
    regulation = QuyDinh.query.all()
    regulation_dict = {}
    for r in regulation:
        regulation_dict[r.noi_dung] = r.gia_tri
    return regulation_dict


def get_regulation_value(id):
    reg = QuyDinh.query.filter(QuyDinh.id.__eq__(id)).first()

    if reg:
        return reg.gia_tri


def set_regulation(id, new_value):
    regulation = QuyDinh.query.get(id)
    regulation.gia_tri = new_value
    db.session.add(regulation)
    db.session.commit()


def get_stats(from_date=None, to_date=None):
    if from_date and to_date:
        result = db.session.query(TuyenBay.id, TuyenBay.name, func.count(ChuyenBay.id), func.sum(Ve.tong_tien_ve)) \
            .join(ChuyenBay, TuyenBay.id == ChuyenBay.tuyenbay_id, isouter=True) \
            .filter(ChuyenBay.gio_bay.between(from_date, to_date)) \
            .join(Ve, ChuyenBay.id == Ve.chuyenbay_id) \
            .join(HoaDon, Ve.hoadon_id == HoaDon.id) \
            .filter(HoaDon.da_thanh_toan == True) \
            .group_by(TuyenBay.id) \
            .all()
    else:
        result = db.session.query(TuyenBay.id, TuyenBay.name, func.count(ChuyenBay.id), func.sum(Ve.tong_tien_ve)) \
            .join(ChuyenBay, TuyenBay.id == ChuyenBay.tuyenbay_id, isouter=True) \
            .join(Ve, ChuyenBay.id == Ve.chuyenbay_id) \
            .join(HoaDon, Ve.hoadon_id == HoaDon.id) \
            .filter(HoaDon.da_thanh_toan == True) \
            .group_by(TuyenBay.id) \
            .all()

    return result

def get_airports():
    return SanBay.query.all()


def get_scheduled_fllights():
    scheduled_fllights = ChuyenBay.query.filter(ChuyenBay.san_sang.__eq__(False))
    return scheduled_fllights.all()


def get_airport_by_id(id):
    return SanBay.query.get(id)


def get_airport_id(airport_name):
    airport = SanBay.query.filter(SanBay.name.__eq__(airport_name)).first()
    return airport.id


def get_airport_name(id):
    return SanBay.query.get(id).name


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
