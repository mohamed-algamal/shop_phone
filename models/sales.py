from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Sales(models.Model):
    _name = 'sales'
    _description = 'Sales'

    ref = fields.Char(string='Reference', readonly=True)
    total = fields.Float(string='Total', compute='_compute_total', readonly=True, store=True)

    sales_accessories_ids = fields.One2many('sales.accessories', 'sales_id', string='Sales Accessories')
    sales_electricity_ids = fields.One2many('sales.electricity', 'sales_id', string='Sales Electricity')
    sales_internal_ids = fields.One2many('sales.internal', 'sales_id', string='Sales Internal')
    sales_mobiles_ids = fields.One2many('sales.mobiles', 'sales_id', string='Sales Mobiles')
    sales_petrine_work_ids = fields.One2many('sales.petrine.work', 'sales_id', string='Sales Petrine Work')

    @api.depends('sales_accessories_ids', 'sales_electricity_ids', 'sales_internal_ids', 'sales_mobiles_ids',
                 'sales_petrine_work_ids')
    def _compute_total(self):
        total = 0.0
        for rec in self:
            for record in rec.sales_accessories_ids:
                total += record.sup_total
            for record in rec.sales_internal_ids:
                total += record.sup_total
            for record in rec.sales_mobiles_ids:
                total += record.sup_total
            for record in rec.sales_electricity_ids:
                total += record.sup_total
            for record in rec.sales_petrine_work_ids:
                total += record.sup_total
        self.total = total

    def check_duplicates(self, list_id):
        if len(list_id) != len(set(list_id)):
            raise ValidationError(_("you choose the field two time."))

    @api.model
    def write(self, vals):
        if 'sales_accessories_ids' in vals:
            for rec in vals['sales_accessories_ids']:
                if self.env['sales.accessories'].search([('accessories_id', '=', rec[2].get('accessories_id'))]):
                    raise ValidationError(_("you choose the field two time."))

        if 'sales_electricity_ids' in vals:
            for rec in vals['sales_electricity_ids']:
                if self.env['sales.electricity'].search([('electricity_id', '=', rec[2].get('electricity_id'))]):
                    raise ValidationError(_("you choose the field two time."))

        if 'sales_internal_ids' in vals:
            for rec in vals['sales_internal_ids']:
                if self.env['sales.internal'].search([('internal_id', '=', rec[2].get('internal_id'))]):
                    raise ValidationError(_("you choose the field two time."))

        if 'sales_mobiles_ids' in vals:
            for rec in vals['sales_mobiles_ids']:
                if self.env['sales.mobiles'].search([('mobiles_id', '=', rec[2].get('mobiles_id'))]):
                    raise ValidationError(_("you choose the field two time."))

        if 'sales_petrine_work_ids' in vals:
            for rec in vals['sales_petrine_work_ids']:
                if self.env['sales.petrine.work'].search([('petrine_work_id', '=', rec[2].get('petrine_work_id'))]):
                    raise ValidationError(_("you choose the field two time."))

        return super(Sales, self).write(vals)

    @api.model
    def create(self, vals):
        if vals['sales_accessories_ids']:
            list_id = []
            for rec in vals['sales_accessories_ids']:
                list_id.append(rec[2].get('accessories_id'))
            self.check_duplicates(list_id)

        if vals['sales_electricity_ids']:
            list_id = []
            for rec in vals['sales_electricity_ids']:
                list_id.append(rec[2].get('electricity_id'))
            self.check_duplicates(list_id)

        if vals['sales_internal_ids']:
            list_id = []
            for rec in vals['sales_internal_ids']:
                list_id.append(rec[2].get('internal_id'))
            self.check_duplicates(list_id)

        if vals['sales_mobiles_ids']:
            list_id = []
            for rec in vals['sales_mobiles_ids']:
                list_id.append(rec[2].get('mobiles_id'))
            self.check_duplicates(list_id)

        if vals['sales_petrine_work_ids']:
            list_id = []
            for rec in vals['sales_petrine_work_ids']:
                list_id.append(rec[2].get('petrine_work_id'))
            self.check_duplicates(list_id)

        vals['ref'] = self.env['ir.sequence'].next_by_code('sales')
        return super(Sales, self).create(vals)

    def action_test(self):
        for rec in self:
            print(self.sales_accessories_ids.accessories_id)


