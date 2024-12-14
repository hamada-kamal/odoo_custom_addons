from odoo import api, fields, models, _

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = 'mail.thread'
    _rec_name = 'name'

    name = fields.Char(string='Name', required = True, tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female')], string = 'Gender', tracking=True)
    active = fields.Boolean(default=True)
    assign_date = fields.Date(default=fields.Date.today)

    ref = fields.Char(string='Reference', default=_("New"))

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['ref'] = self.env['ir.sequence'].next_by_code('hospital.doctor')
        return super(HospitalDoctor,self).create(vals_list)


    # def name_get(self):
    #     results = []
    #     for rec in self:
    #         name = f"{rec.name} - {rec.ref}"
    #         results.append((rec.id,name))
    #     return results