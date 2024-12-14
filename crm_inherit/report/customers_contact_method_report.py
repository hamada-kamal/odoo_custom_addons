from odoo import api,models


class CustomerPreferredContact(models.AbstractModel):
    _name = 'report.crm_inherit.report_contact_info'

    @api.model
    def _get_report_values(self, docids, data=None):
        # print("=======================")
        # print("docids: ",docids)
        customers = self.env['res.partner'].browse(docids)
        # print("customers: ",customers)
        # print("=======================")
        return {
            'customers': customers,
        }