from typing import Annotated
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user import User
from app.models.code_file import CodeFile
from app.models.editing_session import EditingSession, UserRole
from app.api.auth import get_current_user
from app.services.collaboration_service import manager

router = APIRouter()

async def get_file_access(
    file_id: int,
    current_user: User,
    db: Session
) -> CodeFile:
    file = db.query(CodeFile).filter(CodeFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if user has access
    session = db.query(EditingSession).filter(
        EditingSession.code_file_id == file_id,
        EditingSession.user_id == current_user.id
    ).first()
    
    if not session and file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return file

@router.websocket("/ws/{file_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    file_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    # Authenticate user
    try:
        current_user = await get_current_user(db, token)
    except HTTPException:
        await websocket.close(code=1008)  # Policy Violation
        return
    
    # Verify file access
    try:
        file = await get_file_access(file_id, current_user, db)
    except HTTPException:
        await websocket.close(code=1008)
        return
    
    await manager.connect(websocket, file_id, current_user.id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "cursor_update":
                await manager.update_cursor(
                    file_id,
                    current_user.id,
                    data["position"]
                )
            
            elif data["type"] == "code_update":
                # Update file content in database
                file.content = data["content"]
                db.commit()
                
                # Broadcast to other users
                await manager.broadcast_code_update(
                    file_id,
                    data["content"],
                    current_user.id
                )
                
    except WebSocketDisconnect:
        await manager.disconnect(file_id, current_user.id)

@router.post("/files/{file_id}/invite")
async def invite_collaborator(
    file_id: int,
    collaborator_email: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    # Check if user owns the file
    file = db.query(CodeFile).filter(
        CodeFile.id == file_id,
        CodeFile.owner_id == current_user.id
    ).first()
    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found or you're not the owner"
        )
    
    # Find collaborator
    collaborator = db.query(User).filter(User.email == collaborator_email).first()
    if not collaborator:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already a collaborator
    existing_session = db.query(EditingSession).filter(
        EditingSession.code_file_id == file_id,
        EditingSession.user_id == collaborator.id
    ).first()
    
    if existing_session:
        raise HTTPException(
            status_code=400,
            detail="User is already a collaborator"
        )
    
    # Create new editing session
    session = EditingSession(
        code_file_id=file_id,
        user_id=collaborator.id,
        role=UserRole.COLLABORATOR
    )
    db.add(session)
    db.commit()
    
    return {"message": "Collaborator added successfully"} 