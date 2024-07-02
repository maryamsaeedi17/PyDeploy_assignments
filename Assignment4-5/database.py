from sqlmodel import Field, SQLModel, create_engine, Session, select

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    city: str = Field()
    username: str = Field()
    passwors: str = Field()

engine = create_engine('sqlite:///./database.db', echo=True)
SQLModel.metadata.create_all(engine)

def get_user_by_username(username: str):
    with Session(engine) as db_session:
            statement = select(User).where(User.username == username)
            user = db_session.exec(statement).first()

def create_user(username: str, hashed_password: str):
    user = User(username=username, password=hashed_password)
    with Session(engine) as db_session:
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user