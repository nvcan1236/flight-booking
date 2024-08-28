import hashlib

from sqlalchemy import func
from flask import session
from app import db, utils
from app.models import SanBay, TuyenBay, ChuyenBay, HangVe, NguoiDung, HanhKhach, Ve, HoaDon, QuyDinh, Ghe, DungChan
from cloudinary import uploader
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