from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Maintenance(models.Model):
    _name = 'maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Maintenance'

    ref = fields.Char(string='Reference', readonly=True)
    price = fields.Float(string='Price', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('prepare', 'Prepare'),
        ('done', 'Done'),
        ('cancel', 'Cancel')], string='State', default='draft'
    )
    description = fields.Text(string='description')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('maintenance')
        return super(Maintenance, self).create(vals)

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_prepare(self):
        for rec in self:
            rec.state = 'prepare'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
