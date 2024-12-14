from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Trip(models.Model):
    _name = 'operation.trip'
    _description = "This Is Trip Model"

    pricing_id = fields.Many2one('operation.pricing')
    vehicle_id = fields.Many2one('fleet.vehicle', required=True)
    from_city = fields.Many2one('operation.city')
    to_city = fields.Many2one('operation.city')
    distance = fields.Float()
    price = fields.Float()

    @api.constrains('vehicle_id','from_city','to_city')
    def _check_vehicle_city(self):
        trip = self.pricing_id.trip_ids.filtered(
            lambda t: t.vehicle_id == self.vehicle_id
            and t.from_city == self.from_city
            and t.to_city == self.to_city
            )
        if len(trip) > 1:
            print("Bad Trip: ", trip.pricing_id.name,trip.vehicle_id,trip.from_city.name,trip.to_city.name)
            raise ValidationError("There are two trips with the same data!")
        if self.from_city == self.to_city:
            raise ValidationError("From and To cities must be different!")
        if not self.from_city or not self.to_city:
            raise ValidationError("From and To cities must have a city!")

    @api.constrains('distance','price')
    def _check_distance_price(self):
        if self.distance <= 0 or self.price <= 0:
            raise ValidationError("Distance and Price must be positive!")