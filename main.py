from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.product_route import router

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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