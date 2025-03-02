from datetime import datetime
from app.models.projects import Projects
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.helpers.url_exist import github_url_exists
from app.services.user_services import get_user
from functools import lru_cache


async def insert_project(db: AsyncSession, project_data: dict, clerk_id: str):
    try:
        print("project data inside",project_data)
        project_data["credits_required"] = 0
        project_data["status"] = "active"
        print("before validation\n", project_data)
        gitbook_url = project_data.get("gitbook_url")

        data = Projects(**project_data)

        user = await get_user(db, clerk_id)
        print("/n user", user)
        await db.refresh(user, attribute_names=["projects"])
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        res = user.projects.append(data)
        await db.commit()
        await db.refresh(user)

        return data.id
    except Exception as e:
        await db.rollback()
        print("Error creating new project:", e)

        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")


async def get_projects_db(db: AsyncSession, clerk_id: str):
    try:
        result = await db.execute(select(Projects).where(Projects.clerk_id == clerk_id))
        projects = result.scalars().all()
        projects_list = [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "github_url": project.github_url,
            }
            for project in projects
        ]
        print("result from get projectttt", projects_list)
        return projects_list
    except Exception as e:
        print("Error getting projects:", e)
        return None


async def delete_project_db(db: AsyncSession, project_id: int, clerk_id: str):

    result = await db.execute(
        select(Projects).where(Projects.id == project_id, Projects.clerk_id == clerk_id)
    )
    project = result.scalars().one_or_none()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    await db.delete(project)
    await db.commit()
    return True
