from odoo import models, fields, api

from enum import Enum

class CountryAlias2Fields(Enum):
    id = "id"
    co = "code"
    na = "name"
    cd = 'create_date'
    wd = 'write_date'
    cu = 'create_uid'
    wu = 'write_uid'

class CountryFields2Labels(Enum):
    id = "ID"
    code = "Ma Quoc Gia"
    name = "Ten Quoc Gia"
    create_date = 'Ngày tạo'
    write_date = 'Ngày cập nhật'
    create_uid = 'Mã Người tạo'
    write_uid = 'Mã Người cập nhật'

class CountryModel(models.Model):
    _name = 'country'
    _description = 'Country'

    code = fields.Char(
        string='Mã quốc gia',
        required=True,
        size=100,
        default=None,
        help='Mã định danh duy nhất cho quốc gia, tối đa 100 ký tự',
    )

    name = fields.Char(
        string='Tên quốc gia',
        required=True,
        size=500,
        default=None,
        help='Tên đầy đủ của quốc gia, tối đa 500 ký tự',
    )