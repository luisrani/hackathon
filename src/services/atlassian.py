from bs4 import BeautifulSoup, ResultSet
from requests import Response, request

from src.interfaces.service import Service


class Atlassian(Service):
    URL: str = "https://jira-software.status.atlassian.com/"

    @classmethod
    def __get_page(cls) -> Response | None:
        response: Response = request(
            method="GET",
            url=cls.URL,
        )

        return response if response.ok else None

    @staticmethod
    def __define_services(
        response: Response,
    ) -> dict[str, bool]:
        soup: BeautifulSoup = BeautifulSoup(
            markup=response.text,
            features="html.parser",
        )

        status_components: ResultSet = soup.find_all(
            name="div",
            class_="component-container border-color",
        )

        services: dict[str, bool] = {}

        for component in status_components:
            service: str = component.find(
                name="span",
                class_="name",
            ).text.strip()

            service_status: str = component.find(
                name="span",
                class_="component-status",
            ).text.strip()

            status: bool = True if "operational" in service_status.lower() else False
            services[service] = status

        return services

    @classmethod
    def services(cls) -> dict[str, bool]:
        response: Response | None = cls.__get_page()

        if response is not None:
            return cls.__define_services(response=response)

        return {}
