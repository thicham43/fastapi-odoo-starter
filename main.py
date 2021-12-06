from fastapi import FastAPI
import uvicorn

import odoo
from api import partners


app = FastAPI(title="FastAPI-Odoo15 App",
              description="Make Odoo APIs")

app.include_router(partners.router)


@app.on_event("startup")
def set_default_executor() -> None:
    from concurrent.futures import ThreadPoolExecutor
    import asyncio

    loop = asyncio.get_running_loop()
    # Tune this according to your requirements !
    loop.set_default_executor(ThreadPoolExecutor(max_workers=5))


@app.on_event("startup")
def initialize_odoo() -> None:
    # Read Odoo config from $ODOO_RC.
    odoo.tools.config.parse_config([])


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
