from datetime import timedelta
import random
import string
from odoo import models, fields, api, _


def random_text(length=20):
    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=length))


class AccessToken(models.Model):
    _name = 'access.token'
    _description = 'Access Token'

    user_id = fields.Many2one('res.users', required=True)
    token = fields.Char(required=True)
    expiration_date = fields.Date(required=True)
    scope = fields.Char()

    def create_token(self, user_id=None):
        if not user_id:
            return None
        access_token = self.env['access.token'].create({
            'user_id': user_id,
            'scope': 'userinfo',
            'token': random_text(),
            'expiration_date': fields.Date.today + timedelta(days=1)
        })
        return access_token

    def find_or_create(self, user_id=None, create=False):
        if not user_id:
            user_id = self.env.user.id
        access_token = self.env['access.token'].sudo().search([('user_id', '=', user_id)], order='id DESC', limit=1)
        if not access_token and create:
            # create access token
            access_token = self.create_token(user_id=user_id)
        return access_token.token if access_token else None

    def has_expired(self):
        self.ensure_one()
        return fields.Date.today() > self.expiration_date

