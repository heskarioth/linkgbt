from typing import cast

from pydantic import BaseSettings


from starlite import Starlite, State


import mongoengine

def global_init():
    mongoengine.register_connection(alias='core',name='mycontentgenerator')


class AppSettings(BaseSettings):
    DATABASE_URI: str = "postgresql+asyncpg://postgres:mysecretpassword@pg.db:5432/db"


settings = AppSettings()


def get_db_connection(state: State):
    """Returns the db engine.

    If it doesn't exist, creates it and saves it in on the application state object
    """
    if not getattr(state, "engine", None):
        state.engine = mongoengine.register_connection(alias='core',name='mycontentgenerator')
    return state.engine


async def close_db_connection(state: State) -> None:
    """Closes the db connection stored in the application State object."""
    if getattr(state, "engine", None):
        state.engine.unregister_connection(alias='core',name='mycontentgenerator')


