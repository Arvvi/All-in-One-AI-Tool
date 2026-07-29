from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite डेटाबेस फाइल का नाम
SQLALCHEMY_DATABASE_URL = "sqlite:///./chat_history.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# चैट सेव करने वाली टेबल का डिज़ाइन
class ChatRecord(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    ai_response = Column(String)

# असली डेटाबेस क्रिएट करना
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()