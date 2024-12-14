from odoo import models, fields, api


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"

    appointment_id = fields.Many2one('hospital.appointment')
    patient_id = fields.Many2one('hospital.patient', string="Patient", readonly=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", readonly=True)
    date_appointment = fields.Date(string="Date", readonly=True)
    state = fields.Selection([('cancel', 'Cancelled'),('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done')], default='draft',
                             string="Status", readonly=True)

    def confirm_cancel_appointment(self):
        self.appointment_id.state = 'cancel'
