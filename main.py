import logging
from dotenv import load_dotenv

load_dotenv()

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Third-party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Local application imports
from src.utils.cache import create_redis_connection, close_redis_connection
from src.routes.product_route import router

load_dotenv()

# Rate limiter configuration
limiter = Limiter(key_func=get_remote_address, default_limits=["10/5seconds"])

# FastAPI application instance
app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SlowAPI middleware for rate limiting
app.add_middleware(SlowAPIMiddleware)

# Include API routes
app.include_router(router=router, prefix="/products")


@app.on_event("startup")
async def startup_event():
    logger.info("Opening Redis...")
    app.state.redis = await create_redis_connection()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Opening Redis...")
    await close_redis_connection(app.state.redis)


def main():
    # Your main program logic here
    ...


if __name__ == "__main__":
    main()
