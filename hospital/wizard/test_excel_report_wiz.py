import base64
import io
from odoo import fields, models, _
from odoo.exceptions import ValidationError
import xlsxwriter

class AppointmentExcelReportWizard(models.TransientModel):
    _name = "appointment.excel.report.wizard"

    patient_ids = fields.Many2many('hospital.patient')
    # date_from = fields.Date('Date From', required=True)
    # date_to = fields.Date('Date To', required=True)

    excel_sheet = fields.Binary('Download Report')
    excel_sheet_name = fields.Char(string='Name', size=64)

    def get_report_data(self):
        # if self.date_from and self.date_to:
        #     if self.date_from > self.date_to:
        #         raise ValidationError(_('Date from must be before date to!'))
        #     # print("\n\n data: ",data)
        if self.patient_ids:
            patients = self.env['hospital.patient'].browse(self.patient_ids.ids)
            print("\npatients: ",patients)
            # for patient in patients:
            #     data['patients'].append({
            #         'id': patient.id,
            #         'patient_name': patients.full_name,
            #         'doctor_name': appointment.doctor_id.first_name,
            #         'date_appointment': appointment.date_appointment,
            #         'date_checkup': appointment.date_checkup,
            #         'state': appointment.state,
            #     })
            data = {'patients': patients}
            return data
        raise ValidationError(_('Plz, select at least one patient!'))

    def print_appointments_excel_report(self):
        data = self.get_report_data()
        self.ensure_one()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        header_format = workbook.add_format({
            'bold': 1,
            'font_name': 'Arial',
            'border': 2,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
        })

        line_format = workbook.add_format({
            # 'bold': 1,
            'font_name': 'Arial',
            'border': 1,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black',
        })

        worksheet = workbook.add_worksheet('appointments')
        row = 0
        col = 0

        if len(data['patients']) == 1:
            worksheet.set_row(0, 40)
            worksheet.set_row(1, 30)
            worksheet.set_column(0, 0, 20)
            worksheet.set_column(1, 1, 35)
            worksheet.set_column(2, 2, 20)
            worksheet.set_column(3, 3, 20)
            worksheet.set_column(4, 4, 20)
            worksheet.set_column(5, 5, 20)
            worksheet.merge_range(row, row, col, col + 5,f"{data['patients'].full_name}'s appointments", header_format)
            worksheet.write(row+1,col,'Doctor',header_format)
            worksheet.write(row+1,col+1,'Department',header_format)
            worksheet.write(row+1,col+2,'Date',header_format)
            worksheet.write(row+1,col+3,'State',header_format)
            worksheet.write(row+1,col+4,'Checks',header_format)
            worksheet.write(row+1,col+5,'Total Cost',header_format)
            row = 1
            col = 0
            for appointment in data['patients'].appoinment_ids:
                row += 1
                print(appointment.date_appointment)
                worksheet.write(row, col, appointment.doctor_id.first_name, line_format)
                worksheet.write(row, col+1, appointment.department_id.name, line_format)
                worksheet.write(row, col+2, appointment.date_appointment.strftime('%Y-%m-%d'), line_format)
                worksheet.write(row, col+3, appointment.state, line_format)
                worksheet.write(row, col+4, "-".join(appointment.check_ids.mapped('name')), line_format)
                worksheet.write(row, col+5, appointment.cost, line_format)
        else:
            worksheet.set_row(0, 30)
            worksheet.set_column(0, 0, 17)
            worksheet.set_column(1, 1, 17)
            worksheet.set_column(2, 2, 30)
            worksheet.set_column(3, 3, 17)
            worksheet.set_column(4, 4, 17)
            worksheet.set_column(5, 5, 17)
            worksheet.set_column(6, 6, 17)

            worksheet.write(row, col, 'Patient', header_format)
            worksheet.write(row, col + 1, 'Doctor', header_format)
            worksheet.write(row, col + 2, 'Department', header_format)
            worksheet.write(row, col + 3, 'Date', header_format)
            worksheet.write(row, col + 4, 'State', header_format)
            worksheet.write(row, col + 5, 'Checks', header_format)
            worksheet.write(row, col + 6, 'Total Cost', header_format)

            row = 1
            for patient in data['patients']:
                worksheet.merge_range(row, col, row + len(patient.appoinment_ids)-1, col,
                                      f"{patient.full_name}", header_format)
                for appointment in patient.appoinment_ids:
                    worksheet.write(row, col + 1, appointment.doctor_id.first_name, line_format)
                    worksheet.write(row, col + 2, appointment.department_id.name, line_format)
                    worksheet.write(row, col + 3, appointment.date_appointment.strftime('%Y-%m-%d'), line_format)
                    worksheet.write(row, col + 4, appointment.state, line_format)
                    worksheet.write(row, col + 5, "-".join(appointment.check_ids.mapped('name')), line_format)
                    worksheet.write(row, col + 6, appointment.cost, line_format)
                    row += 1
                # add empty row between every patient
                row += 1
                # row += len(patient.appoinment_ids)


        self.excel_sheet_name = 'appointments_excel'
        workbook.close()
        output.seek(0)
        self.excel_sheet = base64.encodebytes(output.read())
        self.excel_sheet_name = str(self.excel_sheet_name) + '.xlsx'
        return {
            'type': 'ir.actions.act_url',
            'name': 'totals Report',
            'url': '/web/content/appointment.excel.report.wizard/%s/excel_sheet/appointments_excel.xlsx?download=true' % (
                self.id),
            'target': 'new'
        }

