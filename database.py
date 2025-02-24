from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import date

DATABASE_URL = "sqlite:///./habits.db"

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()


#Habit base model
class HabitDB(Base):
    __tablename__="habits"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default= False)
    #last_completed_date = Column(Date, nullable=True)
    created_date = Column(Date, default=date.today)

    #Progress Tracking
    streak = Column(Integer, default=0)
    last_completed_date = Column(Date, nullable=True)
# Create table
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
