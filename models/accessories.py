from odoo import models, fields, api, _


class Accessories(models.Model):
    _name = 'accessories'
    _inherit = ['type']
    _description = 'Accessories'

    accessories = fields.Selection([
        ("grapes", "Grapes"),
        ("screens", "Screens"),
        ("additions", "additions")], string='Accessories', required=True
    )

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('accessories')
        return super(Accessories, self).create(vals)

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} ({rec.accessories})"
