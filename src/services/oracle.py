from selenium.webdriver import Firefox as Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement

from src.interfaces.service import Service


class Oracle(Service):
    URL: str = "https://ocistatus.oraclecloud.com/#/"

    opt: Options = Options()
    opt.add_argument("--headless")

    @staticmethod
    def get_status_table_rows(
        driver: Browser,
    ) -> list[WebElement]:
        driver.find_element(
            by=By.ID,
            value="LAD",
        ).click()

        status_table: WebElement = driver.find_element(
            by=By.TAG_NAME,
            value="table",
        )

        return status_table.find_elements(
            by=By.TAG_NAME,
            value="tr",
        )

    @classmethod
    def services(cls) -> dict[str, bool]:
        driver: Browser = Browser(options=cls.opt)
        driver.get(cls.URL)

        services: dict[str, bool] = {}

        for row in cls.get_status_table_rows(
            driver=driver,
        ):
            service: str = row.find_element(
                by=By.TAG_NAME,
                value="th",
            ).text.strip()

            status: list[WebElement] = row.find_elements(
                by=By.TAG_NAME,
                value="td",
            )

            if len(status) == 5:
                status_source = (
                    status[1]
                    .find_element(
                        by=By.TAG_NAME,
                        value="img",
                    )
                    .get_attribute("title")
                    .lower()
                )

                services[service] = False if status_source != "operational" else True

        driver.quit()

        return services