class SalesAccessories(models.Model):
    _name = 'sales.accessories'
    _description = 'Sales Accessories'

    sales_id = fields.Many2one('sales', string='sales')
    accessories_id = fields.Many2one('accessories', string='Accessories', required=True)
    count = fields.Integer(string='Count', default=1)
    count_found = fields.Integer(string='Count Found', compute='_compute_count_found', readonly=True, store=True)
    price = fields.Float(string='Price', compute='_compute_price', readonly=True, store=True)
    sup_total = fields.Float(string='Sup Total', compute='_compute_sup_total', store=True)

    @api.depends('count', 'price')
    def _compute_sup_total(self):
        for rec in self:
            rec.sup_total = (rec.price * rec.count)

    @api.depends('accessories_id')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.accessories_id.price

    @api.depends('accessories_id')
    def _compute_count_found(self):
        for rec in self:
            rec.count_found = rec.accessories_id.count

    @api.model
    def create(self, vals):
        return super(SalesAccessories, self).create(vals)


class SalesElectricity(models.Model):
    _name = 'sales.electricity'
    _description = 'Sales Electricity'

    sales_id = fields.Many2one('sales', string='sales')
    electricity_id = fields.Many2one('electricity', string='Electricity', required=True)
    count = fields.Integer(string='Count', default=1)
    count_found = fields.Integer(string='Count Found', compute='_compute_count_found', readonly=True, store=True)
    price = fields.Float(string='Price', compute='_compute_price', readonly=True, store=True)
    sup_total = fields.Float(string='Sup Total', compute='_compute_sup_total', readonly=True, store=True)

    @api.depends('count', 'price')
    def _compute_sup_total(self):
        for rec in self:
            rec.sup_total = (rec.price * rec.count)

    @api.depends('electricity_id')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.electricity_id.price

    @api.depends('electricity_id')
    def _compute_count_found(self):
        for rec in self:
            rec.count_found = rec.electricity_id.count


class SalesInternal(models.Model):
    _name = 'sales.internal'
    _description = 'Sales Internal'

    sales_id = fields.Many2one('sales', string='sales')
    internal_id = fields.Many2one('internal', string='Internal', required=True)
    count = fields.Integer(string='Count', default=1)
    count_found = fields.Integer(string='Count Found', compute='_compute_count_found', readonly=True, store=True)
    price = fields.Float(string='Price', compute='_compute_price', readonly=True, store=True)
    sup_total = fields.Float(string='Sup Total', compute='_compute_sup_total', store=True)

    @api.depends('count', 'price')
    def _compute_sup_total(self):
        for rec in self:
            rec.sup_total = (rec.price * rec.count)

    @api.depends('internal_id')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.internal_id.price

    @api.depends('internal_id')
    def _compute_count_found(self):
        for rec in self:
            rec.count_found = rec.internal_id.count


class SalesMobiles(models.Model):
    _name = 'sales.mobiles'
    _description = 'Sales Mobiles'

    sales_id = fields.Many2one('sales', string='sales')
    mobiles_id = fields.Many2one('mobiles', string='Mobiles', required=True)
    count = fields.Integer(string='Count', default=1)
    count_found = fields.Integer(string='Count Found', compute='_compute_count_found', readonly=True, store=True)
    price = fields.Float(string='Price', compute='_compute_price', readonly=True, store=True)
    sup_total = fields.Float(string='Sup Total', compute='_compute_sup_total', store=True)

    @api.depends('count', 'price')
    def _compute_sup_total(self):
        for rec in self:
            rec.sup_total = (rec.price * rec.count)

    @api.depends('mobiles_id')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.mobiles_id.price

    @api.depends('mobiles_id')
    def _compute_count_found(self):
        for rec in self:
            rec.count_found = rec.mobiles_id.count


class SalesPetrineWork(models.Model):
    _name = 'sales.petrine.work'
    _description = 'Sales Petrine Work'

    sales_id = fields.Many2one('sales', string='sales')
    petrine_work_id = fields.Many2one('petrine.work', string='Petrine Work', required=True)
    count = fields.Integer(string='Count', default=1)
    count_found = fields.Integer(string='Count Found', compute='_compute_count_found', readonly=True, store=True)
    price = fields.Float(string='Price', compute='_compute_price', readonly=True, store=True)
    sup_total = fields.Float(string='Sup Total', compute='_compute_sup_total', store=True)

    @api.depends('count', 'price')
    def _compute_sup_total(self):
        for rec in self:
            rec.sup_total = (rec.price * rec.count)

    @api.depends('petrine_work_id')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.petrine_work_id.price

    @api.depends('petrine_work_id')
    def _compute_count_found(self):
        for rec in self:
            rec.count_found = rec.petrine_work_id.count
