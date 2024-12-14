import random

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'full_name'
    _order = 'full_name desc'
    _description = "this is the hospital patient's model"

    _sql_constraints = [('age_constrains', 'CHECK(age > 0)', 'The age must be a positive number.'),
                        ('phone_constrains','UNIQUE(phone)','The phone already used!'),
                        ('identity_number_constrains','UNIQUE(identity_number)','The identity number already used!')]

    first_name = fields.Char(string='First Name', required=True, copy=True, default="", translate=True)
    last_name = fields.Char(string='Last Name', required=True, copy=True, default="", translate=True)
    full_name = fields.Char(string='Name', compute='_get_full_name', translate=True)
    photo = fields.Binary(string='Photo', copy=False)
    age = fields.Integer(string='Age', copy=True)
    active = fields.Boolean(default=True)
    phone = fields.Char(string='Phone', required=True, size=11, copy=False)
    identity_number = fields.Char(string='Identity Number', required=True, size=16, copy=False)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', copy=True)
    is_child = fields.Boolean(string='Is Child ?', copy=True, compute='_is_child', store=True)
    appoinment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appoinments",
                                     context={'default_note': 'this is the default context value'},
                                     domain=[('state', '!=', 'cancel')])
    ref = fields.Char(string='Reference', default=lambda self: _('New'))



    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        domain = ['|', ('full_name', operator, name), ('phone', 'like', name), ('identity_number', 'like', name)]
        # domain = ['|', ('full_name', operator, name), ('identity_number', 'like', name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)

    # @api.constrains('phone')
    # def _check_phone(self):
    #     if self.phone <= 0:
    #         raise ValidationError('The age must be a positive number.')

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['ref'] = self.env['ir.sequence'].next_by_code('my_sequence_code')
        return super(HospitalPatient, self).create(vals)
    #
    # def write(self, vals):
    #     rec_count = 0
    #     if 'code' and 'phone' in vals.keys():
    #         rec_count = self.env['hospital.patient'].search_count([
    #             '|',
    #             ('phone', '=', vals['phone']),
    #             ('code', '=', vals['code']),
    #         ])
    #     elif 'code' in vals.keys():
    #         rec_count = self.env['hospital.patient'].search_count([
    #             ('code', '=', vals['code']),
    #         ])
    #     elif 'phone' in vals.keys():
    #         rec_count = self.env['hospital.patient'].search_count([
    #             ('phone', '=', vals['phone']),
    #         ])
    #
    #     # print("rec_count: ", rec_count)
    #     if rec_count > 0:
    #         raise ValidationError(
    #             "there's an appointment for this patient with the same (date, department) already exists!")
    #     res = super(HospitalAppointment, self).write(vals)
    #     # print("before vals: ", vals)
    #     return res

    @api.onchange('age')
    def onchange_age(self):
        self.is_child = True if self.age <= 10 else False

    @api.depends('age')
    def _is_child(self):
        for rec in self:
            rec.is_child = True if rec.age <= 10 else False

    @api.depends('first_name', 'last_name')
    def _get_full_name(self):
        for rec in self:
            rec.full_name = rec.first_name + ' ' + rec.last_name

    def make_appointment_from_patient(self):
        return {
            'name': "",
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'form',
            'context': {'default_patient_id': self.id},
        }

    #To deal with records that are related with an x2many relations
    def create_new_record(self):
         pass
        # exsisting_appointment = self.env['hospital.appointment'].search([],limit=1)
        # new_patient = super(HospitalPatient,self).create({
        #     'first_name': 'test',
        #     'last_name': 'test',
        #     'age': 55,
        #     'phone': random.randint(10,541548),
        #     'identity_number':random.randint(10,541548),
        #     'appoinment_ids':[exsisting_appointment.id],
        # })
        # return new_patient

    # def edit_existing_record(self):
    #     print("create demo patient")
    #
    # def remove_record_from_database(self):
    #     print("create demo patient")
    #
    # def remove_one_record_from_relational_field(self):
    #     print("create demo patient")
    #
    # def remove_all_record_from_relational_field(self):
    #     print("create demo patient")

    def open_excel_report_wizard(self):
        return {
            'name': 'Excel Report',
            'type': 'ir.actions.act_window',
            'res_model': 'appointment.excel.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
            }
        }