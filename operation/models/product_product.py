from odoo import fields, models, api


class Product(models.Model):
    _inherit = 'product.product'
    _description = "This is Product Inherit Model"

    vehicle_id = fields.Many2one('fleet.vehicle')

    @api.model
    def create(self, vals):
        res = super(Product, self).create(vals)
        res.product_tmpl_id.name = res.name
        return res

    @api.constrains('vehicle_id')
    def _check_vehicle_id(self):
        if self.vehicle_id:
            self.vehicle_id.product_id = self.id

    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        self.name = str(self.vehicle_id.license_plate) + "/" + str(self.vehicle_id.model_id.name) + "/" + str(self.vehicle_id.model_id.brand_id.name) if self.vehicle_id else ''
