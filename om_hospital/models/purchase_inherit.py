from odoo import api,fields,models


class HospitalPurchase(models.Model):
    _inherit = 'purchase.order'

    purchase_code = fields.Char(string="Purchase Code")
    is_complete = fields.Boolean(string="Is Complete?")


class PurchaseProduct(models.Model):
    _inherit = 'product.template'

    tracking = fields.Selection(selection_add=[('hospital','Test')], ondelete={'hospital':'set default'})


class HospitalPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_code = fields.Char(string="Product Code")

