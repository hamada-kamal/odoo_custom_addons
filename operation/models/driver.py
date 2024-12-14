from odoo import fields, models


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    _description = "This is Res Partner Inherit Model"

    business_entity = fields.Selection([
        ('vip', 'Vip'),
        ('green taxi', 'Green Taxi'),
        ('limousine', 'Limousine'),
    ])

    is_driver = fields.Boolean(default=False)