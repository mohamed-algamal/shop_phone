from odoo import models, fields, api, _


class Electricity(models.Model):
    _name = 'electricity'
    _inherit = ['type']
    _description = 'Electricity'

    electricity = fields.Selection([
        ("micro_charger", "Micro charger"),
        ("type_c_charger", "Type c charger"),
        ("charger_head", "Charger head"),
        ("micro_connectors", "Micro connectors"),
        ("type_c_connectors", "Type c connectors"),
        ("hand_free", "Hand free"),
        ("hand_type_c", "Hand type c"),
        ("hand_iPhone", "Hand iPhone"),
        ("mobile_holder", "Mobile holder"),
        ("flashes", "Flashes"),
        ("memory_cards", "Memory cards"),
        ("flash_reader", "Flash Reader"),
        ("additions", "additions")], string='Electricity', required=True
    )

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('electricity')
        return super(Electricity, self).create(vals)

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} ({rec.electricity})"
