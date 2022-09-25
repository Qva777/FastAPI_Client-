from fastapi import FastAPI, HTTPException, Query, Body, Depends
from typing import Optional, List, Union

from fastapi.encoders import jsonable_encoder

from application import models
# from application.models import TaskDB, ManagerDB
from application.schemas import Task, Manager
from application.database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI(title="FastAPI_Client")
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# TASK URL
@app.get('/api/all-tasks/', tags=["GET Methods"])
async def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(models.TaskDB).all()


@app.get('/api/task/{task_id}', tags=["GET Methods"])
async def get_task(task_id: int, db: Session = Depends(get_db)):
    return db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()


@app.post("/api/create-task", tags=["POST Methods"])
def create_task(task: Task, db: Session = Depends(get_db)):
    task_model = models.TaskDB()
    task_model.name = task.name
    task_model.description = task.description
    task_model.status = task.status
    task_model.created_at = task.created_at
    task_model.updated_at = task.updated_at

    db.add(task_model)
    db.commit()

    return task


@app.put("/api/task/{task_id}", tags=["PUT Methods"])
def update_task(task_id: int, task: Task, db: Session = Depends(get_db)):
    task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {task_id} : Does not exist"
        )

    task_model.name = task.name
    task_model.description = task.description
    task_model.status = task.status
    task_model.created_at = task.created_at
    task_model.updated_at = task.updated_at

    db.add(task_model)
    db.commit()

    return task


@app.delete("/api/task/{task_id}", tags=["DELETE Methods"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {task_id} : Does not exist"
        )

    db.query(models.TaskDB).filter(models.TaskDB.id == task_id).delete()

    db.commit()


# @app.patch("/update")
# async def update_profile(task_id: int, task: Task, db: Session = Depends(get_db)):
#     task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
#
#     task_model.update(task.dict(exclude_unset=True))

# for key, value in TaskDB.items():
#     print("key ----", key)
#     print("value ----", value)
#
#     setattr(task, key, value)

# db.commit()
# return task_model

# Manager URL
@app.get('/api/all-managers/', tags=["GET Methods"])
async def get_all_managers(db: Session = Depends(get_db)):
    return db.query(models.ManagerDB).all()


@app.get('/api/manager/{manager_id}', tags=["GET Methods"])
async def get_manager(manager_id: int, db: Session = Depends(get_db)):
    return db.query(models.ManagerDB).filter(models.ManagerDB.id == manager_id).first()


@app.post("/api/create-manager", tags=["POST Methods"])
def create_manager(manager: Manager, db: Session = Depends(get_db)):

    manager_model = models.ManagerDB()
    manager_model.username = manager.username
    manager_model.first_name = manager.first_name
    manager_model.last_name = manager.last_name
    # manager_model.email = manager.email
    manager_model.password = manager.password
    manager_model.created_at = manager.created_at
    manager_model.updated_at = manager.updated_at

    db.add(manager_model)
    db.commit()

    return manager


@app.put("/api/manager/{manager_id}", tags=["PUT Methods"])
def update_book(manager_id: int, manager: Manager, db: Session = Depends(get_db)):
    manager_model = db.query(models.ManagerDB).filter(models.ManagerDB.id == manager_id).first()

    if manager_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {manager_id} : Does not exist"
        )
    # create_book()
    manager_model.username = manager.username
    manager_model.first_name = manager.first_name
    manager_model.last_name = manager.last_name
    # manager_model.email = manager.email
    manager_model.password = manager.password
    manager_model.created_at = manager.created_at
    manager_model.updated_at = manager.updated_at

    db.add(manager_model)
    db.commit()

    return manager


@app.delete("/api/manager/{manager_id}", tags=["DELETE Methods"])
def delete_manager(manager_id: int, db: Session = Depends(get_db)):
    manager_model = db.query(models.ManagerDB).filter(models.ManagerDB.id == manager_id).first()

    if manager_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {manager_id} : Does not exist"
        )

    db.query(models.ManagerDB).filter(models.ManagerDB.id == manager_id).delete()

    db.commit()
