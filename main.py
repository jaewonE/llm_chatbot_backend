import uvicorn
from fastapi import FastAPI

from apis import router as main_router
from apis.user import router as user_router
from apis.room import router as room_router
from apis.chat import router as chat_router
from apis.raw import router as raw_router

app = FastAPI()

app.include_router(main_router)
app.include_router(user_router)
app.include_router(room_router)
app.include_router(chat_router)
app.include_router(raw_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7701)
# uvicorn main:app --host 0.0.0.0 --port 7701 --reload
