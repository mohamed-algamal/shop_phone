from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Sales(models.Model):
    _name = 'sales'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sales'
    _order = 'id desc'
    _rec_name = 'ref'

    ref = fields.Char(string='Reference', readonly=True)
    total = fields.Float(string='Total', compute='_compute_total', readonly=True, store=True)
    is_done = fields.Boolean(string='Is Done', readonly=True)

    sales_accessories_ids = fields.One2many('sales.accessories', 'sales_id', string='Sales Accessories')
    sales_electricity_ids = fields.One2many('sales.electricity', 'sales_id', string='Sales Electricity')
    sales_internal_ids = fields.One2many('sales.internal', 'sales_id', string='Sales Internal')
    sales_mobiles_ids = fields.One2many('sales.mobiles', 'sales_id', string='Sales Mobiles')
    sales_petrine_work_ids = fields.One2many('sales.petrine.work', 'sales_id', string='Sales Petrine Work')
    state = fields.Selection([
        ('prepare', 'Prepare'),
        ('done', 'Done')], string='State', default='prepare'
    )

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        print(default)
        if default is None:
            default = {}
        return super(Sales, self).copy(default)

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

    @api.model
    def write(self, vals):
        if 'sales_accessories_ids' in vals:
            for rec in vals['sales_accessories_ids']:
                if len(rec) == 3:
                    for record in self.sales_accessories_ids:
                        if record.accessories_id.id == rec[2].get('accessories_id'):
                            raise ValidationError(_("You choose the field two time."))

        if 'sales_electricity_ids' in vals:
            for rec in vals['sales_electricity_ids']:
                if len(rec) == 3:
                    for record in self.sales_electricity_ids:
                        if record.electricity_id.id == rec[2].get('electricity_id'):
                            raise ValidationError(_("You choose the field two time."))

        if 'sales_internal_ids' in vals:
            for rec in vals['sales_internal_ids']:
                if len(rec) == 3:
                    for record in self.sales_internal_ids:
                        if record.internal_id.id == rec[2].get('internal_id'):
                            raise ValidationError(_("You choose the field two time."))

        if 'sales_mobiles_ids' in vals:
            for rec in vals['sales_mobiles_ids']:
                if len(rec) == 3:
                    for record in self.sales_mobiles_ids:
                        if record.mobiles_id.id == rec[2].get('mobiles_id'):
                            raise ValidationError(_("You choose the field two time."))

        if 'sales_petrine_work_ids' in vals:
            for rec in vals['sales_petrine_work_ids']:
                if len(rec) == 3:
                    for record in self.sales_petrine_work_ids:
                        if record.petrine_work_id.id == rec[2].get('petrine_work_id'):
                            raise ValidationError(_("You choose the field two time."))

        return super(Sales, self).write(vals)

    def check_duplicates(self, list_id):
        if len(list_id) != len(set(list_id)):
            raise ValidationError(_("You choose the field two time."))

    @api.model
    def create(self, vals):
        if 'sales_accessories_ids' in vals:
            if vals['sales_accessories_ids']:
                list_id = []
                for rec in vals['sales_accessories_ids']:
                    list_id.append(rec[2].get('accessories_id'))
                self.check_duplicates(list_id)

        if 'sales_electricity_ids' in vals:
            if vals['sales_electricity_ids']:
                list_id = []
                for rec in vals['sales_electricity_ids']:
                    list_id.append(rec[2].get('electricity_id'))
                self.check_duplicates(list_id)

        if 'sales_internal_ids' in vals:
            if vals['sales_internal_ids']:
                list_id = []
                for rec in vals['sales_internal_ids']:
                    list_id.append(rec[2].get('internal_id'))
                self.check_duplicates(list_id)

        if 'sales_mobiles_ids' in vals:
            if vals['sales_mobiles_ids']:
                list_id = []
                for rec in vals['sales_mobiles_ids']:
                    list_id.append(rec[2].get('mobiles_id'))
                self.check_duplicates(list_id)

        if 'sales_petrine_work_ids' in vals:
            if vals['sales_petrine_work_ids']:
                list_id = []
                for rec in vals['sales_petrine_work_ids']:
                    list_id.append(rec[2].get('petrine_work_id'))
                self.check_duplicates(list_id)

        vals['ref'] = self.env['ir.sequence'].next_by_code('sales')
        return super(Sales, self).create(vals)

    def unlink(self):
        for rec in self:
            if rec.state == "done":
                raise ValidationError(_("You can't delete done records."))
        return super(Sales, self).unlink()

    def _check_count(self, rec):
        if rec.count > rec.count_found:
            raise ValidationError(_("The number of product don't found."))
        if not rec.count:
            raise ValidationError(_("You should inter the number above zero in count field."))

    def action_done(self):
        for rec in self:
            if rec.total == 0:
                raise ValidationError(_("Total field shouldn't be equal zero."))

        for rec in self.sales_accessories_ids:
            self._check_count(rec)

        for rec in self.sales_electricity_ids:
            self._check_count(rec)

        for rec in self.sales_mobiles_ids:
            self._check_count(rec)

        for rec in self.sales_internal_ids:
            self._check_count(rec)

        for rec in self.sales_petrine_work_ids:
            self._check_count(rec)

        for rec in self.sales_accessories_ids:
            rec.accessories_id.count -= rec.count

        for rec in self.sales_electricity_ids:
            rec.electricity_id.count -= rec.count

        for rec in self.sales_mobiles_ids:
            rec.mobiles_id.count -= rec.count

        for rec in self.sales_internal_ids:
            rec.internal_id.count -= rec.count

        for rec in self.sales_petrine_work_ids:
            rec.petrine_work_id.count -= rec.count

        for rec in self:
            rec.state = "done"
            rec.is_done = True

        self.message_post(body=f'The sale is done with total {self.total}.', message_type='comment',
                          subtype_xmlid='mail.mt_note',)

    def action_print(self): 
        record = []
        if self.sales_accessories_ids:
            for rec in self.sales_accessories_ids:
                x = {
                    'name': rec.accessories_id.name,
                    'category': rec.accessories_id.accessories,
                    'price': rec.price,
                    'count': rec.count,
                    'subtotal': rec.sup_total,
                }
                record.append(x)
        if self.sales_internal_ids:
            for rec in self.sales_internal_ids:
                x = {
                    'name': rec.internal_id.name,
                    'category': rec.internal_id.internal,
                    'price': rec.price,
                    'count': rec.count,
                    'subtotal': rec.sup_total,
                }
                record.append(x)
        if self.sales_mobiles_ids:
            for rec in self.sales_mobiles_ids:
                x = {
                    'name': rec.mobiles_id.name,
                    'category': rec.mobiles_id.mobiles,
                    'price': rec.price,
                    'count': rec.count,
                    'subtotal': rec.sup_total,
                }
                record.append(x)
        if self.sales_electricity_ids:
            for rec in self.sales_electricity_ids:
                x = {
                    'name': rec.electricity_id.name,
                    'category': rec.electricity_id.electricity,
                    'price': rec.price,
                    'count': rec.count,
                    'subtotal': rec.sup_total,
                }
                record.append(x)
        if self.sales_petrine_work_ids:
            for rec in self.sales_petrine_work_ids:
                x = {
                    'name': rec.petrine_work_id.name,
                    'category': rec.petrine_work_id.petrine_work,
                    'price': rec.price,
                    'count': rec.count,
                    'subtotal': rec.sup_total,
                }
                record.append(x)
        data = {
            'form': self.read()[0],
            'record': record,
        }
        # external id for report action
        return self.env.ref('shop_phone.report_sales_card').report_action(self, data=data)


