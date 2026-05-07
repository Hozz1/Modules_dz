from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.tasks import Task
from schemas.tasks import TaskCreate

async def create_task(session: AsyncSession, task_data: TaskCreate) -> Task:
    task = Task(**task_data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_task_by_id(session: AsyncSession, task_id: int) -> Task | None:
    result = await session.execute(
        select(Task).where(Task.id == task_id)
    )
    return result.scalar_one_or_none()

async def delete_task_by_id(session: AsyncSession, task_id: int) -> bool:
    task = await get_task_by_id(session, task_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True
