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


class PDFReturnService:

    @staticmethod
    def generate_return_pdf(
        part_return,
        returned_by,
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
                "PART RETURN",
                styles["Title"],
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        header_data = [

            [
                "Return Number",
                part_return.return_number,
            ],

            [
                "Return Date",
                str(
                    part_return.return_date
                ),
            ],

            [
                "Issue Reference",
                str(
                    part_return.issue_id
                ),
            ],

            [
                "Returned By",
                returned_by.full_name
                if returned_by
                else "-",
            ],

            [
                "Received By",
                received_by.full_name
                if received_by
                else "-",
            ],

            [
                "Status",
                part_return.status,
            ],
        ]

        header_table = Table(
            header_data,
            colWidths=[
                150,
                330,
            ],
        )

        header_table.setStyle(
            TableStyle(
                [
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
                ]
            )
        )

        elements.append(
            header_table
        )

        elements.append(
            Spacer(1, 20)
        )

        rows = [[
            "Part",
            "Qty Returned",
            "Serial Number",
            "Remarks",
        ]]

        total_qty = 0

        for detail in details:

            qty = float(
                detail.quantity_returned
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

        detail_table = Table(
            rows,
            colWidths=[
                140,
                90,
                120,
                150,
            ],
        )

        detail_table.setStyle(
            TableStyle(
                [
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
                        colors.green,
                    ),
                ]
            )
        )

        elements.append(
            detail_table
        )

        elements.append(
            Spacer(1, 20)
        )

        totals_table = Table(
            [
                [
                    "Total Quantity Returned",
                    f"{total_qty:.2f}",
                ]
            ],
            colWidths=[
                180,
                120,
            ],
        )

        totals_table.setStyle(
            TableStyle(
                [
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
                        colors.green,
                    ),
                ]
            )
        )

        elements.append(
            totals_table
        )

        elements.append(
            Spacer(1, 35)
        )

        signature_table = Table(
            [
                [
                    "Returned By",
                    "Store Keeper",
                    "Approver",
                ]
            ],
            colWidths=[
                165,
                165,
                165,
            ],
        )

        signature_table.setStyle(
            TableStyle(
                [
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
                ]
            )
        )

        elements.append(
            signature_table
        )

        add_pdf_footer(
            elements
        )

        doc.build(
            elements
        )

        buffer.seek(0)

        return buffer