class SalesAccessories(models.Model):
    _name = 'sales.accessories'
    _description = 'Sales Accessories'

    sales_id = fields.Many2one('sales', string='sales')
    accessories_id = fields.Many2one('accessories', string='Accessories', required=True)
    count = fields.Integer(string='Count', default=1)
    count_found = fields.Integer(string='Count Found', compute='_compute_count_found', readonly=True, store=True)
    price = fields.Float(string='Price', compute='_compute_price', readonly=True, store=True)
    sup_total = fields.Float(string='Sup Total', compute='_compute_sup_total', store=True)
    category = fields.Char(string='Category', compute='_compute_category', readonly=True)

    @api.depends('accessories_id')
    def _compute_category(self):
        for rec in self:
            rec.category = rec.accessories_id.accessories

    @api.depends('count', 'price')
    def _compute_sup_total(self):
        for rec in self:
            rec.sup_total = (rec.price * rec.count)

    @api.depends('accessories_id')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.accessories_id.price

    @api.depends('accessories_id', 'accessories_id.count')
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
    category = fields.Char(string='Category', compute='_compute_category', readonly=True)

    @api.depends('electricity_id')
    def _compute_category(self):
        for rec in self:
            rec.category = rec.electricity_id.electricity

    @api.depends('count', 'price')
    def _compute_sup_total(self):
        for rec in self:
            rec.sup_total = (rec.price * rec.count)

    @api.depends('electricity_id')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.electricity_id.price

    @api.depends('electricity_id', 'electricity_id.count')
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
    category = fields.Char(string='Category', compute='_compute_category', readonly=True)

    @api.depends('internal_id')
    def _compute_category(self):
        for rec in self:
            rec.category = rec.internal_id.internal

    @api.depends('count', 'price')
    def _compute_sup_total(self):
        for rec in self:
            rec.sup_total = (rec.price * rec.count)

    @api.depends('internal_id')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.internal_id.price

    @api.depends('internal_id', 'internal_id.count')
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
    category = fields.Char(string='Category', compute='_compute_category', readonly=True)

    @api.depends('mobiles_id')
    def _compute_category(self):
        for rec in self:
            rec.category = rec.mobiles_id.mobiles

    @api.depends('count', 'price')
    def _compute_sup_total(self):
        for rec in self:
            rec.sup_total = (rec.price * rec.count)

    @api.depends('mobiles_id')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.mobiles_id.price

    @api.depends('mobiles_id', 'mobiles_id.count')
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
    category = fields.Char(string='Category', compute='_compute_category', readonly=True)

    @api.depends('petrine_work_id')
    def _compute_category(self):
        for rec in self:
            rec.category = rec.petrine_work_id.petrine_work

    @api.depends('count', 'price')
    def _compute_sup_total(self):
        for rec in self:
            rec.sup_total = (rec.price * rec.count)

    @api.depends('petrine_work_id')
    def _compute_price(self):
        for rec in self:
            rec.price = rec.petrine_work_id.price

    @api.depends('petrine_work_id', 'petrine_work_id.count')
    def _compute_count_found(self):
        for rec in self:
            rec.count_found = rec.petrine_work_id.count
