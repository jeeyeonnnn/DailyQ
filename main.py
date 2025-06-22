from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.account.endpoint import router as account_router 
from app.region.endpoint import router as region_router
from app.user.endpoint import router as user_router
from app.ranking.endpoint import router as ranking_router
from app.chat.endpoint import router as chat_router

def set_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=['access-token', 'refresh-token']
    )

def start_application():
    app = FastAPI(title="DailyQ API", version="1.0.0")

    @app.get('/', tags=['☑️ Healthy Check'])
    def ecs_heathly_check():
        return 'success'

    set_cors(app)
    app.include_router(region_router)
    app.include_router(account_router)
    app.include_router(user_router)
    app.include_router(ranking_router)
    app.include_router(chat_router)
    return app

app = start_application()
