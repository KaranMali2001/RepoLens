from datetime import datetime
from app.models.users import Users
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.models.users import Users
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user_data: dict):
    print("inside create_user", user_data)
    try:

        userCount = await get_user(db, user_data["clerk_id"])
        print("userCount", userCount)
        if userCount is not None:
            print("user exists")
            return False

        user = Users(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        print("response", user)

        return True
    except Exception as e:
        await db.rollback()
        print("Error creating new user:", e)

        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


async def get_user(db: AsyncSession, clerk_id: str):
    try:
        result = await db.execute(select(Users).where(Users.clerk_id == clerk_id))
        print("result from get_userrrr", result)
        user = result.scalar_one_or_none()
        
        return user
    except Exception as e:
        print("Error getting user:", e)
        return None
