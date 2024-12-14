from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread']
    _description = "Hospital Patient"
    # _order = "id desc"

    p_sequence = fields.Char(string='Sequence',defalut= lambda self:_(''))
    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    is_child = fields.Boolean(string="Is Child")
    gender = fields.Selection([('male', 'Male'),('female', 'Female'),]
                              , required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string="Status", tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    image = fields.Binary(string="Patient Image")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    appointment_count = fields.Integer(string='Appointment Count', compute="compute_appointment_count" )

    @api.model_create_multi
    def create(self,vals):
        for val in vals:
            val['p_sequence'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient,self).create(vals)
    @api.onchange('age')
    def onchange_age(self):
        if self.age <= 10:
            self.is_child = True
        else:
            self.is_child = False

    @api.constrains('is_child', 'age')
    def check_child_age(self):
        if self.is_child and self.age == 0:
            raise ValidationError('The age has to be recorded !')

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            print(rec.id)

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def compute_appointment_count(self):
        for rec in self:
            appointments_num = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])  # search will return objs
            rec.appointment_count = appointments_num
