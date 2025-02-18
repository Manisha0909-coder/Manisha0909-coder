from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from datetime import date

app = FastAPI()

# Habit model
class Habit(BaseModel):
    name: str
    description: str
    completed: bool = False
    progress: Dict[str,bool]={}

# In-memory database (dict for simplicity)
habits: Dict[int, Habit] = {}

habit_id_counter = 1

@app.get("/")
def home():
    return {"message": "Welcome to the Habit Tracker API!"}

@app.post("/habits/")
def create_habit(habit: Habit):
    global habit_id_counter
    habits[habit_id_counter] = habit
    habit_id_counter += 1
    return {"message": "Habit added successfully", "habit_id": habit_id_counter - 1}

@app.get("/habits/{habit_id}")
def get_habit(habit_id: int):
    if habit_id not in habits:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habits[habit_id]

@app.get("/habits/")
def get_all_habits():
    return habits

@app.put("/habits/{habit_id}")
def update_habit(habit_id: int, habit: Habit):
    if habit_id not in habits:
        raise HTTPException(status_code=404, detail="Habit not found")
    habits[habit_id] = habit
    return {"message": "Habit updated successfully"}

@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int):
    if habit_id not in habits:
        raise HTTPException(status_code=404, detail="Habit not found")
    del habits[habit_id]
    return {"message": "Habit deleted successfully"}

@app.post("/habits/{habit_id}/completed")
def habit_completed(habit_id:int):
    if habit_id not in habits:
        raise HTTPException(status_code=404,details="Habit not found")
    
    today = str(date.today())
    habits[habit_id].progress[today]=True
    return{"message":f"Habit {habit_id} marked completed today"}
