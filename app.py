from fastapi import FastAPI, Request, HTTPException, status, BackgroundTasks, Depends, File, UploadFile, Form, requests


import json as json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, IPvAnyNetwork, IPvAnyAddress,UUID4
from typing import Optional, List, Dict, Annotated
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from Classifier import ApplyAI
from models import *
from database import SessionLocal, engine
from modelclasses import *
import os

from IPLOCATOR import get_IP_location

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def log_ip(IP, db: Session = Depends(get_db)):
    ip_as_string = str(IP)
    ip_log_entry = IP_logger(ipaddress=ip_as_string, requested_at=datetime.now())
    db.add(ip_log_entry)
    db.commit()
    db.refresh(ip_log_entry)
    return

# Endpoint for new userEntry
@app.post("/new_user", response_model=Saved_User)
async def new_USER(entry: UserEntry, request: Request,backgroundtasks : BackgroundTasks, db: Session = Depends(get_db), save: bool = True):
    IP = IPvAnyAddress(request.client.host)

    backgroundtasks.add_task(log_ip, IP, db)

    IP_origin = get_IP_location(IP)

    folderList = entry.folders.dict()
    tagList = entry.tags.dict()

    try:
        new_UserRecord = UserRecord(folders=folderList, tags=tagList, origin=IP_origin)
        if save:
            db.add(new_UserRecord)
            db.commit()
            db.refresh(new_UserRecord)

        return Saved_User(
            id=new_UserRecord.id,
            created_at=new_UserRecord.created_at,
            last_login=new_UserRecord.last_login,
            updated_at=new_UserRecord.updated_at,
            last_IP_origin=new_UserRecord.last_IP_origin,
            folders=new_UserRecord.folders,
            tags=new_UserRecord.tags
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")

        # soft test endpoint
        return new_UserRecord
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@app.get("/{uuid}/info", response_model=Saved_User)
async def get_user_record(uuid: UUID4, background_tasks: BackgroundTasks,request :Request, db: Session = Depends(get_db)):
    """
    Get a USER DATA by UUID.
    """
    IP = IPvAnyAddress(request.client.host)
    background_tasks.add_task(log_ip, IP, db)
    IP_origin = get_IP_location(IP)

    try:
        user = db.query(UserRecord).filter(UserRecord.id == uuid).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        background_tasks.add_task(update_last_login, user.id, db, IP_origin)
        user_entry = Saved_User(
            id=user.id,
            created_at=user.created_at,
            last_login=datetime.now(),
            updated_at=user.updated_at,
            last_IP_origin=user.last_IP_origin,
            folders=user.folders,
            tags=user.tags
        )
        return user_entry
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")

@app.put("/{uuid}/update", response_model=Saved_User, status_code=status.HTTP_202_ACCEPTED)
async def update_user_record(uuid: UUID4, entry: UserEntry, request: Request,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Update a USER DATA by UUID.
    """
    IP = IPvAnyAddress(request.client.host)
    background_tasks.add_task(log_ip, IP, db)

    IP_origin = get_IP_location(IP)

    try:
        user = db.query(UserRecord).filter(UserRecord.id == uuid).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")


        user.updated_at = datetime.now()
        user.folders = entry.folders.dict()
        user.tags = entry.tags.dict()
        user.last_login = datetime.now()
        user.last_IP_origin = IP_origin

        db.commit()
        db.refresh(user)

        return user


    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")

def update_last_login(user_id: str, db, origin=None):
    # Perform the actual update of the last login time in the database
    # You can use the same database session or create a new one within this function
    # Update the last login time for the user with the specified user_id
    user = db.query(UserRecord).filter(UserRecord.id == user_id).first()
    user.last_login = datetime.now()
    user.last_IP_origin = origin
    db.commit()
    pass

@app.post("/{uuid}/classify", response_model=None)
async def Classify_Content(uuid: UUID4, CONTENT_STR:str, OPEN_AI_TOKEN: str ,request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    user = db.query(UserRecord).filter(UserRecord.id == uuid).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    IP = IPvAnyAddress(request.client.host)
    IP_origin = get_IP_location(IP)

    background_tasks.add_task(update_last_login, user.id, db, IP_origin)
    raw = ApplyAI(CONTENT_STR,user.folders,user.tags,OPEN_AI_TOKEN)
    try:
        classification = Classification(**raw)
        return classification
    except Exception as e:
        d = {'error': f" {e}" , 'raw': raw}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)

