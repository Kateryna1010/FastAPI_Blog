from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models
from ..hashing import Hash


def create(request: schemas.User, db: Session):
    email = db.query(models.User).filter(models.User.email == request.email).first()
    if email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'User with such email already exists')
    hashed_pwd = Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not available')
    return user