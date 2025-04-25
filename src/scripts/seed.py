#!/usr/bin/env python3

import random
import string

from sqlmodel import Session

from src.settings import RUN_MODE, RunMode

if RUN_MODE != RunMode.DEVELOPMENT:
    raise Exception("Database seeding is only allowed in development mode.")

from src.auth.crypto import hash_password
from src.db.common import engine
from src.model.note import Note
from src.model.user import User


def seed_db():
    Note.metadata.drop_all(engine)
    Note.metadata.create_all(engine)

    with Session(engine) as session:
        users = [
            User(
                username=f"user{i}",
                hashed_password=hash_password(f"password{i}"),
            )
            for i in range(10)
        ]
        notes = [
            Note(
                title=f"Note {i}",
                content=f"This is the content of note {i}. "
                + "".join(
                    random.choices(
                        string.ascii_letters + string.digits + " " * 10,
                        k=100,
                    )
                ),
            )
            for i in range(30)
        ]

        session.add_all(users)
        session.add_all(notes)

        session.commit()


if __name__ == "__main__":
    seed_db()
    print("OK!")
