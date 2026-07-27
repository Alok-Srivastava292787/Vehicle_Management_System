from fastapi import (APIRouter,Depends,)    #type: ignore

from fastapi.responses import (    StreamingResponse,)  #type: ignore

from sqlalchemy.orm import (
    Session,
)

from app.db.dependencies import (
    get_db,
)

from app.repositories.part_return_repository import (
    PartReturnRepository,
)

from app.repositories.part_return_detail_repository import (
    PartReturnDetailRepository,
)

from app.repositories.employee_repository import (
    EmployeeRepository,
)

from app.repositories.part_repository import (
    PartRepository,
)

from app.services.pdf_return_service import (
    PDFReturnService,
)

router = APIRouter(
    prefix="/api/v1/return_print",
    tags=["Part Return PDF"],
)


@router.get(
    "/{return_id}/pdf"
)
def generate_return_pdf(
    return_id: int,
    db: Session = Depends(get_db),
):

    return_repo = (
        PartReturnRepository(db)
    )

    part_return = (
        return_repo.get_by_id(
            return_id
        )
    )

    if not part_return:

        return {
            "message":
            "Part Return not found"
        }

    detail_repo = (
        PartReturnDetailRepository(
            db
        )
    )

    details = [

        item

        for item in (
            detail_repo.get_all()
        )

        if item.return_id
        == return_id

    ]

    employee_repo = (
        EmployeeRepository(
            db
        )
    )

    returned_by = None
    received_by = None

    if (
        part_return
        .returned_by_employee_id
    ):

        returned_by = (
            employee_repo.get_by_id(
                part_return
                .returned_by_employee_id
            )
        )

    if (
        part_return
        .received_by_employee_id
    ):

        received_by = (
            employee_repo.get_by_id(
                part_return
                .received_by_employee_id
            )
        )

    part_repo = (
        PartRepository(db)
    )

    part_lookup = {}

    for detail in details:

        part = (
            part_repo.get_by_id(
                detail.part_id
            )
        )

        if part:

            part_lookup[
                detail.part_id
            ] = (
                part.part_name
            )

    pdf_stream = (
        PDFReturnService
        .generate_return_pdf(
            part_return,
            returned_by,
            received_by,
            details,
            part_lookup,
        )
    )

    return StreamingResponse(
        pdf_stream,
        media_type=
        "application/pdf",
        headers={
            "Content-Disposition":
            (
                f'inline; '
                f'filename="return_{return_id}.pdf"'
            )
        },
    )