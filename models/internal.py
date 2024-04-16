from odoo import models, fields, api, _


class Internal(models.Model):
    _name = 'internal'
    _inherit = ['type']
    _description = 'Internal'

    internal = fields.Selection([
        ("screens", "Screens"),
        ("housing", "Housing"),
        ("back", "Back"),
        ("frame", "Frame"),
        ("batteries", "Batteries"),
        ("flats", "Flats"),
        ("shipping", "Shipping"),
        ("insulated", "Insulated"),
        ("flatah_power", "Flatah Power and Volume"),
        ("suktat", "Suktat"),
        ("bell", "Bell"),
        ("cameras", "Cameras"),
        ("additions", "additions")], string='Internal', required=True
    )

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('internal')
        return super(Internal, self).create(vals)

