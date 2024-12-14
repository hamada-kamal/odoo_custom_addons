from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime


class CostType(models.Model):
    _name = 'cost.type'

    _sql_constraints = [
        ('day_value_check', 'CHECK(day > 0 AND day < 32)','The value of Day Field must be in range [1 - 31]')
    ]

    name = fields.Text(string='Name')
    code = fields.Text(string='Code')
    medical = fields.Boolean(string='Medical')
    housing = fields.Boolean(string='Housing')
    visa = fields.Boolean(string='Visa')
    manual = fields.Boolean(string='Manual')
    monthly_cost = fields.Integer(string='Monthly Cost',default=0)
    day = fields.Integer(string='Day',default=1)
    date_from = fields.Date(string='Date', default=fields.Date.today)
    status = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], default='draft')

    @api.constrains('medical', 'housing', 'visa', 'manual')
    def check_if_type_not_selected(self):
        if not (self.medical or self.housing or self.visa or self.manual):
            raise ValidationError("You Must Select Cost Type!")


    @api.onchange('medical')
    def onchange_medical(self):
        if self.medical:
            self.housing = False
            self.visa = False
            self.manual = False

    @api.onchange('housing')
    def onchange_housing(self):
        if self.housing:
            self.medical = False
            self.visa = False
            self.manual = False

    @api.onchange('visa')
    def onchange_visa(self):
        if self.visa:
            self.medical = False
            self.housing = False
            self.manual = False

    @api.onchange('manual')
    def onchange_manual(self):
        if self.manual:
            self.medical = False
            self.housing = False
            self.visa = False

    @api.constrains('medical','housing','visa','manual')
    def check_if_type_exists(self):
        if self.medical:
            type_count = self.env['cost.type'].search_count([('medical','=',True)])
            if type_count > 1:
                raise ValidationError('"medical" type already exists in the system')

        elif self.housing:
            type_count = self.env['cost.type'].search_count([('housing','=',True)])
            if type_count > 1:
                raise ValidationError('"housing" type already exists in the system')

        elif self.visa:
            type_count = self.env['cost.type'].search_count([('visa','=',True)])
            if type_count > 1:
                raise ValidationError('"visa" type already exists in the system')

        elif self.manual:
            type_count = self.env['cost.type'].search_count([('manual','=',True)])
            if type_count > 1:
                raise ValidationError('"manual" type already exists in the system')

    def set_draft(self):
        self.status = 'draft'
        self.monthly_cost = 0

    def set_confirm(self):
        self.status = 'confirm'
        if self.medical:
            self.monthly_cost = 10
        elif self.housing:
            self.monthly_cost = 20
        elif self.visa:
            self.monthly_cost = 30

    @staticmethod
    def is_today_target_day(date):
        return date.day == datetime.today().date().day

    @staticmethod
    def is_doctor_assign_date_matches(date,day):
        return date.day <= day

    def create_employee_cost_record(self, employee,cost_type):

        new_employee_cost = {
            'doctor_id': employee.id,
            'cost_type_id': cost_type.id,
            'cost': cost_type.monthly_cost,
            'date_from': cost_type.date_from,
        }

        self.env['employee.cost'].create(new_employee_cost)
        print("recorded created")

    @api.model
    def _cron_create_employee(self):
        visa_type = self.env['cost.type'].search([('name', '=', 'Visa')])
        if self.is_today_target_day(visa_type.date_from):
            doctors = self.env['hospital.doctor'].search([])
            for doctor in doctors:
                if self.is_doctor_assign_date_matches(doctor.assign_date, visa_type.day):
                    print("doctor: ",doctor.name)
                    self.create_employee_cost_record(doctor,visa_type)


