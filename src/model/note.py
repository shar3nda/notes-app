from datetime import datetime

from sqlmodel import Field, SQLModel

from db.common import created_at, updated_at


class NoteBase(SQLModel):
    title: str
    content: str


class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = created_at()
    updated_at: datetime = updated_at()


class NoteMetadata(SQLModel):
    id: int
    title: str
    content_preview: str
    created_at: datetime
    updated_at: datetime


class NoteCreate(NoteBase):
    pass


class NoteUpdate(SQLModel):
    title: str | None = None
    content: str | None = None


class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime


class NoteReadShort(SQLModel):
    id: int
