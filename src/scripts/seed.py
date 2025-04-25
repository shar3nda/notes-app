#!/usr/bin/env python3

from sqlmodel import Session

from settings import RUN_MODE, RunMode

if RUN_MODE != RunMode.DEVELOPMENT:
    raise Exception("Database seeding is only allowed in development mode.")

from src.db.common import engine
from src.model.note import Note


def seed_db():
    Note.metadata.drop_all(engine)
    Note.metadata.create_all(engine)

    with Session(engine) as session:
        notes = [
            Note(title=f"Note {i}", content=f"This is the content of note {i}")
            for i in range(100)
        ]

        session.add_all(notes)

        session.commit()


if __name__ == "__main__":
    seed_db()
    print("OK!")
