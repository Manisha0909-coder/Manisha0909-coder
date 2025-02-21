from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
from datetime import date,timedelta
from sqlalchemy.orm import Session
from database import sessionLocal, Base, engine,HabitDB


#Dependency to get DB session
def get_db():
    db= sessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Habit model
class Habit(BaseModel):
    name: str
    description: str
    completed: bool = False
    progress: Dict[str,bool]={}

# In-memory database (dict for simplicity)
#habits: Dict[int, Habit] = {}

habit_id_counter = 1

@app.get("/")
def home():
    return {"message": "Welcome to the Habit Tracker API!"}

@app.post("/habits/")
def create_habit(habit: Habit, db:Session = Depends(get_db)):
    new_habit = HabitDB(
        name = habit.name,
        description = habit.description,
        completed = habit.completed,
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    
    
    #global habit_id_counter
    #habits[habit_id_counter] = habit
    #habit_id_counter += 1
    return {"message": "Habit added successfully", "habit_id": new_habit.id}

#Get single Habit
@app.get("/habits/{habit_id}")
def get_habit(habit_id: int,db: Session =Depends(get_db)):
    habit = db.query(HabitDB).filter(HabitDB.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

#Get all habits
@app.get("/habits/")
def get_all_habits(db: Session = Depends(get_db)):
    habits = db.query(HabitDB).all()
    return habits

#Update Habit
@app.put("/habits/{habit_id}")
def update_habit(habit_id: int, habit:Habit, db: Session = Depends(get_db)):
    db_habit = db.query(HabitDB).filter(HabitDB.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    db_habit.name = habit.name
    db_habit.description = habit.description
    db_habit.completed = habit.completed
    db.commit()

    return {"message": "Habit updated successfully"}

@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db:Session = Depends(get_db)):
    habit = db.query(HabitDB).filter(HabitDB.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted successfully"}

@app.post("/habits/{habit_id}/completed")
def habit_completed(habit_id:int, db: Session = Depends(get_db)):
    habit = db.query(HabitDB).filter(HabitDB.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    #today = str(date.today())
    #habits[habit_id].progress[today]=True

    today = date.today()
    if habit.last_completed_date == today:
        return{"message":f"Habit {habit_id} already marked today"}
    
    if habit.last_completed_date == today - timedelta(days=1):
        habit.streak+=1 #Increment 
    else:
        habit.streak=1 #Reset the streak if skipped the day
    
    habit.last_completed_date = today
    db.commit()
    return{"message":f"Habit {habit_id} marked completed today"}


@app.get("/habits/{habit_id}/progress")
def get_habit_progress(habit_id:int,db:Session = Depends(get_db)):
    habit =db.query(HabitDB).filter(HabitDB.id == habit_id).first()

    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
        #raise HTTPException(status_code=400, detail="Invalid request")
    return {"habit_id":habit.id,"name":habit.name,"streak": habit.streak,"last_completed_date":habit.last_completed_date}
