from odoo import models, api


class SalesPdfReport(models.AbstractModel):
    # _name = 'report.module_name.template_id'
    _name = 'report.shop_phone.report_sales_card_id'
    _description = 'Sales Pdf Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("Test......", docids)  # return the id of selected record
        # docs = self.env['hospital.patient'].browse(docids)
        # docs = self.env['hospital.patient'].search([('id', 'in', docids)])
        return {
            'docs': docids,
        }

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     # print("Test.......", docids)
    #     # print("Test.......", data) the data come form button print
    #     gender = data.get('form').get('gender')
    #     domain = []
    #     if gender:
    #         domain += ('gender', '=', gender)
    #     docs = self.env['hospital.patient'].search([domain])
    #     return {  # you can pass any value you went
    #         'docs': docs,
    #         'email': 'algamalmohamed@gmail.com',
    #     }
