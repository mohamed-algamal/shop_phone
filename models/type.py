from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Type(models.Model):
    _name = 'type'
    _description = 'Type'

    name = fields.Char(string="Name", required=True)
    ref = fields.Char(string='Reference', readonly=True)
    count = fields.Integer(stirng='count')
    price = fields.Float(string='Price', required=True)
    check_count = fields.Boolean(string='Check Count', compute='_compute_check_count', store=True)

    @api.constrains('price')
    def check_price(self):
        for rec in self:
            if rec.price == 0:
                raise ValidationError(_("You should enter the value in price field above zero."))

    @api.depends('count')
    def _compute_check_count(self):
        for rec in self:
            if rec.count <= 5:
                rec.check_count = True
            else:
                rec.check_count = False

