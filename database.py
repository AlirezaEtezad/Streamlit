from sqlmodel import SQLModel, Session, create_engine, select
from models import User, Message, Optional


DATABASE_URL = "sqlite:///database.db"
# DATABASE_URL = "postgresql://admin:123-localhost:5432/chatbotdb"
# DATABASE_URL = "postgresql://root:YBfURfdyej4NgjOhVN1k0Q1Z@aaa:5432/postgres"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user(name: str, email: str, password: str) -> Optional[User]:
    with Session(engine) as session:
        if get_user_by_email(session, email):
            return None
        user = User(name=name, email=email)
        user.set_password(password)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

def authenticate_user(email: str, password: str) -> Optional[User]:
    with Session(engine) as session:
        user = get_user_by_email(session, email)
        if user and user.verify_password(password):
            return user
    return None
