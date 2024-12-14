from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = "This is Account Move Inherit Model"

    counter_id = fields.Many2one('operation.counter')

