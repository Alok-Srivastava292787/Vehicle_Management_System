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

from app.utils.pdf_footer import (
    add_pdf_footer,
)


class PDFIssueService:

    @staticmethod
    def generate_issue_pdf(
        issue,
        issued_by,
        received_by,
        details,
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

        elements.append(
            Paragraph(
                "PART ISSUE",
                styles["Title"],
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        header = [

            [
                "Issue Number",
                issue.issue_number,
            ],

        [
            "Issue Date",
            (
                issue.issue_date.strftime(
                    "%d-%b-%Y %H:%M"
                )
                if issue.issue_date
                else "-"
            ),
        ],
            [
                "Status",
                issue.status,
            ],

            [
                "Issued By",
                issued_by.full_name
                if issued_by
                else "-",
            ],

            [
                "Received By",
                received_by.full_name
                if received_by
                else "-",
            ],

            [
                "Requisition",
                getattr(
                    issue,
                    "requisition_number",
                    "-"
                ) or "-",
            ],
        ]

        header_table = Table(
            header,
            colWidths=[
                150,
                330,
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
            Spacer(1, 20)
        )

        rows = [[
            "Part",
            "Qty Issued",
            "Serial Number",
            "Remarks",
        ]]

        total_qty = 0

        for detail in details:

            qty = float(
                detail.quantity_issued
                or 0
            )

            total_qty += qty

            rows.append([
                part_lookup.get(
                    detail.part_id,
                    "-"
                ),
                f"{qty:.2f}",
                detail.serial_number
                or "-",
                detail.remarks
                or "-",
            ])

        table = Table(
            rows,
            colWidths=[
                140,
                90,
                120,
                150,
            ],
        )

        table.setStyle(
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

                (
                    "TEXTCOLOR",
                    (1, 1),
                    (1, -1),
                    colors.blue,
                ),
            ])
        )

        elements.append(
            table
        )

        elements.append(
            Spacer(1, 20)
        )

        summary = Table(
            [[
                "Total Quantity Issued",
                f"{total_qty:.2f}",
            ]],
            colWidths=[180, 120],
        )

        summary.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),
                (
                    "TEXTCOLOR",
                    (1, 0),
                    (1, 0),
                    colors.blue,
                ),
            ])
        )

        elements.append(
            summary
        )

#        elements.append(
#            Spacer(1, 35)
#        )

        elements.append(
            Spacer(1, 18)
        )

        elements.append(
            Paragraph(
                f"<b>Issue Status: </b>{issue.status}",
                styles["Normal"],
            )
        )
        elements.append(
            Spacer(1, 4)
        )

        elements.append(
            Paragraph(
                "Related Documents",
                styles["Heading2"],
            )
        )
        related_text = f"""
            <b>Requisition :</b>
            {getattr(issue, "requisition_number", "-")}
            <b>Job Card :</b>
            {getattr(issue, "job_card_id", "-")}
            """

        elements.append(
            Paragraph(
                related_text,
                styles["Normal"],
            )
        )
        elements.append(
            Spacer(1, 8)
        )

        signature = Table(
            [[
                "Store Keeper",
                "Receiver",
                "Approver",
            ]],
            colWidths=[
                165,
                165,
                165,
            ],
        )

        signature.setStyle(
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
            signature
        )

        add_pdf_footer(
            elements
        )

        doc.build(
            elements
        )

        buffer.seek(0)

        return buffer