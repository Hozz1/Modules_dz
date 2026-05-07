from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from schemas.tasks import TaskCreate, TaskOut
from repositories.tasks import (
    create_task,
    get_task_by_id,
    delete_task_by_id,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    return await create_task(session, task)

@router.get("/{task_id}", response_model=TaskOut)
async def get(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
async def delete(task_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await delete_task_by_id(session, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"status": "deleted"}
