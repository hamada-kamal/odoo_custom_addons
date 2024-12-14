from odoo import api,fields,models


class PurchaseReportInherit(models.Model):
    _inherit = 'purchase.report'

    is_complete = fields.Boolean(string="Is Complete?")

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        print("hi hi hi")
        res['is_complete'] = """ po.is_complete"""
        return res
