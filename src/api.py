from fastapi import FastAPI

from src.services.aws_scrapping import AWS
from src.services.atlassian import Atlassian
from src.services.oracle import Oracle
from src.services.incidents import Incidents
API: FastAPI = FastAPI()


@API.get("/health/jira")
def ws_atl() -> dict[str, bool]:
    response: dict[str, bool] = Atlassian.services()
    return response


@API.get("/health/aws")
def ws_aws() -> dict[str, bool]:
    response = AWS.services()
    return response


@API.get("/health/oracle")
def ws_oci() -> dict[str, bool]:
    response: dict[str, bool] = Oracle.services()
    return response

@API.get("/health/incidents")
def ws_incidents() -> dict[str, bool]:
    response = Incidents.services()
    return response
