from backend.db import Base, engine, get_db
from backend.models import projects, users
from backend.schemas.users import UserType
from config import settings


# init database
Base.metadata.create_all(bind=engine)


session = next(get_db())


session.add(
    users.User.create_user(
        settings.admin_user, settings.admin_pass, "Admin", "Admin", int(UserType.admin)
    )
)
session.commit()
