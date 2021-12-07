from fastapi import FastAPI
import uvicorn

import odoo
from api import partners


app = FastAPI(title="FastAPI-Odoo15 App",
              description="Make Odoo APIs")

app.include_router(partners.router)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
