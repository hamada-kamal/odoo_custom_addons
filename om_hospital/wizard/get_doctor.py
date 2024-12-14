from odoo import api, fields, models


class GetDoctorWizard(models.TransientModel):
    _name = 'get.doctor.wizard'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    name = fields.Char(string='Name', required=True, tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)

    # active = fields.Boolean(default=True)
    # assign_date = fields.Date(default=fields.Date.today)
    # ref = fields.Char(string='Reference', default=_("New"))

    @api.onchange('doctor_id')
    def onchange_doctor_id(self):
        doctor = self.env['hospital.doctor'].browse(self.doctor_id.id)
        self.name = doctor.name
        self.gender = doctor.gender

    def action_get_doctor(self):
        print("Doctor Get Done.")
        # doctor = self.env['hospital.doctor'].browse(self.doctor_id.id)
        # self.name = doctor.name
        # self.gender = doctor.gender
