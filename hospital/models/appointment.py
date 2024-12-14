from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime
from dateutil.relativedelta import relativedelta
import pytz



class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment desc"
    _rec_name = "date_appointment"

    def get_company_id(self):
        return self.env.user.company_id.id

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    department_id = fields.Many2one('hospital.department', string="Department", required=True,
                                    domain="[('active','=', True)]")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True,
                                domain="[('department_id','=', department_id)]")

    check_ids = fields.Many2many('hospital.check', string="Checks",
                                 domain="['|',('doctor_id','=', doctor_id),('doctor_id','=', False)]")

    state = fields.Selection([('cancel', 'Cancelled'), ('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done')], default='draft',
                             string="State")
    date_appointment = fields.Date(string="Date", default=fields.Date.today, required=True)
    start = fields.Datetime(string="Start")
    end = fields.Datetime(string="End", default=fields.Date.today)
    date_checkup = fields.Datetime(string="Check Up Time")
    note = fields.Text(string='Note')
    # reference_record = fields.Reference([('hospital.patient','Patient'),('hospital.doctor','Doctor')],string="Record")
    # department_id = fields.Many2one('hospital.department', string='Department', required=True)

    company_id = fields.Many2one('res.company', default=get_company_id)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    cost = fields.Monetary(string="Total Cost", currency_field='currency_id', compute='_calc_total_cost', store=True)
    ref = fields.Char(string='Reference', default=lambda self: _('New'))
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

    def _utc_to_tz(self, utc_date):
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        my_date = pytz.utc.localize(utc_date).astimezone(user_tz)
        # reformat the date
        new_tz = my_date.strftime("%Y-%m-%d %H:%M:%S")
        # str to datetime
        new_tz = fields.Datetime.from_string(new_tz)
        return new_tz

    @api.depends('check_ids')
    def _calc_total_cost(self):
        total = 0.0
        for rec in self:
            for check in rec.check_ids:
                total += check.cost
        self.cost = total

    @api.onchange('department_id')
    def onchange_department(self):
        self.doctor_id = False

    @api.onchange('doctor_id')
    def onchange_doctor(self):
        self.check_ids = False

    #{start:, end:}  {start:, end:}
    def _is_periods_not_intersection(self, period1, period2):
        if period1['start'] != period2['start']:
            return True
        else:
            return (period1['end'] + relativedelta(hours=3)).time() <= (
                    period2['start'] + relativedelta(hours=3)).time()

    def _is_date_equal(self, start_date, end_date):
        return start_date.date() == end_date.date()

    def _is_valid_time(self, start_date, end_date):
        return (start_date + relativedelta(hours=3)).time() < (end_date + relativedelta(hours=3)).time()

    @api.constrains('start', 'end')
    def _check_start_end_dates(self):
        if not self._is_date_equal(self.start, self.end):
            raise ValidationError("Start and end date must be the same!")
        if not self._is_valid_time(self.start, self.end):
            raise ValidationError("Start time must be less than the end time!")

    @api.model
    def create(self, vals):
        rec_count = self.env['hospital.appointment'].search_count([
            ('patient_id', '=', vals['patient_id']),
            ('date_appointment', '=', vals['date_appointment']),
            ('department_id', '=', vals['department_id'])
        ])
        vals['start'] = fields.Datetime.from_string(vals['start'])

        if rec_count > 0:
            raise ValidationError(
                _("there's an appointment for this patient with the same (date, department) already exists!"))

        # rec_count = 0
        # apps = (self.env['hospital.appointment'].search([])
        #              .filtered(lambda x: x.start.date() == fields.Datetime.from_string(vals['start']).date() and
        #                                  (x.start + relativedelta(hours=3)).time() >= (
        #                                          fields.Datetime.from_string(vals['start']) + relativedelta(hours=3)).time() <= (
        #                                          x.end + relativedelta(hours=3)).time() and (
        #                                          x.state == 'draft' or x.state == 'confirm')))
        # print("\nappointments =  ", apps)
        vals['ref'] = self.env['ir.sequence'].next_by_code('appointment_sequence_code')
        res = super(HospitalAppointment, self).create(vals)
        # print(res.date_appointment, vals['date_appointment'])
        return res

    def write(self, vals):
        rec_count = 0
        # appointment = self.env['hospital.appointment'].browse(self.id)
        # print("appointment: ",appointment.date_appointment,appointment.patient_id)
        if 'date_appointment' in vals.keys():
            print(self.date_appointment, vals['date_appointment'])
            rec_count = self.env['hospital.appointment'].search_count([
                ('patient_id', '=', self.patient_id.id),
                ('date_appointment', '=', vals['date_appointment']),
                ('department_id', '=', self.department_id.id)
            ])

        # print("rec_count: ", rec_count)
        if rec_count > 0:
            raise ValidationError(
                "there's an appointment for this patient with the same (date, department) already exists!")
        res = super(HospitalAppointment, self).write(vals)
        # print("before vals: ", vals)
        return res

    def unlink(self):
        if self.state != 'cancel':
            raise ValidationError('You can not delete This appointment !!')
        return super(HospitalAppointment, self).unlink()

    def show_patient_data(self):
        return {
            'name': '',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.patient',
            'res_id': self.patient_id.id,
            'view_mode': 'form',
        }

    def show_doctor_data(self):
        return {
            'name': '',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.doctor',
            'res_id': self.doctor_id.id,
            'view_mode': 'form',
        }

    def show_department_data(self):
        return {
            'name': '',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.department',
            'res_id': self.department_id.id,
            'view_mode': 'form',
        }

    def _load_cost(self):
        pass

    def set_draft(self):
        self.state = 'draft'
        self.date_appointment = fields.Date.today()

    def show_invoice(self):
        return {
            'name': '',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_id.id
        }

    def create_invoice(self):
        invoice_obj = self.env['account.move']
        print(invoice_obj)
        for appointment in self:
            print("\n\n", appointment)
            invoice_vals = {
                'move_type': 'out_invoice',
                'appointment_id': appointment.id,  # or 'in_invoice' for vendor bills
                'patient_id': appointment.patient_id.id,  # Assuming the patient is linked to a partner
                'department_id': appointment.department_id.id,
                'doctor_id': appointment.doctor_id.id,
                'invoice_date': fields.Date.today(),
                # 'state': 'draft',
                'note': appointment.note,
            }
            invoice = invoice_obj.create(invoice_vals)
            print(invoice)
            print("id: ", invoice.appointment_id)
            print("patient_id: ", invoice.patient_id)
            print("department_id: ", invoice.department_id)
            print("doctor_id: ", invoice.doctor_id)
            print("state: ", invoice.state)
            print("cost: ", invoice.cost)
            print("note: ", invoice.note)
            appointment.invoice_id = invoice.id

    def set_confirm(self):
        self.state = 'confirm'
        self.create_invoice()
        print("recorded created")

    def set_done(self):
        self.state = 'done'
        self.date_checkup = datetime.date.today()

    def cancel_appointment_popup(self):
        return {
            'name': _('Cancel Appointment'),
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.appointment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_appointment_id': self.id,
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
                'default_date_appointment': self.date_appointment,
                'default_state': self.state,
            },
        }

    # Schedule Action Send Patient Mail
    @api.model
    def _cron_archive_patient(self):
        patient_ids = self.env['hospital.patient'].search([]).ids
        for p_id in patient_ids:
            appointments = (self.env['hospital.appointment'].search([('patient_id', '=', p_id)])
                            .sorted(key=lambda r: r.date_appointment, reverse=True))
            if appointments:
                last_date = appointments[0].date_appointment
                time_delta = fields.Date.today() - last_date
                days = time_delta.days
                if days >= 7:
                    patient = self.env['hospital.patient'].browse(p_id)
                    if patient:
                        patient.update({'active': False})


