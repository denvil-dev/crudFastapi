from fastapi import FastAPI
from routes import userRoute, loginRoute


app = FastAPI()

app.include_router(userRoute.userRouter)
app.include_router(loginRoute.loginRouter)
@app.get("/")
async def read_root():
    return {"Hello": "World"}

