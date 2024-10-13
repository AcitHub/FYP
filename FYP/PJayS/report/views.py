from django.shortcuts import render
from django.http import HttpResponse
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER  
import xlsxwriter  # For Excel report generation
from datetime import datetime
from .models import Report  # Import your REPORT model
from student.models import Member  # Import Member model
from teacher.models import Teacher  # Import Teacher model

def generate_report(request):
    if request.method == 'POST':
        report_type = request.POST.get('report-type')
        start_date = request.POST.get('gen-startDate')
        end_date = request.POST.get('gen-endDate')
        community = request.POST.get('gen-list')

        # Validate date fields
        if not start_date or not end_date:
            return render(request, 'generate/muka surat-Hasilkan Laporan.html', {'error': 'Please provide both start and end dates.'})

        # Convert date strings to Python date objects
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return render(request, 'generate/muka surat-Hasilkan Laporan.html', {'error': 'Invalid date format. Please use YYYY-MM-DD.'})

        # Generate report based on selected community
        if community == "Pelajar":
            member_report_data = Member.objects.filter(tarikh_daftar__range=[start_date, end_date])
            if not member_report_data:
                return render(request, 'generate/muka surat-Hasilkan Laporan.html', {'error': 'No student data found for the selected date range.'})
            return generate_student_report(report_type, member_report_data, start_date, end_date)

        elif community == "Kakitangan":
            teacher_report_data = Teacher.objects.filter(tarikh_daftar__range=[start_date, end_date])
            if not teacher_report_data:
                return render(request, 'generate/muka surat-Hasilkan Laporan.html', {'error': 'No teacher data found for the selected date range.'})
            return generate_teacher_report(report_type, teacher_report_data, start_date, end_date)

        elif community == "Keseluruhan":
            member_report_data = Member.objects.filter(tarikh_daftar__range=[start_date, end_date])
            teacher_report_data = Teacher.objects.filter(tarikh_daftar__range=[start_date, end_date])
            if not member_report_data and not teacher_report_data:
                return render(request, 'generate/muka surat-Hasilkan Laporan.html', {'error': 'No data found for the selected date range.'})
            return generate_combined_report(report_type, member_report_data, teacher_report_data, start_date, end_date)

    # If the request is not POST, render the report generation page
    return render(request, 'generate/muka surat-Hasilkan Laporan.html')


def generate_student_report(report_type, member_data, start_date, end_date):
    if report_type == 'pdf-type':
        return generate_student_pdf_report(member_data, start_date, end_date)
    elif report_type == 'xlsx-type':
        return generate_student_excel_report(member_data, start_date, end_date)

def generate_teacher_report(report_type, teacher_data, start_date, end_date):
    if report_type == 'pdf-type':
        return generate_teacher_pdf_report(teacher_data, start_date, end_date)
    elif report_type == 'xlsx-type':
        return generate_teacher_excel_report(teacher_data, start_date, end_date)

def generate_combined_report(report_type, member_data, teacher_data, start_date, end_date):
    if report_type == 'pdf-type':
        return generate_combined_pdf_report(member_data, teacher_data, start_date, end_date)
    elif report_type == 'xlsx-type':
        return generate_combined_excel_report(member_data, teacher_data, start_date, end_date)

