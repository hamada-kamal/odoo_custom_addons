from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread']
    _description = "Hospital Appointment"

    name = fields.Char(string='Sequency', default=lambda self: _(''))
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    age = fields.Integer(string='Age', related='patient_id.age', tracking=True, store=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string="Status", tracking=True)
    # note = fields.Text(string='Description')
    date_appointment = fields.Date(string="Date",default = fields.Date.today)
    date_checkup = fields.Datetime(string="Check Up Time")
    # prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id',
    #                                         string="Prescription Lines")

    def action_share_whatsapp(self):
        print("Go whatsapp")
        if not self.patient_id.phone:
            raise ValidationError("missing patient phone number!")
        message = f"Hey {self.patient_id.name}, don't missing your appointment at {self.date_appointment}"
        whatsapp_api_url = f"https://api.whatsapp.com/send?phone={self.patient_id.phone}&text={message}"
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url,
        }

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('name', _('')) == _(''):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        res = super(HospitalAppointment, self).create(vals)
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            # if self.patient_id.note:
            #     self.note = self.patient_id.note
        else:
            self.gender = ''
            # self.note = ''