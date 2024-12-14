from odoo import fields, models, api
from odoo.exceptions import ValidationError


class OperationalCenter(models.Model):
    _name = 'operation.operational.center'
    _inherit = ['mail.thread']
    _description = "This Is Operational Center Model"

    name = fields.Char(required=True, tracking=True)
    airport = fields.Boolean(default=False, tracking=True)
    other = fields.Boolean(default=False, tracking=True)
    include_barking = fields.Boolean(default=False, tracking=True)
    hall = fields.Integer(default=1, required=True, tracking=True)
    hall_ids = fields.One2many('operation.hall', 'center_id')
    hall_count = fields.Integer(default=0, compute='_get_total_hall')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], default='draft', tracking=True)

    @api.model
    def create(self, vals):
        res = super(OperationalCenter, self).create(vals)
        if res.state == 'confirm':
            res.create_halls(res.hall)
        return res

    def unlink(self):
        for hall in self.hall_ids:
            hall.unlink()
        return super(OperationalCenter, self).unlink()

    @api.constrains('hall')
    def _check_hall_number(self):
        if self.hall <= 0:
            raise ValidationError("Hall Number Must Be Positive!")

    def _get_total_hall(self):
        self.hall_count = len(self.hall_ids)

    def show_halls(self):
        return {
            'name': 'Halls',
            'type': 'ir.actions.act_window',
            'res_model': 'operation.hall',
            'view_mode': 'tree,form',
            'domain': [('center_id', '=', self.id)],
        }

    def show_parking(self):
        pass

    @api.onchange('airport')
    def onchange_airport(self):
        self.other = False if self.airport else True

    @api.onchange('other')
    def onchange_other(self):
        self.airport = False if self.other else True

    def create_halls(self, halls_no):
        for number in range(halls_no):
            hall_obj = self.env['operation.hall']
            vals = {
                'center_id': self.id,
                'name': f"{self.name} - hall {number + 1}"
            }
            new_hall = hall_obj.create(vals)

    def set_draft(self):
        halls = self.env['operation.hall'].search([('center_id','=',self.id)])
        for hall in halls:
            hall.unlink()
        self.state = 'draft'

    def set_confirm(self):
        self.state = 'confirm'
        self.create_halls(self.hall)


