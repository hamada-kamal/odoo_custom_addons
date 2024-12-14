from odoo import fields, models


class City(models.Model):
    _name = 'operation.city'
    _description = "This Is City Model"

    name = fields.Char(required=True)