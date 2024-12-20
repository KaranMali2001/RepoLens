from fastapi import APIRouter, Depends, HTTPException
from app.services.clerk_services import ClerkTokenVerifier


from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import datetime
from app.config.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.project_services import insert_project,get_projects_db

verifier = ClerkTokenVerifier()
router = APIRouter(
    prefix="/users", tags=["users"]
)


@router.post("/create-project")
async def create_project(request: Request, db: AsyncSession = Depends(get_session),token_data:dict=Depends(verifier.verify_token)):
    body = await request.json()
    print("inside create project",body)
    clerk_id = token_data["sub"]
    try:

        res = await insert_project(db, body,clerk_id)
        if res is True:
            return JSONResponse(
                status_code=200, content={"message": "Project created successfully"}
            )
    except Exception as e:
        print("Error creating project:", e)
        return JSONResponse(
            status_code=500, content={"message": "Error creating project"}
        )
@router.get("/get-projects")
async def get_projects( req: Request, db: AsyncSession = Depends(get_session),token_data:dict=Depends(verifier.verify_token)):
    
    print("inside Get Projects")
    clerk_id=token_data['sub']
    try: 
        print("inside get projects try chatch",clerk_id)
        res = await get_projects_db(db,clerk_id)
        if res is not None:
            return JSONResponse(
                status_code=200, content=res
            )                         
    except Exception as e:
        print("Error fetching projects:", e)
        return JSONResponse(
            status_code=500, content={"message": "Error fetching projects"}
        )