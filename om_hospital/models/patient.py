from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = 'mail.thread'

    name = fields.Char(string='Name', required = True, tracking=True)
    is_child = fields.Boolean(string = 'Is Child ?', tracking=True)
    notes = fields.Text(string='Notes', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female')], string = 'Gender', tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    capitalized_name = fields.Char(string='Capital Name', compute='_compute_capitalized_name')
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    ref = fields.Char(string='Reference', default=_("New"))
    tag_ids = fields.Many2many('res.partner.category',string="Tags")
    has_group_user = fields.Boolean(string='Has Group User', compute='_has_group_user')


    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals_list)

    @api.onchange('age')
    def onchange_age(self):
        self.is_child = True if self.age <= 10 else False

    @api.depends('name')
    def _compute_capitalized_name(self):
        for rec in self:
            rec.capitalized_name = rec.name.upper() if rec.name else ""

    @api.constrains('age')
    def _check_age(self):
        if self.age < 1:
            raise ValidationError(_("Age must be > 0"))

    # how to make field editable for a group of users
    @api.depends('has_group_user')
    def _has_group_user(self):
        self.has_group_user = self.env.user.has_group('om_hospital.low_level_users')
        print("set the value to ", self.has_group_user)