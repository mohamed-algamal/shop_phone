from odoo import models, fields, api, _


class PetrineWork(models.Model):
    _name = 'petrine.work'
    _inherit = ['type']
    _description = 'Petrine Work'

    petrine_work = fields.Selection([
        ("airpods", "Airpods"),
        ("smart_watch", "Smart Watch"),
        ("Head phones", "Head phones"),
        ("additions", "additions")], string='Petrine Work', required=True
    )

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('petrine_work')
        return super(PetrineWork, self).create(vals)

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} ({rec.petrine_work})"
