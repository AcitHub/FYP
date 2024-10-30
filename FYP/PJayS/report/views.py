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
    reports = []  # Initialize an empty list to hold reports

    if request.method == 'POST':
        # Get form data
        report_type = request.POST.get('report-type')  # Keep this for report generation
        community = request.POST.get('gen-list')
        start_date = request.POST.get('gen-startDate')
        end_date = request.POST.get('gen-endDate')

        # Validate date fields
        if not start_date or not end_date:
            return render(request, 'generate/muka surat-Hasilkan Laporan.html', {
                'error': 'Please provide both start and end dates.',
                'reports': reports
            })

        # Convert date strings to Python date objects
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return render(request, 'generate/muka surat-Hasilkan Laporan.html', {
                'error': 'Invalid date format. Please use YYYY-MM-DD.',
                'reports': reports
            })

        # Query based on the selected community
        if community == 'Pelajar':
            member_report_data = Member.objects.filter(tarikh_daftar__range=[start_date, end_date])
            reports = list(member_report_data) if member_report_data else []
            for report in reports:
                report.is_member = True  # Mark as member

        elif community == 'Kakitangan':
            teacher_report_data = Teacher.objects.filter(tarikh_daftar__range=[start_date, end_date])
            reports = list(teacher_report_data) if teacher_report_data else []
            for report in reports:
                report.is_teacher = True  # Mark as teacher

        elif community == 'Keseluruhan':
            member_report_data = Member.objects.filter(tarikh_daftar__range=[start_date, end_date])
            teacher_report_data = Teacher.objects.filter(tarikh_daftar__range=[start_date, end_date])
            reports = list(member_report_data) + list(teacher_report_data)

            # Set flags for both members and teachers
            for report in member_report_data:
                report.is_member = True
            for report in teacher_report_data:
                report.is_teacher = True

        elif community == 'Saham':
            member_report_data = Member.objects.filter(tarikh_daftar__range=[start_date, end_date], modal_syer__isnull=False)
            reports = list(member_report_data) if member_report_data else []
            for report in reports:
                report.is_member = True

        # Generate report if report_type is specified
        if report_type:
            if community == 'Pelajar':
                return generate_student_report(report_type, reports, start_date, end_date)
            elif community == 'Kakitangan':
                return generate_teacher_report(report_type, reports, start_date, end_date)
            elif community == 'Saham':
                return generate_saham_report(report_type, reports, start_date, end_date)
            elif community == 'Keseluruhan':
                member_data = [r for r in reports if hasattr(r, 'is_member')]
                teacher_data = [r for r in reports if hasattr(r, 'is_teacher')]
                return generate_combined_report(report_type, member_data, teacher_data, start_date, end_date)

        # Print reports for debugging
        print("Reports:", reports)

        # Pass the combined reports list to the template if no report generation
        return render(request, 'generate/muka surat-Hasilkan Laporan.html', {'reports': reports})

    # If the request is not POST, render the report generation page
    return render(request, 'generate/muka surat-Hasilkan Laporan.html', {'reports': reports})

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

def generate_saham_report(report_type, member_data, start_date, end_date):
    if report_type == 'pdf-type':
        return generate_saham_pdf_report(member_data, start_date, end_date)
    elif report_type == 'xlsx-type':
        return generate_saham_excel_report(member_data, start_date, end_date)

def generate_combined_report(report_type, member_data, teacher_data, start_date, end_date):
    if report_type == 'pdf-type':
        return generate_combined_pdf_report(member_data, teacher_data, start_date, end_date)
    elif report_type == 'xlsx-type':
        return generate_combined_excel_report(member_data, teacher_data, start_date, end_date)
    


