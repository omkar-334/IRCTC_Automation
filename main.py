import time

from selenium import webdriver


class Booking:
    def __init__(self, values):
        """
        It will hold the main class for executing Chrome Browser
        :param values:
        """
        self.browser = None
        self.values = values

    def main(self):
        """
        It will be having main script for Chrome automation
        """
        try:
            self.browser = webdriver.Chrome()
            self.browser.get("https://www.irctc.co.in/nget/train-search")
            login_page = self.browser.find_element("id", "loginFormId")
            login_page.find_element("id", "usernameId").send_keys(self.values["UserID"])
            login_page.find_element("name", "j_password").send_keys(self.values["Password"])
            time.sleep(10)
            login_page.find_element("id", "loginbutton").click()
            main_page = self.browser.find_element("class name", "container")
            main_page.find_element("id", "quickbookTab:header:inactive").click()
            main_page.find_element("id", "qbform:trainNUmber").send_keys(self.values["TrainNo"])
            main_page.find_element("id", "qbform:fromStation").send_keys(self.values["FromStation"])
            main_page.find_element("id", "qbform:toStation").send_keys(self.values["ToStation"])
            main_page.find_element("id", "qbform:qbJrnyDateInputDate").send_keys(self.values["Date"])
            main_page.find_element("id", "qbform:class").send_keys(self.values["Class"])
            main_page.find_element("id", "qbform:quota").send_keys(self.values["Quota"])
            main_page.find_element("id", "qbform:quickBookSubmit").click()
            for index in range(3):
                self.browser.find_element("id", f"addPassengerForm:psdetail:{index}:j_idt567").find_element(
                    "tag name", "input"
                ).send_keys(self.values[f"Name{index}"])
                self.browser.find_element("id", f"addPassengerForm:psdetail:{index}:psgnAge").send_keys(
                    self.values[f"Age{index}"]
                )
                self.browser.find_element("id", f"addPassengerForm:psdetail:{index}:psgnGender").send_keys(
                    self.values[f"Gender{index}"]
                )
                self.browser.find_element("id", "addPassengerForm:mobileNo").send_keys(self.values["MobileNo"])
            self.browser.find_element("id", "nlpAnswer").send_keys("")
            time.sleep(10)
            self.browser.find_element("id", "COD").click()
            self.browser.find_elements("css selector", "input[type='radio'][value='100']")[0].click()
            self.browser.find_element("id", "validate").click()
            exit(0)
        except BaseException as error:
            raise error
