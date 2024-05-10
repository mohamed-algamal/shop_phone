from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Maintenance(models.Model):
    _name = 'maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Maintenance'
    _rec_name = 'ref'
    _order = 'id desc'

    ref = fields.Char(string='Reference', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=74)
    price = fields.Float(string='Price')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('prepare', 'Prepare'),
        ('done', 'Done'),
        ('cancel', 'Cancel')], string='State', default='draft'
    )
    description = fields.Text(string='description')
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email")
    client_name = fields.Char(string="Client Name", required=True)

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('maintenance')
        rec = super(Maintenance, self).create(vals)
        self.env['sales'].create({'maintenance_id': rec.id, 'state': 'prepare', 'is_maintenance_record': True})
        return rec

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_prepare(self):
        for rec in self:
            rec.state = 'prepare'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            sales = self.env['sales'].search([('maintenance_id', '=', self.id)])
            if sales:
                sales.action_done()

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
            sales = self.env['sales'].search([('maintenance_id', '=', self.id)])
            if sales:
                sales.action_cancel()

    def action_print(self):
        data = {}
        sales = self.env['sales'].search([('maintenance_id', '=', self.id)])
        if sales:
            data = sales.print_report()
        data.update({'maintenance': self.read()[0]})
        # external id for report action
        return self.env.ref('shop_phone.report_maintenance_card').report_action(self, data=data)

    def action_sales(self):
        sales = self.env['sales'].search([('maintenance_id', '=', self.id)])
        return {
            'view_mode': 'form',
            'res_model': 'sales',
            'res_id': sales.id,
            'target': 'new',  # current and new and inline
            'type': 'ir.actions.act_window',
        }

    # function of email
    def action_send_email(self):
        mail_template = self.env.ref('shop_phone.maintenance_mail_template')  # external id for email template
        for rec in self:
            if rec.email:
                # email_values = {'subject': 'Test OM'} # this for enter date static
                mail_template.send_mail(rec.id, force_send=True)  # force_send=True for send mail immediately
