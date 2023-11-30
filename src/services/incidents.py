from selenium.webdriver import Firefox as Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement

from src.interfaces.service import Service


class Incidents(Service):
    driver: Browser = Browser()
  driver.get("https://jira-software.status.atlassian.com/history")
  
  data: list[WebElement] = driver.find_elements(
      by=By.CLASS_NAME,
      value="month",
  )
  
  incidents = {}
  
  for each in data:
    month: str = each.find_elements(
      by=By.CLASS_NAME,
      value="month-title"
    )[0].text
        
    incident_data: list[WebElement] = each.find_elements(
      by=By.CLASS_NAME,
      value="incident-data"
    )
    
    dict_incidents = {}
    for incidents_data in incident_data:
      title:str = incidents_data.find_elements(
        by=By.CLASS_NAME,
        value="incident-title"
      )[0].text
      dict_incidents["title"] = title
      
      desc:str = incidents_data.find_elements(
        by=By.CLASS_NAME,
        value="incident-body"
      )[0].text
      dict_incidents["desc"] = desc
      
      date:str = incidents_data.find_elements(
        by=By.CSS_SELECTOR,
        value=".incident-body + .secondary.font-small.color-secondary"
      )[0].text
      
      dict_incidents["date"] = date
      
    incidents[month] = dict_incidents
    
  return incidents
