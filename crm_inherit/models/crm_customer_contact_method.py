from odoo import api,models,fields


class CrmInherit(models.Model):
    _inherit = 'res.partner'

    contact_method = fields.Selection([
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('sms', 'SMS'),], string='Preferred Contact Method', default='email')
