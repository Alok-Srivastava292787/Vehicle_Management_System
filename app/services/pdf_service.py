from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import (
    getSampleStyleSheet,
)

from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from app.utils.pdf_footer import add_pdf_footer

class PDFService:

    @staticmethod
    def generate_job_card_pdf(
        job_card,
        vehicle,
        driver,
        technician1,
        technician2,
        requested_by,
        verified_by,
        approved_by,
        parts,
        part_lookup,
    ):
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
        )
        styles = (
            getSampleStyleSheet()
        )
        elements = []
        title = Paragraph(
            "VEHICLE JOB CARD",
            styles["Title"],
        )
        elements.append(title)
        elements.append(
            Spacer(1, 2)
        )
        header_data = [
            [ "Job Card No", str(job_card.job_card_id),],
            [ "Vehicle",   vehicle.vehicle_id
                if vehicle
                else "-",
            ],
            [ "Driver",   driver.driver_name
                if driver
                else "-",
            ],
            [ "Technician 1",   technician1.full_name
                if technician1
                else "-",
            ],
            [ "Technician 2",   technician2.full_name
                if technician2
                else "-",
            ],
            [ "Status",
                job_card.job_status
                or "-",
            ],
            [ "Maintenance Type",
                job_card.maintenance_type
                or "-",
            ],
            [ "Zone",
                job_card.zone_area
                or "-",
            ],
            [
                "Mileage",
                job_card.mileage_hours
                or "-",
            ],
            [
                "Date Time In",
                str(
                    job_card.date_time_in
                    or "-"
                ),
            ],

            [
                "Date Time Out",
                str(
                    job_card.date_time_out
                    or "-"
                ),
            ],
        ]
        header_table = Table(
            header_data,
            colWidths=[
                140,
                320,
            ],
        )
        header_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
            ])
        )
        elements.append(
            header_table
        )
        elements.append(
            Spacer(1, 4)
        )
        elements.append(
            Paragraph(
                "<b>Issue Reported</b>",
                styles["Heading2"],
            )
        )
        elements.append(
            Paragraph(
                job_card.issue_reported
                or "-",
                styles["Normal"],
            )
        )
        elements.append(
            Spacer(1, 4)
        )
        elements.append(
            Paragraph(
                "<b>Problems Found & Action Taken</b>",
                styles["Heading2"],
            )
        )
        elements.append(
            Paragraph(
                job_card.problem_found_action_taken
                or "-",
                styles["Normal"],
            )
        )
        elements.append(
            Spacer(1, 4)
        )
        elements.append(
            Paragraph(
                "Parts Used",
                styles["Heading2"],
            )
        )
        elements.append(
            Spacer(1, 2)
        )
        active_parts = [
            part
            for part in parts
            if part.active_flag
        ]

        part_count = len(
            active_parts
        )

        total_parts_cost = 0
        grand_total=0
        part_rows = [    
            [
                "Part Name",
                "Quantity",
                "Unit Price",
                "Total"
            ]
        ]
        for part in active_parts:
            part_name = part_lookup.get(
                part.part_id,
                "-"
            )
            qty = part.quantity or 0
            price = ( part.unit_price or 0 )
            total = qty * price
            total_parts_cost += total
            part_rows.append(
                [
                    part_name,
                    str(qty),
                    str(round(float(price), 2)),
                    str(round(float(total), 2)),
                ]
            )
            part_table = Table(
            part_rows,
            colWidths=[150, 100],
            
        )
        labour_charges = (
            job_card.labour_charges
            or 0
        )

        grand_total = (
            total_parts_cost
            + labour_charges
        )

        part_rows.append(
            [
                "",
                "",
                "Parts Total",
                f"{total_parts_cost:.2f}",
            ]
        )
        part_rows.append(
            [
                "",
                "",
                "Labour",
                f"{labour_charges:.2f}",
            ]
        )
        part_rows.append(
            [
                "",
                "",
                "Grand Total",
                f"{grand_total:.2f}",
            ]
        )
        part_table = Table(
        part_rows,
        colWidths=[150, 100],)

        part_table.setStyle(
            TableStyle([
            
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),
        
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
            ])
        )
        elements.append(
            part_table
        )
        elements.append(
            Spacer(1, 8)
        )

        elements.append(
            Paragraph(
                "<b>Cost Summary</b>",
                styles["Heading2"],
            )
        )

        cost_text = f"""
        Active Parts : {part_count}

        Parts Cost : Rs.{total_parts_cost:.2f}

        Labour Cost : Rs.{labour_charges:.2f}

        <b>Grand Total : Rs.{grand_total:.2f}</b>
        """

        elements.append(
            Paragraph(
                cost_text,
                styles["Normal"],
            )
        )
        v_approved_at=(
            job_card.approved_at.strftime(
                "%d-%b-%Y %H:%M"
            )
            if job_card.approved_at
            else "-"
        )
        v_requested_at=(
                job_card.requested_at.strftime(
                    "%d-%b-%Y %H:%M"
                )
                if job_card.requested_at
                else "-"
            )
        v_verified_at=(
            job_card.verified_at.strftime(
                "%d-%b-%Y %H:%M"
            )
            if job_card.verified_at
            else "-"
        )
        requisition_number = (
            getattr(
                job_card,
                "requisition_slip_number",
                None
            )
            or "-"
        )

        approval_data = [

            [
                "Current Status",
                job_card.job_status
                or "-"
            ],
            [
                "Requested By",
                requested_by.full_name
                if requested_by
                else "-"
            ],

            [
                "Requested At",v_requested_at
            ],

            [
                "Verified By",
                verified_by.full_name
                if verified_by
                else "-"
            ],

            [
                "Verified At",v_verified_at
            ],

            [
                "Approved By",
                approved_by.full_name
                if approved_by
                else "-"
            ],

            [
                "Approved At",v_approved_at
            ],

        ]

        approval_table = Table(
            approval_data,
            colWidths=[
                140,
                320,
            ],
        )
        approval_table.setStyle(
            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
            ])
        )
        elements.append(
            Paragraph(
                "<b>Approval Workflow</b>",
                styles["Heading2"],
            )
        )
        elements.append(
            Paragraph(
                f'<b>STATUS :→</b> {job_card.job_status or "-"}',
                styles["Normal"],
            )
        )
        approval_text = f"""

        <b>Requested By:</b> {
            requested_by.full_name
            if requested_by else "-"
        }
        
        ({v_requested_at})

        <b> → Verified By:</b> {
            verified_by.full_name
            if verified_by else "-"
        }
        
        ({v_verified_at})

        <b> → Approved By</b> : {
            approved_by.full_name
            if approved_by else "-"
        }
        
        ({v_approved_at})
        """
                
        elements.append(
            Paragraph(
                approval_text,
                styles["Normal"],
            )
        )
        elements.append(
            Spacer(1, 4)
        )

        elements.append(
            Paragraph(
                "<b>Related Documents</b>",
                styles["Heading2"],
            )
        )

        related_text = f"""
        Requisition :
        {requisition_number        }
        """

        elements.append(
            Paragraph(
                related_text,
                styles["Normal"],
            )
        )
        elements.append(
            Spacer(1, 40)
        )
        signature_table = Table(
            [[
                "Requested By",
                "Verified By",
                "Approved By",
            ]],
            colWidths=[
                170,
                170,
                170,
            ],
        )
        signature_table.setStyle(
            TableStyle([
                (
                    "LINEABOVE",
                    (0, 0),
                    (-1, 0),
                    1,
                    colors.black,
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
            ])
        )
        elements.append(
            signature_table
        )
        add_pdf_footer(elements)
        doc.build(
            elements
        )
        buffer.seek(0)
        return buffer