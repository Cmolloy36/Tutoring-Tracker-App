from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud_tutoringsessions, schemas
from ..database import *


router = APIRouter()

@router.get("/tutoring_sessions/{tutoring_session_id}", response_model=schemas.TutoringSession)
def get_tutoring_session(tutoring_session_id: int, session: Session = Depends(get_session)):
    tutoring_session = crud_tutoringsessions.get_tutoring_session(session=session, tutoring_session_id=tutoring_session_id)
    if tutoring_session is None:
        raise HTTPException(status_code=404, detail=f"a tutoring_session with this id does not exist")
    return tutoring_session

@router.get("/tutoring_sessions", response_model=list[schemas.TutoringSession])
def get_tutoring_sessions(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    tutoring_sessions = crud_tutoringsessions.get_tutoring_sessions(session=session, skip=skip, limit=limit)
    if tutoring_sessions is None:
        raise HTTPException(status_code=204, detail=f"no tutoring sessions exist!")
    return tutoring_sessions

@router.post("/tutoring_sessions",response_model=schemas.TutoringSession)
def post_tutoring_session(tutoring_session: schemas.TutoringSessionCreate, session: Session = Depends(get_session)):
    tutoring_session, err = crud_tutoringsessions.post_tutoring_session(session=session, tutoring_session=tutoring_session)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"unable to add tutoring_session: {err}")
    return tutoring_session

@router.get("/tutoring_sessions/{tutoring_session_id}", response_model=schemas.TutoringSession)
def get_tutoring_session(tutoring_session_id: int, session: Session = Depends(get_session)):
    tutoring_session = crud_tutoringsessions.get_tutoring_session(session=session, tutoring_session_id=tutoring_session_id)
    if tutoring_session is None:
        raise HTTPException(status_code=404, detail=f"a tutoring_session with this id does not exist")
    return tutoring_session

@router.get("/tutoring_sessions", response_model=list[schemas.TutoringSession])
def get_tutoring_sessions(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    tutoring_sessions = crud_tutoringsessions.get_tutoring_sessions(session=session, skip=skip, limit=limit)
    # if tutoring_sessions is []:
    #     ...
    return tutoring_sessions

@router.put("/tutoring_sessions/{tutoring_session_id}", response_model=schemas.TutoringSession)
def update_tutoring_session(tutoring_session_id: int, tutoring_session_data: schemas.TutoringSessionUpdate, session: Session = Depends(get_session)):
    tutoring_session, err = crud_tutoringsessions.update_tutoring_session(session=session, tutoring_session_id=tutoring_session_id, tutoring_session_data=tutoring_session_data)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"error: {err}")
    return tutoring_session

@router.delete("/tutoring_sessions/{tutoring_session_id}", response_model=str)
def delete_tutoring_session(tutoring_session_id: int, session: Session = Depends(get_session)):
    tutoring_session_name, tutoring_session_id, err = crud_tutoringsessions.delete_tutoring_session(session=session, tutoring_session_id=tutoring_session_id)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"error: {err}")
    return f"{tutoring_session_name} (tutoring_session_id: {tutoring_session_id}) has been deleted"