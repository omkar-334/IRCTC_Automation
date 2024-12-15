import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from driver import create_driver

xpath = {
    # Signin
    "login": "//button[text()='LOGIN']",
    "user_id": "//input[@placeholder='User Name']",
    "password": "//input[@placeholder='Password']",
    "signin": "//button[@type='submit' and text()='SIGN IN']",
    #
    # Enter Form
    "from": "//p-autocomplete[@aria-label='Enter From station. Input is Mandatory.']//input",
    "to": "//p-autocomplete[@aria-label='Enter To station. Input is Mandatory.']//input",
    "date": "//p-calendar[@aria-label='Enter Journey Date. Formate D.D./.M.M./.Y.Y.Y.Y. Input is Mandatory.']//input",
    "class": "//p-dropdown[@id='journeyClass' and @formcontrolname='journeyClass']",
    "quota": "//p-dropdown[@id='journeyQuota' and @formcontrolname='journeyQuota']",
    "option": "{}//li[@role='option' and normalize-space(@aria-label)='{}']",
    #
    # Select Ticket
    "modify_search": "//button[@type='submit' and contains(., 'Modify Search')]",
    "refresh": "//strong[normalize-space(.) = '{}']/ancestor::div/following-sibling::div//span[contains(@class, 'fa-repeat')]",
    "select_date": "//strong[normalize-space(.) = '{}']",
    "book": "//button[@type='button' and normalize-space(.)='Book Now']",


class Booking:
    def __init__(self, values):
        self.values = values

    def click(self, xpath):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def send_keys(self, xpath, keys, nextkeys=None):
        field = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        field.clear()
        field.send_keys(keys)
        if nextkeys:
            field.send_keys(nextkeys)

    def signin(self):
        self.send_keys(xpath["user_id"], self.values["UserID"])
        self.send_keys(xpath["password"], self.values["Password"])
        time.sleep(10)

        self.click(xpath["signin"])
        print(f"Signed in as {values['UserID']}")

    def set_date_via_calendar(self, xpath, raw_date):
        date_obj = datetime.strptime(raw_date, "%Y-%m-%d")
        day = date_obj.day
        month = date_obj.strftime("%B")
        year = date_obj.year

        self.click(xpath)

        while True:
            current_month_year = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-title").text
            if f"{month}{year}" in current_month_year:
                break
            else:
                self.driver.find_element(By.CLASS_NAME, "ui-datepicker-next").click()

        day_xpath = f"//a[text()='{day}']"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, day_xpath))).click()

    def enter_form(self):
        self.send_keys(xpath["from"], self.values["FromStation"])
        self.send_keys(xpath["to"], self.values["ToStation"])

        self.set_date_via_calendar(xpath["date"], self.values["Date"])

        self.click(xpath["class"])
        self.click(xpath["option"].format(xpath["class"], self.values["Class"]))
        self.click(xpath["quota"])
        self.click(xpath["option"].format(xpath["quota"], self.values["Quota"]))
        self.click("//button[@type='submit' and text()='Search']")

        print("Form Submitted.")

    def select_ticket(self):
        self.click(xpath["modify_search"])

        self.click(xpath["refresh"].format(self.values["Class"]))

        date = datetime.strptime(self.values["Date"], "%Y-%m-%d").strftime("%a, %d %b")
        self.click(xpath["select_date"].format(date))

        self.click(xpath["book"])
        print("Ticker Selected")

    def main(self):
        try:
            self.driver = create_driver(headless=False)
            self.wait = WebDriverWait(self.driver, 10)

            self.driver.get("https://www.irctc.co.in/nget/train-search")

            self.enter_form()

            self.select_ticket()

            self.signin()

            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            self.driver.quit()


if __name__ == "__main__":
    values = {
        "UserID": "omkar334k",
        "Password": "password123",
        "FromStation": "KACHEGUDA - KCG (SECUNDERABAD)",
        "ToStation": "MYSURU JN - MYS (MYSURU)",
        "Date": "2025-01-31",
        "Class": "Sleeper (SL)",
        "Quota": "GENERAL",
        "MobileNo": "1234567890",
        "Passengers": [{"Name": "Omkar Kabde", "Age": "18", "Gender": "Male"}],
    }

    booking = Booking(values)
    booking.main()