# Individual PDF generation functions for each community
def generate_student_pdf_report(member_data, start_date, end_date):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'
    buffer = io.BytesIO()

    # Define page size and margins
    PAGE_WIDTH, PAGE_HEIGHT = A4
    left_margin = 30
    right_margin = 30
    top_margin = 30
    bottom_margin = 30

    available_width = PAGE_WIDTH - left_margin - right_margin

    p = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin
    )

    content = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="CustomTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        spaceAfter=12
    )

    title = Paragraph("Student Report", title_style)
    date_range = Paragraph(f"From: {start_date.strftime('%d-%m-%Y')} To: {end_date.strftime('%d-%m-%Y')}", styles['Normal'])
    content.append(title)
    content.append(date_range)
    content.append(Spacer(1, 12))

    headers = ["Nama", "IC", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
    col_proportions = [1.5, 1.5, 1, 1.5, 1.5]
    total_proportion = sum(col_proportions)
    col_widths = [(prop / total_proportion) * available_width for prop in col_proportions]

    table_data = [headers]
    cell_style = ParagraphStyle('cell_style', fontSize=8, alignment=1)

    for record in member_data:
        table_data.append([   
            Paragraph(record.nama, cell_style),
            Paragraph(record.ic_pelajar, cell_style),
            Paragraph(record.ahli, cell_style),
            Paragraph(f"RM {record.modal_syer:.2f}", cell_style),
            Paragraph(record.tarikh_daftar.strftime('%d-%m-%Y'), cell_style)
        ])

    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    content.append(table)
    p.build(content)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def generate_teacher_pdf_report(teacher_data, start_date, end_date):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="teacher_report.pdf"'
    buffer = io.BytesIO()

    PAGE_WIDTH, PAGE_HEIGHT = A4
    left_margin = 30
    right_margin = 30
    top_margin = 30
    bottom_margin = 30

    available_width = PAGE_WIDTH - left_margin - right_margin

    p = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin
    )

    content = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="CustomTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        spaceAfter=12
    )

    title = Paragraph("Teacher Report", title_style)
    date_range = Paragraph(f"From: {start_date.strftime('%d-%m-%Y')} To: {end_date.strftime('%d-%m-%Y')}", styles['Normal'])
    content.append(title)
    content.append(date_range)
    content.append(Spacer(1, 12))

    headers = ["Nama", "IC", "Pangkat", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
    col_proportions = [1.5, 1, 1, 0.5, 1, 1]  # You can adjust these values
    total_proportion = sum(col_proportions)
    col_widths = [(prop / total_proportion) * available_width for prop in col_proportions]

    table_data = [headers]
    cell_style = ParagraphStyle('cell_style', fontSize=8, alignment=1)

    for record in teacher_data:
        table_data.append([
            Paragraph(record.nama, cell_style),
            Paragraph(record.ic_cikgu, cell_style),
            Paragraph(record.pangkat, cell_style),
            Paragraph(record.ahli, cell_style),
            Paragraph(f"RM {record.modal_syer:.2f}", cell_style),
            Paragraph(record.tarikh_daftar.strftime('%d-%m-%Y'), cell_style)
        ])

    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    content.append(table)
    p.build(content)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def generate_combined_pdf_report(member_data, teacher_data, start_date, end_date):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="combined_report.pdf"'
    buffer = io.BytesIO()

    PAGE_WIDTH, PAGE_HEIGHT = A4
    left_margin = 30
    right_margin = 30
    top_margin = 30
    bottom_margin = 30

    available_width = PAGE_WIDTH - left_margin - right_margin

    p = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin
    )

    content = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="CustomTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        spaceAfter=12
    )

    # Title
    title = Paragraph("Combined Report", title_style)
    date_range = Paragraph(f"From: {start_date.strftime('%d-%m-%Y')} To: {end_date.strftime('%d-%m-%Y')}", styles['Normal'])
    content.append(title)
    content.append(date_range)
    content.append(Spacer(1, 12))  # Space after title

    # Table for Students
    if member_data:
        student_header = Paragraph("Student Data", title_style)  # Section header
        content.append(student_header)
        content.append(Spacer(1, 6))  # Space before student table
        
        headers = ["Nama", "IC", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
        col_proportions = [1.5, 1.5, 1, 1.5, 1.5]
        total_proportion = sum(col_proportions)
        col_widths = [(prop / total_proportion) * available_width for prop in col_proportions]

        table_data = [headers]
        cell_style = ParagraphStyle('cell_style', fontSize=8, alignment=1)

        for record in member_data:
            table_data.append([
                Paragraph(record.nama, cell_style),
                Paragraph(record.ic_pelajar, cell_style),
                Paragraph(record.ahli, cell_style),
                Paragraph(f"RM {record.modal_syer:.2f}", cell_style),
                Paragraph(record.tarikh_daftar.strftime('%d-%m-%Y'), cell_style)
            ])

        student_table = Table(table_data, colWidths=col_widths)
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        content.append(student_table)
        content.append(Spacer(1, 12))  # Space after student table

    # Add a new page for the teacher report
    content.append(PageBreak())  # Create a new page for the teacher report

    # Table for Teachers
    if teacher_data:
        teacher_header = Paragraph("Teacher Data", title_style)  # Section header
        content.append(teacher_header)
        content.append(Spacer(1, 6))  # Space before teacher table

        headers = ["Nama", "IC", "Pangkat", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
        col_proportions = [1.5, 1, 1, 0.5, 1, 1]
        total_proportion = sum(col_proportions)
        col_widths = [(prop / total_proportion) * available_width for prop in col_proportions]

        table_data = [headers]
        cell_style = ParagraphStyle('cell_style', fontSize=8, alignment=1)

        for record in teacher_data:
            table_data.append([
                Paragraph(record.nama, cell_style),
                Paragraph(record.ic_cikgu, cell_style),
                Paragraph(record.pangkat, cell_style),
                Paragraph(record.ahli, cell_style),
                Paragraph(f"RM {record.modal_syer:.2f}", cell_style),
                Paragraph(record.tarikh_daftar.strftime('%d-%m-%Y'), cell_style)
            ])

        teacher_table = Table(table_data, colWidths=col_widths)
        teacher_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        content.append(teacher_table)

    p.build(content)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


# Separate Excel report generation functions
def generate_student_excel_report(member_data, start_date, end_date):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="student_report.xlsx"'

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Define formats for headers and data
    header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#D7E4BC',
        'border': 1
    })
    
    data_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })

    # Adjust column widths
    worksheet.set_column('A:A', 20)  # Nama
    worksheet.set_column('B:B', 20)  # IC
    worksheet.set_column('C:C', 20)  # Ahli
    worksheet.set_column('D:D', 20)  # Modal Syer
    worksheet.set_column('E:E', 20)  # Tarikh Pendaftaran

    # Write header information
    worksheet.merge_range('A1:E1', f'Student Report', workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14}))
    worksheet.write('A2', f'From: {start_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    worksheet.write('A3', f'To: {end_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    
    # Add column headers
    headers = ["Nama", "IC", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
    for col_num, header in enumerate(headers):
        worksheet.write(4, col_num, header, header_format)

    # Write data to the worksheet
    row = 5  # Start writing data from this row
    
    # Write member data if available
    for record in member_data:
        worksheet.write(row, 0, record.nama, data_format)  # Nama
        worksheet.write(row, 1, record.ic_pelajar, data_format)  # IC
        worksheet.write(row, 2, record.ahli, data_format)  # Ahli
        worksheet.write(row, 3, f'RM {record.modal_syer:.2f}', data_format)  # Modal Syer
        worksheet.write(row, 4, record.tarikh_daftar.strftime('%d-%m-%Y'), data_format)  # Tarikh Pendaftaran
        row += 1

    # Close the workbook and write it to the output stream
    workbook.close()

    output.seek(0)
    response.write(output.read())
    
    return response


def generate_teacher_excel_report(teacher_data, start_date, end_date):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="teacher_report.xlsx"'

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Define formats for headers and data
    header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#D7E4BC',
        'border': 1
    })
    
    data_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })

    # Adjust column widths
    worksheet.set_column('A:A', 20)  # Nama
    worksheet.set_column('B:B', 20)  # IC
    worksheet.set_column('C:C', 20)  # Pangkat
    worksheet.set_column('D:D', 20)  # Ahli
    worksheet.set_column('E:E', 20)  # Modal Syer
    worksheet.set_column('F:F', 20)  # Tarikh Pendaftaran

    # Write header information
    worksheet.merge_range('A1:F1', f'Teacher Report', workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14}))
    worksheet.write('A2', f'From: {start_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    worksheet.write('A3', f'To: {end_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    
    # Add column headers
    headers = ["Nama", "IC", "Pangkat", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
    for col_num, header in enumerate(headers):
        worksheet.write(4, col_num, header, header_format)

    # Write data to the worksheet
    row = 5  # Start writing data from this row
    
    # Write teacher data if available
    for record in teacher_data:
        worksheet.write(row, 0, record.nama, data_format)  # Nama
        worksheet.write(row, 1, record.ic_cikgu, data_format)  # IC
        worksheet.write(row, 2, record.pangkat, data_format)  # Pangkat
        worksheet.write(row, 3, record.ahli, data_format)  # Ahli
        worksheet.write(row, 4, f'RM {record.modal_syer:.2f}', data_format)  # Modal Syer
        worksheet.write(row, 5, record.tarikh_daftar.strftime('%d-%m-%Y'), data_format)  # Tarikh Pendaftaran
        row += 1

    # Close the workbook and write it to the output stream
    workbook.close()

    output.seek(0)
    response.write(output.read())
    
    return response


def generate_combined_excel_report(member_data, teacher_data, start_date, end_date):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="combined_report.xlsx"'

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Define formats for headers and data
    header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#D7E4BC',  # Light green background for headers
        'border': 1  # Border for all cells
    })
    
    data_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })

    # Adjust column widths
    worksheet.set_column('A:A', 20)   # Nama
    worksheet.set_column('B:B', 20)   # IC
    worksheet.set_column('C:C', 20)   # Pangkat
    worksheet.set_column('D:D', 20)   # Ahli
    worksheet.set_column('E:E', 20)   # Modal Syer
    worksheet.set_column('F:F', 20)   # Tarikh Pendaftaran

    # Write header information
    worksheet.merge_range('A1:F1', f'Combined Report', workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14}))
    worksheet.write('A2', f'From: {start_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    worksheet.write('A3', f'To: {end_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))

    # Initialize row count
    row = 5  

    # Add student data if available
    if member_data:
        worksheet.write(row, 0, 'Student Data', header_format)
        row += 1
        headers = ["Nama", "IC", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
        for col_num, header in enumerate(headers):
            worksheet.write(row, col_num, header, header_format)
        row += 1

        for record in member_data:
            worksheet.write(row, 0, record.nama, data_format)  # Nama
            worksheet.write(row, 1, record.ic_pelajar, data_format)  # IC
            worksheet.write(row, 2, record.ahli, data_format)  # Ahli
            worksheet.write(row, 3, f'RM {record.modal_syer:.2f}', data_format)  # Modal Syer
            worksheet.write(row, 4, record.tarikh_daftar.strftime('%d-%m-%Y'), data_format)  # Tarikh Pendaftaran
            row += 1
        row += 2  # Add extra space after students

    # Add teacher data if available
    if teacher_data:
        worksheet.write(row, 0, 'Teacher Data', header_format)
        row += 1
        headers = ["Nama", "IC", "Pangkat", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
        for col_num, header in enumerate(headers):
            worksheet.write(row, col_num, header, header_format)
        row += 1

        for record in teacher_data:
            worksheet.write(row, 0, record.nama, data_format)  # Nama
            worksheet.write(row, 1, record.ic_cikgu, data_format)  # IC
            worksheet.write(row, 2, record.pangkat, data_format)  # Pangkat
            worksheet.write(row, 3, record.ahli, data_format)  # Ahli
            worksheet.write(row, 4, f'RM {record.modal_syer:.2f}', data_format)  # Modal Syer
            worksheet.write(row, 5, record.tarikh_daftar.strftime('%d-%m-%Y'), data_format)  # Tarikh Pendaftaran
            row += 1

    # Close the workbook and write it to the output stream
    workbook.close()

    output.seek(0)
    response.write(output.read())
    
    return response