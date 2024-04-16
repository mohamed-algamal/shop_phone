from odoo import models, fields, api, _


class Mobiles(models.Model):
    _name = 'mobiles'
    _inherit = ['type']
    _description = 'Mobiles'

    mobiles = fields.Selection([
        ('new_mobiles', 'New Mobiles'),
        ('used_mobiles', 'Used Mobiles'),
        ('buttons_mobiles', 'Buttons Mobiles')], string='Mobiles', required=True
    )

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('mobiles')
        return super(Mobiles, self).create(vals)

