from odoo import models, fields, api


class TypeProduct(models.Model):
    _name = 'type.product'
    _description = 'Type Product'

    name = fields.Char(string='Name')
    cartalge = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()


