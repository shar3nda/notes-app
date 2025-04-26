from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from src.auth.user import get_current_user
from src.db.common import engine
from src.model.note import Note, NoteCreate, NoteRead, NoteReadShort, NoteUpdate
from src.model.user import User

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=NoteRead)
def create_note(note_create: NoteCreate, user: User = Depends(get_current_user)):
    note = Note(**note_create.model_dump(), user_id=user.id)
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
        return note


@router.get("/", response_model=list[NoteRead])
def get_notes(user: User = Depends(get_current_user)):
    with Session(engine) as session:
        stmt = select(
            Note.id,
            Note.title,
            func.substring(Note.content, 1, 50).label("content"),
            Note.updated_at,
            Note.created_at,
        ).where(Note.user_id == user.id)
        stmt = stmt.order_by(Note.updated_at.desc())
        result = session.exec(stmt).all()
        return result


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note or note.user_id != user.id:
            raise HTTPException(status_code=404, detail="Note not found")
        return note


@router.put("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int,
    updated_note: NoteUpdate,
    user: User = Depends(get_current_user),
):
    with Session(engine) as session:
        db_note = session.get(Note, note_id)
        if not db_note or db_note.user_id != user.id:
            raise HTTPException(status_code=404, detail="Note not found")
        note_data = updated_note.model_dump(exclude_unset=True)
        db_note.sqlmodel_update(note_data)
        session.add(db_note)
        session.commit()
        session.refresh(db_note)
        return db_note


@router.delete("/{note_id}", response_model=NoteReadShort)
def delete_note(note_id: int, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note or note.user_id != user.id:
            raise HTTPException(status_code=404, detail="Note not found")
        session.delete(note)
        session.commit()
        return NoteReadShort(id=note.id)
