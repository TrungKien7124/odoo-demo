from odoo import models, fields
from datetime import date, datetime


class SupplierModel(models.Model):
    _name = 'supplier'
    _description = 'du lieu nha cung cap'

    code = fields.Char(
        string='Mã nhà cung cấp',
        required=True,
        size=100,
        default=None,
        help='Mã định danh duy nhất cho nhà cung cấp, tối đa 100 ký tự',
    )

    alias = fields.Char(
        string='Tên viết tắt',
        required=True,
        size=500,
        default=None,
        help='Tên viết tắt của nhà cung cấp, tối đa 100 ký tự',
    )

    name = fields.Char(
        string='Tên nhà cung cấp',
        required=False,
        size=500,
        default=None,
        help='Tên đầy đủ của nhà cung cấp, tối đa 500 ký tự',
    )

    country_id = fields.Many2one(
        comodel_name='country',
        string='Quốc gia',
        required=True,
        help='Quốc gia của nhà cung cấp, liên kết với bảng country',
    )

    address = fields.Char(
        string='Địa chỉ',
        required=False,
        size=500,
        default=None,
        help='Địa chỉ của nhà cung cấp, tối đa 500 ký tự',
    )

    area_code = fields.Char(
        string='Mã vùng',
        required=False,
        size=100,
        default=None,
        help='Mã vùng của nhà cung cấp, tối đa 100 ký tự',
    )

    area_name = fields.Char(
        string='Tên vùng',
        required=False,
        size=100,
        default=None,
        help='Tên vùng của nhà cung cấp, tối đa 500 ký tự',
    )

    city_code = fields.Char(
        string='Mã thành phố',
        required=False,
        size=100,
        default=None,
        help='Mã thành phố của nhà cung cấp, tối đa 100 ký tự',
    )

    city_name = fields.Char(
        string='Tên thành phố',
        required=False,
        size=100,
        default=None,
        help='Tên thành phố của nhà cung cấp, tối đa 500 ký tự',
    )

    phone_number = fields.Char(
        string='Số điện thoại',
        required=False,
        size=40,
        default=None,
        help='Số điện thoại liên hệ của nhà cung cấp, tối đa 100 ký tự',
    )

    email = fields.Char(
        string='Email',
        required=False,
        size=100,
        default=None,
        help='Địa chỉ email liên hệ của nhà cung cấp, tối đa 100 ký tự',
    )

    website = fields.Char(
        string='Website',
        required=False,
        size=500,
        default=None,
        help='Địa chỉ website của nhà cung cấp, tối đa 500 ký tự',
    )

    tax_code = fields.Char(
        string='Mã số thuế',
        required=False,
        size=100,
        default=None,
        help='Mã số thuế của nhà cung cấp, tối đa 100 ký tự',
    )

    post_code = fields.Char(
        string='Mã bưu điện',
        required=False,
        size=100,
        default=None,
        help='Mã bưu điện của nhà cung cấp, tối đa 100 ký tự',
    )

    fax_number = fields.Char(
        string='Số fax',
        required=False,
        size=40,
        default=None,
        help='Số fax liên hệ của nhà cung cấp, tối đa 40 ký tự',
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Trường này không được trùng nhau.'),
        ('code_not_null', 'CHECK(code IS NOT NULL)',
         'Trường này không được để trống.'),
    ]

    alias_dict = {
        'id': 'id',
        'co': 'code',
        'al': 'alias',
        'na': 'name',
        'ci': 'country_id',
        'ad': 'address',
        'arc': 'area_code',
        'arn': 'area_name',
        'cc': 'city_code',
        'cn': 'city_name',
        'pn': 'phone_number',
        'em': 'email',
        'we': 'website',
        'tc': 'tax_code',
        'pc': 'post_code',
        'fn': 'fax_number',
        'cd': 'create_date',
        'wd': 'write_date',
        "cu": 'create_uid',
        "wu": 'write_uid',
    }

    label_dict = {
        'id': 'ID',
        'code': 'Mã nhà cung cấp',
        'alias': 'Tên viết tắt',
        'name': 'Tên nhà cung cấp',
        'country_id': 'Mã Quốc gia',
        'address': 'Địa chỉ',
        'area_code': 'Mã vùng',
        'area_name': 'Tên vùng',
        'city_code': 'Mã thành phố',
        'city_name': 'Tên thành phố',
        'phone_number': 'Số điện thoại',
        'email': 'Email',
        'website': 'Website',
        'tax_code': 'Mã số thuế',
        'post_code': 'Mã bưu điện',
        'fax_number': 'Số fax',
        'create_date': 'Ngày tạo',
        'write_date': 'Ngày cập nhật',
        'create_uid': 'Mã Người tạo',
        'write_uid': 'Mã Người cập nhật',
    }
