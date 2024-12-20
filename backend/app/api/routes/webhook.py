from datetime import datetime
from fastapi import FastAPI, Request, HTTPException, Header, APIRouter, Depends
import os
from svix.webhooks import Webhook
from app.services.user_services import create_user
from app.config.database import get_session
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/webhook",
    tags=["webhooks"],
)


@router.post("/user")
async def handle_clerk_webhook(
    request: Request,
    svix_id: str = Header(None, alias="svix-id"),
    svix_timestamp: str = Header(None, alias="svix-timestamp"),
    svix_signature: str = Header(None, alias="svix-signature"),
    db: AsyncSession = Depends(get_session),
):
    if not (svix_id and svix_timestamp and svix_signature):
        raise HTTPException(status_code=400, detail="Missing Svix headers")

    payload = await request.body()

    try:
        CLERK_SIGNING_SECRET = os.environ.get("CLERK_SIGNING_SECRET")

        wh = Webhook(CLERK_SIGNING_SECRET)

        evt = wh.verify(
            payload,
            {
                "svix-id": svix_id,
                "svix-timestamp": svix_timestamp,
                "svix-signature": svix_signature,
            },
        )
    except Exception as err:
        print(f"Webhook verification error: {err}")
        raise HTTPException(status_code=400, detail="Webhook verification failed")

    # Extract webhook data
    webhook_data = evt.get("data", {})
    event_type = evt.get("type")

    print(webhook_data)
    if event_type == "user.created":
        try:
            user_data = {
                "clerk_id": webhook_data.get("id"),
                "email": webhook_data.get("email_addresses", [{}])[0].get(
                    "email_address"
                ),
                "full_name": f"{webhook_data.get('first_name', '')} {webhook_data.get('last_name', '')}".strip(),
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "is_active": True,
            }
            print("user_data \n", user_data)
            res = await create_user(db, user_data)
            print("res \n", res)

            if res:
                return {
                    "status": "Webhook received",
                    "message": "User processed successfully",
                }
            else:
                return {
                    "status": "failure",
                    "message": "User already exists",
                }
        except Exception as error:
            print(f"Error in processing user data: {error}")
            raise HTTPException(
                status_code=500,
                detail="Failed to process webhook",
            )
