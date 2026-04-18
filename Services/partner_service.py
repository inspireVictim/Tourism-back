from sqlalchemy.orm import Session

from Repositories import partner_repo
from Schemas.partner import PartnerCreate


def create_partner(db: Session, partner_data: PartnerCreate):
    return partner_repo.create_partner(db, partner_data)


def get_all_partners(db: Session, skip: int = 0, limit: int = 10):
    return partner_repo.get_partners(db, skip=skip, limit=limit)
