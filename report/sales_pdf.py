from odoo import models, api



class AllPatientReport(models.AbstractModel):
    # _name = 'report.module_name.template_id'
    _name = 'report.om_hospital.report_patient_details'
    _description = 'Patient Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # print("Test.......", docids)
        # print("Test.......", data) the data come form button print
        gender = data.get('form').get('gender')
        domain = []
        if gender:
            domain += ('gender', '=', gender)
        docs = self.env['hospital.patient'].search([domain])
        return {  # you can pass any value you went
            'docs': docs,
            'email': 'algamalmohamed@gmail.com',
        }


class PatientCard(models.AbstractModel):
    # _name = 'report.module_name.template_id'
    _name = 'report.om_hospital.report_patient_id_card'
    _description = 'Patient Card'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("Test......", docids)  # return the id of selected record
        docs = self.env['hospital.patient'].browse(docids)
        # docs = self.env['hospital.patient'].search([('id', 'in', docids)])
        return {
            'docs': docs,
        }