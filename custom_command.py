""" This file aims to demonstrate how to write custom commands in OpenWPM

Steps to have a custom command run as part of a CommandSequence

1. Create a class that derives from BaseCommand
2. Implement the execute method
3. Append it to the CommandSequence
4. Execute the CommandSequence

"""
import csv
import logging

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

from openwpm.commands.types import BaseCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.socket_interface import ClientSocket

class FormCountingCommand(BaseCommand):
    def __init__(self) -> None:
        self.logger = logging.getLogger("openwpm")

    # While this is not strictly necessary, we use the repr of a command for logging
    # So not having a proper repr will make your logs a lot less useful
    def __repr__(self) -> str:
        return "LinkCountingCommand"

    # Have a look at openwpm.commands.types.BaseCommand.execute to see
    # an explanation of each parameter
    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
        forms = webdriver.find_elements_by_tag_name("form")
        with open('forms.csv', 'a', newline='') as csvfile:
            for form in forms:
                spamwriter = csv.writer(csvfile, delimiter=',')
                form_text = form.text.replace('\n',' ')
                if form_text == '':
                    form_text = "NONE"
                
                form_id = form.get_attribute("id")
                if form_id == '':
                    form_id = "NONE"
                
                spamwriter.writerow([form_text, form_id, webdriver.current_url])
                print("form text: ", form_text, " ; form id: ", form_id, " url: " + webdriver.current_url)
            
        # current_url = webdriver.current_url
        # link_count = len(webdriver.find_elements(By.TAG_NAME, "a"))
        # self.logger.info("There are %d links on %s", link_count, current_url)

class LinkCountingCommand(BaseCommand):
    """This command logs how many links it found on any given page"""

    def __init__(self) -> None:
        self.logger = logging.getLogger("openwpm")

    # While this is not strictly necessary, we use the repr of a command for logging
    # So not having a proper repr will make your logs a lot less useful
    def __repr__(self) -> str:
        return "LinkCountingCommand"

    # Have a look at openwpm.commands.types.BaseCommand.execute to see
    # an explanation of each parameter
    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
        current_url = webdriver.current_url
        link_count = len(webdriver.find_elements(By.TAG_NAME, "a"))
        self.logger.info("There are %d links on %s", link_count, current_url)
        print(webdriver.find_element(By.TAG_NAME, "a"))
        print(webdriver.find_element(By.TAG_NAME, "a").text)
        print(webdriver.find_element(By.TAG_NAME, "a").size)
