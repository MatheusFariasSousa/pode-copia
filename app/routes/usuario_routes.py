from typing import List
from fastapi import APIRouter, Response, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from db.database import engine,SessionLocal, get_db
from db.models import Usuarios as UsuariosModel
from schemas.usuario import Usuarios as UsuariosSchema

from db.base import Base


#cria a tabela
Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/usuarios")



@router.post("/addComSchema", status_code=status.HTTP_201_CREATED, description='Adicionar user')
def add_user(request:UsuariosSchema, db: Session = Depends(get_db)):
        # produto_on_db = ProdutosModel(id=request.id, item=request.item, peso=request.peso, numero_caixas=request.numero_caixas)
        user_on_db_ = UsuariosModel(**request.dict())
        db.add(user_on_db_)
        db.commit()
        db.refresh(user_on_db_)
        return user_on_db_


@router.get("/listar_todos", response_model=list[SetorResponse])
def find_all(db: Session = Depends(get_db)):
    setores = SetorRepository.find_all(db)
    return [SetorResponse.from_orm(setor) for setor in setores]


@router.get("/procurar_por_id/{id}", response_model=SetorResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    setor = SetorRepository.find_by_id(db, id)
    if not setor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Setor não encontrado"
        )
    return SetorResponse.from_orm(setor)


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not SetorRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Setor não encontrado"
        )
    SetorRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update/{id}", response_model=SetorResponse)
def update(id: int, request: SetorRequest, db: Session = Depends(get_db)):
    if not SetorRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Setor não encontrado"
        )
    setor = SetorRepository.save(db, SetorModel(id=id, **request.dict()))
    return SetorResponse.from_orm(setor)