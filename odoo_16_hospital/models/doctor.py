from odoo import api, fields, models, _
# from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _rec_name = 'name'
    _inherit = ['mail.thread']
    _description = "Hospital Doctor"

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([('male', 'Male'),
                             ('female', 'Female'),], required=True, default='male', tracking=True)
    active = fields.Boolean(default=True)
    def name_get(self):
        reslut = []
        for record in self:
            reslut.append((record.id,f'Dr.{record.name}'))
        return reslut