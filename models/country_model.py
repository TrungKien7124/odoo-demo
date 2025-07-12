from odoo import models, fields, api

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