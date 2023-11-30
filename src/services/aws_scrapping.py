from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox as Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import time

START_TIME: float
END_TIME: float


class AWS():
    opt: Options = Options()
    opt.add_argument("--headless")
    
    @staticmethod
    def filter_submit(
        obj: WebElement,
        text: str
    ) -> None:
        if obj.is_selected:
            obj.send_keys(text)
            obj.send_keys(Keys.ENTER)   
        
    @classmethod
    def services(cls) -> dict[str, bool]:
        driver: Browser = Browser(options=cls.opt)
        driver.get("https://health.aws.amazon.com/health/status")
        
        time.sleep(1)
    
        filter: WebElement = driver.find_elements(
            by=By.CLASS_NAME,
            value="awsui_input_2rhyz_7lwtk_97",
        )[0]
    
        cls.filter_submit(
            filter,
            text="Region = N. Virginia",
        )
        
        cls.filter_submit(
            filter,
            text="Region = Sao Paulo",
        )
    
        status_table: WebElement = driver.find_elements(
            by=By.CSS_SELECTOR,
            value=".awsui_table_wih1l_1l1xk_144 > tbody"
        )[0]
    
        rows: list[WebElement] = status_table.find_elements(
            by=By.TAG_NAME,
            value="tr",
        )
    
        services: dict[str, bool] = {}
    
        for row in rows:
            service: str = row.find_elements(
                by=By.CSS_SELECTOR,
                value=".status-history-name > span"
            )[0].text
    
            status: str = row.find_elements(
                by=By.CLASS_NAME,
                value="awsui_icon_1cbgc_socsa_97"
            )[0].get_attribute("aria-label").lower()
    
            services[service] = status == "resolved"
        
        driver.quit()

        return services
