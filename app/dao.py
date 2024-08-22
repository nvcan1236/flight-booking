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