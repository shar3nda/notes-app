#!/usr/bin/env python3

import random
import string

from sqlmodel import Session, select

from src.settings import RUN_MODE, RunMode

if RUN_MODE != RunMode.DEV:
    raise Exception("Database seeding is only allowed in development mode.")

from src.auth.crypto import hash_password
from src.db.common import engine
from src.model.note import Note
from src.model.user import User


def seed_db():
    Note.metadata.drop_all(engine)
    Note.metadata.create_all(engine)
    User.metadata.drop_all(engine)
    User.metadata.create_all(engine)

    with Session(engine) as session:
        users = [
            User(
                username=f"user{i}",
                hashed_password=hash_password(f"password{i}"),
            )
            for i in range(1, 6)
        ]
        session.add_all(users)
        session.commit()

        users = session.exec(select(User)).all()
        notes = []
        for user in users:
            notes.extend(
                [
                    Note(
                        title=f"Note {i}",
                        content=f"This is the content of note {i}. "
                        + "".join(
                            random.choices(
                                string.ascii_letters + string.digits + " " * 10,
                                k=100,
                            )
                        ),
                        user_id=user.id,
                    )
                    for i in range(1, 31)
                ]
            )

        session.add_all(notes)
        session.commit()


if __name__ == "__main__":
    seed_db()
    print("OK!")
