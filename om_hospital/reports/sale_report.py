from odoo import api,fields,models


class SaleReportInherit(models.Model):
    _inherit = 'sale.report'

    is_patient = fields.Boolean(string="Is Patient?")
    city_code = fields.Char(string="City Code")
    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['is_patient'] = f""" s.is_patient """
        res['city_code'] = f""" s.city_code """
        return res
