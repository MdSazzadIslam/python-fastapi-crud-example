from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


from src.routes.product_route import router

limiter = Limiter(key_func=get_remote_address, default_limits=["10/5seconds"])

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SlowAPIMiddleware)

app.include_router(router=router, prefix="/products")


def main():
    # Your main program logic here
    ...

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Perform cleanup or shutdown tasks
        print("KeyboardInterrupt: Exiting the program gracefully...")