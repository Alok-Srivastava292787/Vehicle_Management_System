from app.models.maintenance import JobCardPart
class JobCardPartService:

    def __init__(
        self,
        part_repo
    ):

        self.part_repo = part_repo

    def create_part(
        self,
        payload
    ):

        obj = JobCardPart(
            job_card_id=payload.job_card_id,
            part_id=payload.part_id,
            quantity=payload.quantity,
            unit_price=payload.unit_price,
            total_price=
            payload.quantity
            * payload.unit_price
        )

        return self.part_repo.create(
            obj
        )