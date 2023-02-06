import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from propelauth_fastapi import init_auth
from propelauth_py.user import User

load_dotenv()

app = FastAPI()
auth = init_auth(os.getenv("PROPELAUTH_AUTH_URL"), os.getenv("PROPELAUTH_API_KEY"))

@app.get("/whoami")
def who_am_i(user: User = Depends(auth.require_user)):
    return {"user_id": user.user_id, "org_id": user.org_id_to_org_member_info}

@app.get("/org/{org_id}")
async def view_org(org_id: str, current_user: User = Depends(auth.require_user)):
    org = auth.require_org_member(current_user, org_id)
    return {"org": org}