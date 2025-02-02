from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.base import get_db
from app.models.user import User
from app.models.code_file import CodeFile
from app.models.editing_session import EditingSession, UserRole
from app.schemas.code_file import (
    CodeFileCreate,
    CodeFileUpdate,
    CodeFile as CodeFileSchema,
    CollaboratorInfo
)
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=CodeFileSchema)
async def create_file(
    file: CodeFileCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    db_file = CodeFile(
        **file.model_dump(),
        owner_id=current_user.id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    # Create owner editing session
    session = EditingSession(
        code_file_id=db_file.id,
        user_id=current_user.id,
        role=UserRole.OWNER
    )
    db.add(session)
    db.commit()
    
    return db_file

@router.get("/", response_model=List[CodeFileSchema])
async def list_files(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    # Get files where user is owner or collaborator
    files = db.query(CodeFile).join(
        EditingSession,
        CodeFile.id == EditingSession.code_file_id
    ).filter(
        or_(
            CodeFile.owner_id == current_user.id,
            EditingSession.user_id == current_user.id
        )
    ).offset(skip).limit(limit).all()
    
    # Enhance files with collaborator information
    for file in files:
        sessions = db.query(EditingSession).filter(
            EditingSession.code_file_id == file.id
        ).all()
        file.collaborators = [
            CollaboratorInfo(user=session.user, role=session.role.value)
            for session in sessions
            if session.user_id != file.owner_id
        ]
    
    return files

@router.get("/{file_id}", response_model=CodeFileSchema)
async def get_file(
    file_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    file = db.query(CodeFile).filter(CodeFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check access
    session = db.query(EditingSession).filter(
        EditingSession.code_file_id == file_id,
        EditingSession.user_id == current_user.id
    ).first()
    
    if not session and file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Add collaborator information
    sessions = db.query(EditingSession).filter(
        EditingSession.code_file_id == file.id
    ).all()
    file.collaborators = [
        CollaboratorInfo(user=session.user, role=session.role.value)
        for session in sessions
        if session.user_id != file.owner_id
    ]
    
    return file

@router.put("/{file_id}", response_model=CodeFileSchema)
async def update_file(
    file_id: int,
    file_update: CodeFileUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    db_file = db.query(CodeFile).filter(CodeFile.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if user has access
    session = db.query(EditingSession).filter(
        EditingSession.code_file_id == file_id,
        EditingSession.user_id == current_user.id
    ).first()
    
    if not session and db_file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Update file attributes
    update_data = file_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_file, field, value)
    
    db.commit()
    db.refresh(db_file)
    
    return db_file

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    db_file = db.query(CodeFile).filter(
        CodeFile.id == file_id,
        CodeFile.owner_id == current_user.id  # Only owner can delete
    ).first()
    
    if not db_file:
        raise HTTPException(
            status_code=404,
            detail="File not found or you're not the owner"
        )
    
    # Delete all associated editing sessions
    db.query(EditingSession).filter(
        EditingSession.code_file_id == file_id
    ).delete()
    
    # Delete the file
    db.delete(db_file)
    db.commit()
    
    return {"message": "File deleted successfully"} 