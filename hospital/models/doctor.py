from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _rec_name = 'full_name'
    _description = "Hospital Doctor desc"

    _sql_constraints = [('phone_constrains', 'UNIQUE(phone)', 'The phone already used!'),
                        ('code_constrains', 'UNIQUE(code)', 'The identity number already used!')]

    _parent_store = True
    _parent_name = "parent_id"

    first_name = fields.Char(string='First Name', required=True, copy=True, default="")
    last_name = fields.Char(string='Last Name', required=True, copy=True, default="")
    full_name = fields.Char(string='Name', compute='_get_full_name')
    gender = fields.Selection([('male','Male'),('female','Female')], string = 'Gender')
    active = fields.Boolean(default=True)
    phone = fields.Char(string='Phone', required=True, size=11, copy=False)
    code = fields.Char(string='Identity Number', required=True, size=16, copy=False)
    department_id = fields.Many2one('hospital.department', string="Department")
    parent_id = fields.Many2one('hospital.doctor', string="Manager")
    child_ids = fields.One2many('hospital.doctor', 'parent_id')
    # check_ids = fields.One2many('hospital.check', 'doctor_id')
    parent_path = fields.Char(index=True)

    @api.depends('full_name')
    def name_get(self):
        doctor_list = []
        for rec in self:
            doctor_list.append(
                (rec.id, "Dr/ " + rec.full_name)
            )
        return doctor_list


    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise ValidationError('Error! You cannot create manager.')

    @api.depends('first_name','last_name')
    def _get_full_name(self):
        for rec in self:
            rec.full_name = rec.first_name + ' ' + rec.last_name