# Individual PDF generation functions for each community
def generate_student_pdf_report(member_data, start_date, end_date):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Laporan Pelajar.pdf"'
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

    p.title = "Laporan Pelajar"

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

    title = Paragraph("Maklumat Pelajar", title_style)
    date_range = Paragraph(f"From: {start_date.strftime('%d-%m-%Y')} To: {end_date.strftime('%d-%m-%Y')}", styles['Normal'])
    content.append(title)
    content.append(date_range)
    content.append(Spacer(1, 12))

    headers = ["No.", "Nama", "IC", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
    col_proportions = [0.5, 1.5, 1.5, 1, 1.5, 1.5]
    total_proportion = sum(col_proportions)
    col_widths = [(prop / total_proportion) * available_width for prop in col_proportions]

    table_data = [headers]
    cell_style = ParagraphStyle('cell_style', fontSize=8, alignment=1)

    for index, record in enumerate(member_data, start=1):
        table_data.append([
            Paragraph(str(index), cell_style),  # Number column
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
    response['Content-Disposition'] = 'attachment; filename="Laporan Cikgu.pdf"'
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

    p.title = "Laporan Cikgu"


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

    title = Paragraph("Maklumat Cikgu", title_style)
    date_range = Paragraph(f"From: {start_date.strftime('%d-%m-%Y')} To: {end_date.strftime('%d-%m-%Y')}", styles['Normal'])
    content.append(title)
    content.append(date_range)
    content.append(Spacer(1, 12))

    headers = ["No.", "Nama", "IC", "Pangkat", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
    col_proportions = [0.5, 1.5, 1, 1, 0.5, 1, 1.5]  # You can adjust these values
    total_proportion = sum(col_proportions)
    col_widths = [(prop / total_proportion) * available_width for prop in col_proportions]

    table_data = [headers]
    cell_style = ParagraphStyle('cell_style', fontSize=8, alignment=1)

    for index, record in enumerate(teacher_data, start=1):
        table_data.append([
            Paragraph(str(index), cell_style),  # Number column
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

def generate_saham_pdf_report(member_data, start_date, end_date):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Laporan Saham Pelajar.pdf"'
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

    p.title = "Laporan Saham Pelajar"

    content = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="CustomTilte",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        spaceAfter=12
    )

    title = Paragraph("Maklumat Saham Pelajar", title_style)
    date_range = Paragraph(f"From: {start_date.strftime('%d-%m-%Y')} To: {end_date.strftime('%d-%m-%Y')}", styles['Normal'])
    content.append(title)
    content.append(date_range)
    content.append(Spacer(1, 12))

    headers = ["No.", "Nama", "Modal Syer", "Tandatangan"]
    col_proportions = [0.5, 1.5, 1.5, 1]
    total_proportion = sum(col_proportions)
    col_widths = [(prop / total_proportion) * available_width for prop in col_proportions]

    table_data = [headers]
    cell_style = ParagraphStyle('cell_style', fontSize=8, alignment=1)

    for index, record in enumerate(member_data, start=1):
        table_data.append([  
            Paragraph(str(index), cell_style),  # Number column
            Paragraph(record.nama, cell_style),
            Paragraph(f"RM {record.modal_syer:.2f}", cell_style),
            "",  # This will create an empty cell
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
    response['Content-Disposition'] = 'attachment; filename="Laporan Keseluruhan.pdf"'
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

    p.title = "Laporan Keseluruhan"

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
    title = Paragraph("Maklumat Keseluruhan", title_style)
    date_range = Paragraph(f"From: {start_date.strftime('%d-%m-%Y')} To: {end_date.strftime('%d-%m-%Y')}", styles['Normal'])
    content.append(title)
    content.append(date_range)
    content.append(Spacer(1, 12))  # Space after title

    # Table for Students
    if member_data:
        student_header = Paragraph("Maklumat Pelajar", title_style)  # Section header
        content.append(student_header)
        content.append(Spacer(1, 6))  # Space before student table
        
        headers = ["No.", "Nama", "IC", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
        col_proportions = [0.5, 1.5, 1.5, 1, 1.5, 1.5]
        total_proportion = sum(col_proportions)
        col_widths = [(prop / total_proportion) * available_width for prop in col_proportions]

        table_data = [headers]
        cell_style = ParagraphStyle('cell_style', fontSize=8, alignment=1)

        for index, record in enumerate(member_data, start=1):
            table_data.append([
                Paragraph(str(index), cell_style),  # Number column
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
        teacher_header = Paragraph("Maklumat Cikgu", title_style)  # Section header
        content.append(teacher_header)
        content.append(Spacer(1, 6))  # Space before teacher table

        headers = ["No.", "Nama", "IC", "Pangkat", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
        col_proportions = [0.5, 1.5, 1, 1, 0.5, 1, 1]
        total_proportion = sum(col_proportions)
        col_widths = [(prop / total_proportion) * available_width for prop in col_proportions]

        table_data = [headers]
        cell_style = ParagraphStyle('cell_style', fontSize=8, alignment=1)

        for index, record in enumerate(teacher_data, start=1):
            table_data.append([
                Paragraph(str(index), cell_style),  # Number column
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
    response['Content-Disposition'] = 'attachment; filename="Laporan Pelajar.xlsx"'

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
    worksheet.set_column('A:A', 10)  # No
    worksheet.set_column('B:B', 50)  # Nama
    worksheet.set_column('C:C', 20)  # IC
    worksheet.set_column('D:D', 20)  # Ahli
    worksheet.set_column('E:E', 20)  # Modal Syer
    worksheet.set_column('F:F', 20)  # Tarikh Pendaftaran

    # Write header information
    worksheet.merge_range('A1:E1', f'Maklumat Pelajar', workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14}))
    worksheet.write('A2', f'From: {start_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    worksheet.write('A3', f'To: {end_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    
    # Add column headers
    headers = ["No.", "Nama", "IC", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
    for col_num, header in enumerate(headers):
        worksheet.write(4, col_num, header, header_format)

    # Write data to the worksheet
    row = 5  # Start writing data from this row
    
    # Write member data if available
    for idx, record in enumerate(member_data, start=1):
        worksheet.write(row, 0, idx, data_format)  # No
        worksheet.write(row, 1, record.nama, data_format)  # Nama
        worksheet.write(row, 2, record.ic_pelajar, data_format)  # IC
        worksheet.write(row, 3, record.ahli, data_format)  # Ahli
        worksheet.write(row, 4, f'RM {record.modal_syer:.2f}', data_format)  # Modal Syer
        worksheet.write(row, 5, record.tarikh_daftar.strftime('%d-%m-%Y'), data_format)  # Tarikh Pendaftaran
        row += 1

    # Close the workbook and write it to the output stream
    workbook.close()

    output.seek(0)
    response.write(output.read())
    
    return response


def generate_teacher_excel_report(teacher_data, start_date, end_date):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Laporan Cikgu.xlsx"'

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
    worksheet.set_column('A:A', 10)  # Nama
    worksheet.set_column('B:B', 50)  # Nama
    worksheet.set_column('C:C', 20)  # IC
    worksheet.set_column('D:D', 20)  # Pangkat
    worksheet.set_column('E:E', 20)  # Ahli
    worksheet.set_column('F:F', 20)  # Modal Syer
    worksheet.set_column('G:G', 20)  # Tarikh Pendaftaran

    # Write header information
    worksheet.merge_range('A1:F1', f'Maklumat Cikgu', workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14}))
    worksheet.write('A2', f'From: {start_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    worksheet.write('A3', f'To: {end_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    
    # Add column headers
    headers = ["No.", "Nama", "IC", "Pangkat", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
    for col_num, header in enumerate(headers):
        worksheet.write(4, col_num, header, header_format)

    # Write data to the worksheet
    row = 5  # Start writing data from this row
    
    # Write teacher data if available
    for idx, record in enumerate(teacher_data, start=1):
        worksheet.write(row, 0, idx, data_format)  # No
        worksheet.write(row, 1, record.nama, data_format)  # Nama
        worksheet.write(row, 2, record.ic_cikgu, data_format)  # IC
        worksheet.write(row, 3, record.pangkat, data_format)  # Pangkat
        worksheet.write(row, 4, record.ahli, data_format)  # Ahli
        worksheet.write(row, 5, f'RM {record.modal_syer:.2f}', data_format)  # Modal Syer
        worksheet.write(row, 6, record.tarikh_daftar.strftime('%d-%m-%Y'), data_format)  # Tarikh Pendaftaran
        row += 1

    # Close the workbook and write it to the output stream
    workbook.close()

    output.seek(0)
    response.write(output.read())
    
    return response

def generate_saham_excel_report(member_data, start_date, end_date):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Laporan Saham Pelajar.xlsx"'

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

    # Adjust column widths for 3 columns
    worksheet.set_column('A:A', 10)  # No
    worksheet.set_column('B:B', 50)  # Nama
    worksheet.set_column('C:C', 20)  # Modal Syer
    worksheet.set_column('D:D', 20)  # Tandatangan

    # Write title and date range (header information)
    worksheet.merge_range('A1:C1', 'Maklumat Saham Pelajar', workbook.add_format({
        'bold': True, 
        'align': 'center', 
        'font_size': 14, 
        'valign': 'vcenter'
    }))
    
    worksheet.write('A2', f'From: {start_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    worksheet.write('A3', f'To: {end_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))

    # Add column headers in row 5
    headers = ["No.", "Nama", "Modal Syer", "Tandatangan"]
    for col_num, header in enumerate(headers):
        worksheet.write(4, col_num, header, header_format)

    # Write data to the worksheet (starting from row 5)
    row = 5  # Start writing data from this row
    
    # Write member data if available
    for idx, record in enumerate(member_data, start=1):
        worksheet.write(row, 0, idx, data_format)  # No
        worksheet.write(row, 1, record.nama, data_format)  # Nama
        worksheet.write(row, 2, f'RM {record.modal_syer:.2f}', data_format)  # Modal Syer
        worksheet.write(row, 3, "", data_format)  # Tandatangan (empty for manual signing)
        row += 1

    # Close the workbook and write it to the output stream
    workbook.close()

    output.seek(0)
    response.write(output.read())
    
    return response


def generate_combined_excel_report(member_data, teacher_data, start_date, end_date):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Laporan Keseluruhan.xlsx"'

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
    worksheet.set_column('A:A', 10)   # No
    worksheet.set_column('B:B', 20)   # Nama
    worksheet.set_column('C:C', 20)   # IC
    worksheet.set_column('D:D', 20)   # Pangkat
    worksheet.set_column('E:E', 20)   # Ahli
    worksheet.set_column('F:F', 20)   # Modal Syer
    worksheet.set_column('G:G', 20)   # Tarikh Pendaftaran

    # Write header information
    worksheet.merge_range('A1:F1', f'Maklumat Keseluruhan ', workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14}))
    worksheet.write('A2', f'From: {start_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))
    worksheet.write('A3', f'To: {end_date.strftime("%d-%m-%Y")}', workbook.add_format({'align': 'left'}))

    # Initialize row count
    row = 5  

    # Add student data if available
    if member_data:
        worksheet.write(row, 0, 'Student Data', header_format)
        row += 1
        headers = ["No.", "Nama", "IC", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
        for col_num, header in enumerate(headers):
            worksheet.write(row, col_num, header, header_format)
        row += 1

        for idx, record in enumerate(member_data, start=1):
            worksheet.write(row, 0, idx, data_format)  # No
            worksheet.write(row, 1, record.nama, data_format)  # Nama
            worksheet.write(row, 2, record.ic_pelajar, data_format)  # IC
            worksheet.write(row, 3, record.ahli, data_format)  # Ahli
            worksheet.write(row, 4, f'RM {record.modal_syer:.2f}', data_format)  # Modal Syer
            worksheet.write(row, 5, record.tarikh_daftar.strftime('%d-%m-%Y'), data_format)  # Tarikh Pendaftaran
            row += 1
        row += 2  # Add extra space after students

    # Add teacher data if available
    if teacher_data:
        worksheet.write(row, 0, 'Teacher Data', header_format)
        row += 1
        headers = ["No.", "Nama", "IC", "Pangkat", "Ahli", "Modal Syer", "Tarikh Pendaftaran"]
        for col_num, header in enumerate(headers):
            worksheet.write(row, col_num, header, header_format)
        row += 1

        for idx, record in enumerate(teacher_data, start=1):
            worksheet.write(row, 0, idx, data_format)  # No
            worksheet.write(row, 1, record.nama, data_format)  # Nama
            worksheet.write(row, 2, record.ic_cikgu, data_format)  # IC
            worksheet.write(row, 3, record.pangkat, data_format)  # Pangkat
            worksheet.write(row, 4, record.ahli, data_format)  # Ahli
            worksheet.write(row, 5, f'RM {record.modal_syer:.2f}', data_format)  # Modal Syer
            worksheet.write(row, 6, record.tarikh_daftar.strftime('%d-%m-%Y'), data_format)  # Tarikh Pendaftaran
            row += 1

    # Close the workbook and write it to the output stream
    workbook.close()

    output.seek(0)
    response.write(output.read())
    
    return response