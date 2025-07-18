from odoo import models, fields, api

class UserModel(models.Model):
    _name = 'user'
    _description = 'User'

    user_name = fields.Char(
        string='User Name',
        required=True,
        size=100,
        default=None,
        help='Unique identifier for the user, maximum 100 characters',
    )

    password = fields.Char(
        string='Password',
        required=True,
        size=100,
        default=None,
        help='Password for the user, maximum 100 characters',
    )

    role = fields.Char(
        string='Role',
        required=True,
        size=50,
        default='user',
        help='Role of the user, default is "user", maximum 50 characters'
    )