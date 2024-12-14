from odoo import fields,models,api



class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"

    name = fields.Char(string='Sequency', default=lambda self: '')
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    age = fields.Integer(string='Age', related='patient_id.age', tracking=True, store=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string="Status", tracking=True)

    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Check Up Time")


    def create_appointment(self):
        print("from wiz python")
        new_appointment = {
            'patient_id': self.patient_id.id,
            'doctor_id': self.doctor_id.id,
            'age': self.age,
            'gender': self.gender,
            'state': self.state,
            'date_appointment': self.date_appointment,
            'date_checkup': self.date_checkup,
        }
        appointment_rec = self.env['hospital.appointment'].create(new_appointment)
        return {
            'name': 'Create Appointment From Python Function Action',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
            'type': 'ir.actions.act_window',
        }


    def get_patient_appointments(self):
        # # method1
        # action = self.env.ref("om_hospital.appointment_action").read()[0]
        # action["domain"] = [('patient_id','=',self.patient_id.id)]
        # return action

        # # method2
        # action = self.env['ir.actions.actions']._for_xml_id("om_hospital.appointment_action")
        # action["domain"] = [('patient_id','=',self.patient_id.id)]
        # return action
        return {
            'name': 'Get Patient Appointments',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.patient_id.id)],
            'type': 'ir.actions.act_window',
        }