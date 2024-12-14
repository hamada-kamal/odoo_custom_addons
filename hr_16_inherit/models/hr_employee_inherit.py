from odoo import api,fields,models


class HospitalSale(models.Model):
    _inherit = 'hr.employee'

    assign_date = fields.Date(string="Assign Date", default=fields.Date.today)