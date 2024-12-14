from odoo import api,fields,models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    city_code = fields.Char(string="City Code")


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    product_code = fields.Char(string="Product Code")


