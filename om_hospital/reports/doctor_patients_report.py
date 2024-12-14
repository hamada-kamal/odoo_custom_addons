from odoo import fields, api, models


class DoctorPatientsReport(models.AbstractModel):
    _name = 'report.om_hospital.report_id_doctor_patients'
    _description = 'Doctor Patients Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        doctor = self.env['hospital.doctor'].browse(docids[0])
        patients = self.env['hospital.patient'].search([('doctor_id','=',doctor.id)])
        return {
            'doctor': doctor,
            'patients': patients,
        }