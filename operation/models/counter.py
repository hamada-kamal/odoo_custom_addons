from odoo import fields, models, api
from odoo.exceptions import ValidationError
import base64
import io
import qrcode


class Counter(models.Model):
    _name = 'operation.counter'
    _inherit = ['mail.thread']
    _description = "This Is Counter Model"
    _rec_name = "customer_name"

    customer_name = fields.Many2one('res.partner', required=True)
    qr_code = fields.Binary(compute='_generate_qr_code')
    phone = fields.Char(required=True, tracking=True)
    pricing_id = fields.Many2one('operation.pricing', domain="[('state','=','confirm')]",required=True, tracking=True)
    hall_id = fields.Many2one('operation.hall', required=True, tracking=True)
    category_id = fields.Many2one('fleet.vehicle.model.category', required=True, tracking=True)
    vehicle_id = fields.Many2one('fleet.vehicle', required=True, domain="[('category_id','=',category_id)]",tracking=True)
    driver_id = fields.Many2one(related='vehicle_id.driver_id', tracking=True)
    journal_id = fields.Many2one('account.journal', required=True, domain="[('type','=','sale')]",tracking=True)
    date = fields.Date(default=fields.Date.today(), tracking=True)
    from_city = fields.Many2one('operation.city', string='From')
    to_city = fields.Many2one('operation.city', string='To')
    amount = fields.Integer()
    invoice_id = fields.Many2one('account.move')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], default='draft', tracking=True)

    @api.depends('customer_name')
    def _generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data("Hi ezz 😍")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        image_stream = io.BytesIO()
        img.save(image_stream, format='PNG')
        image_stream.seek(0)
        # Convert image to base64 so that Odoo can store it
        image_base64 = base64.b64encode(image_stream.read())
        self.qr_code = image_base64

    def unlink(self):
        self.invoice_id.unlink()
        return super(Counter, self).unlink()

    @api.constrains('from_city', 'to_city')
    def _check_cities(self):
        if self.from_city == self.to_city:
            raise ValidationError("From and To cities must be different!")
        if not self.from_city or not self.to_city:
            raise ValidationError("plz, enter from, to values!")
        elif self.from_city != '' and self.to_city != '':
            trip = self.pricing_id.trip_ids.filtered(
                lambda
                t: t.vehicle_id == self.vehicle_id
                and
                t.from_city == self.from_city
                and
                t.to_city == self.to_city
                )
            if len(trip) == 1:
                self.amount = trip.price

    def set_confirm(self):
        if self.amount <= 0:
            raise ValidationError("Amount must be positive!")
        self.create_invoice()
        self.state = 'confirm'

    def create_invoice(self):
        invoice_obj = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'counter_id': self.id,
            'journal_id': self.journal_id.id,
            'invoice_date': self.date,
            'partner_id': self.customer_name.id,
            'invoice_line_ids': [(0, 0, {
                    'product_id': self.vehicle_id.product_id.id,
                    'quantity': 1,
                    'price_unit': self.amount,
                    'price_subtotal': self.amount,
            })],
        })
        self.invoice_id = invoice_obj.id

    def show_invoicing(self):
        return {
            'name': 'Invoices',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
        }

    def show_dashboard(self):
        tree_id = self.env.ref('operation.dashboard_tree').id
        form_id = self.env.ref('operation.dashboard_form').id
        kanban_id = self.env.ref('operation.dashboard_kanban').id
        return {
            'name': 'Dashboard',
            'type': 'ir.actions.act_window',
            'res_model': 'fleet.vehicle',
            'view_mode': 'tree,form',
            'views': [(kanban_id, 'kanban'),(tree_id, 'tree'), (form_id, 'form')],
        }




