from fastapi import APIRouter, HTTPException
from sqlmodel import Session, func, select

from db.common import engine
from model.note import Note, NoteCreate, NoteRead, NoteReadShort, NoteUpdate

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=NoteRead)
def create_note(note_create: NoteCreate):
    note = Note(**note_create.model_dump())
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
        return note


@router.get("/", response_model=list[NoteRead])
def get_notes():
    with Session(engine) as session:
        stmt = select(
            Note.id,
            Note.title,
            func.substring(Note.content, 1, 50).label("content"),
            Note.updated_at,
            Note.created_at,
        ).order_by(Note.updated_at.desc())
        result = session.exec(stmt).all()
        return result


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note


@router.put("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, updated_note: NoteUpdate):
    with Session(engine) as session:
        db_note = session.get(Note, note_id)
        if not db_note:
            raise HTTPException(status_code=404, detail="Note not found")
        note_data = updated_note.model_dump(exclude_unset=True)
        db_note.sqlmodel_update(note_data)
        session.add(db_note)
        session.commit()
        session.refresh(db_note)
        return db_note


@router.delete("/{note_id}", response_model=NoteReadShort)
def delete_note(note_id: int):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        session.delete(note)
        session.commit()
        return NoteReadShort(id=note.id)
