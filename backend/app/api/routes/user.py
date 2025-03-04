from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.services.clerk_services import ClerkTokenVerifier
from app.helpers.index_repo import index_repo

from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import datetime
from app.config.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from functools import lru_cache
from app.services.project_services import (
    insert_project,
    get_projects_db,
    delete_project_db,
)

verifier = ClerkTokenVerifier()
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create-project")
async def create_project(
    request: Request,
    db: AsyncSession = Depends(get_session),
    token_data: dict = Depends(verifier.verify_token),
):
    body = await request.json()
    print("inside create project..................", body)
    clerk_id = token_data["sub"]
    gitbook_url: str = body.get("gitbook_url")
    try:

        res: int = await insert_project(db, body, clerk_id)
    
        if res is True:
            BackgroundTasks.add_task(index_repo, res, gitbook_url, db)
            return JSONResponse(
                status_code=200, content={"message": "Project created successfully"}
            )
    except Exception as e:
        print("Error creating project:", e)
        return JSONResponse(
            status_code=500, content={"message": "Error creating project"}
        )


@lru_cache(maxsize=20)
@router.get("/get-projects")
async def get_projects(
    req: Request,
    db: AsyncSession = Depends(get_session),
    token_data: dict = Depends(verifier.verify_token),
):

    print("inside Get Projects")
    clerk_id = token_data["sub"]
    try:
        print("inside get projects try chatch", clerk_id)
        res = await get_projects_db(db, clerk_id)
        if res is not None:
            return JSONResponse(status_code=200, content=res)
    except Exception as e:
        print("Error fetching projects:", e)
        return JSONResponse(
            status_code=500, content={"message": "Error fetching projects"}
        )


@router.delete("/delete-project")
async def delete_project(
    req: Request,
    db: AsyncSession = Depends(get_session),
    token_data: dict = Depends(verifier.verify_token),
):
    body = await req.json()
    print("inside delete project", body)
    clerk_id = token_data["sub"]
    try:
        res = await delete_project_db(db, body["project_id"], clerk_id)
        if res:
            return JSONResponse(
                status_code=200, content={"message": "Project deleted successfully"}
            )
    except Exception as e:
        print("Error deleting project:", e)
        return JSONResponse(
            status_code=500, content={"message": "Error deleting project"}
        )
