from fastapi import FastAPI

from src.services.amazon import Amazon
from src.services.atlassian import Atlassian
from src.services.oracle import Oracle

app: FastAPI = FastAPI()


@app.get("/health/jira")
def ws_atl() -> dict[str, bool]:
    response: dict[str, bool] = Atlassian.services()
    return response


@app.get("/health/aws")
def ws_aws() -> dict[str, bool]:
    response = Amazon.services()
    return response


@app.get("/health/oracle")
def ws_oci() -> dict[str, bool]:
    response: dict[str, bool] = Oracle.services()
    return response
