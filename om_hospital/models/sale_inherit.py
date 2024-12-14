from odoo import api,fields,models


class HospitalSale(models.Model):
    _inherit = 'sale.order'

    is_patient = fields.Boolean(string="Is Patient?")
    invoice_incoterm_id = fields.Many2one('account.incoterms',string="My Incoterm")
    city_code = fields.Char(string="City Code")
    def _prepare_invoice(self):
        invoice_vals = super(HospitalSale,self)._prepare_invoice()
        # print("invoice_vals: ",invoice_vals)
        invoice_vals['invoice_incoterm_id'] = self.invoice_incoterm_id.id
        invoice_vals.update({'city_code':self.city_code})
        return invoice_vals

    # def _prepare_invoice(self):
    #     invoice_vals = super(SaleOrder, self)._prepare_invoice()
    #     invoice_vals['journal_id'] = self.l10n_in_journal_id.id
    #     return invoice_vals


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('hospital','Test')])