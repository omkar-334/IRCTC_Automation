import time
from datetime import datetime

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from driver import create_driver

CAPTCHA_TIME = 10

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
    #
    # Passengers
    "name": "//input[@placeholder='Name']",
    "age": "//input[@placeholder='Age']",
    "gender": "//select[@formcontrolname='passengerGender']",
    "berth": "//select[@formcontrolname='passengerBerthChoice']",
    "add": "//a[contains(normalize-space(.), '+ Add Passenger')]",
    #
    # Payment Details
    "mobile": "//input[@formcontrolname='mobileNumber']",
    "continue": "//button[@type='submit' and normalize-space(.)='Continue']",
}


class Booking:
    def __init__(self, values):
        self.values = values

    def click(self, xpath):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except StaleElementReferenceException:
            time.sleep(3)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def send_keys(self, xpath, keys, nextkeys=None):
        field = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        field.clear()
        field.send_keys(keys)
        if nextkeys:
            field.send_keys(nextkeys)

    def signin(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath["user_id"])))
        except:
            self.driver.find_element(By.CSS_SELECTOR, "a > i.fa-align-justify").click()
            self.click(xpath["login"])

        self.send_keys(xpath["user_id"], self.values["UserID"])
        self.send_keys(xpath["password"], self.values["Password"])

        print("\n### Enter Captcha\n")
        time.sleep(CAPTCHA_TIME)

        self.click(xpath["signin"])
        print(f"Signed in as {self.values['UserID']}")

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

    def add_passengers(self):
        passengers = self.values["Passengers"]

        for index, i in enumerate(passengers, start=1):
            name_xpath = f"({xpath['name']})[{index}]"
            age_xpath = f"({xpath['age']})[{index}]"
            gender_xpath = f"({xpath['gender']})[{index}]"
            berth_xpath = f"({xpath['berth']})[{index}]"

            print(name_xpath)
            self.send_keys(name_xpath, i["Name"])
            self.send_keys(age_xpath, i["Age"])

            gender = i["Gender"][0].upper()
            dropdown = self.driver.find_element(By.XPATH, gender_xpath)
            Select(dropdown).select_by_value(gender)

            berth = i["Berth"].upper().split()
            if len(berth) == 1:
                berth = berth[0][0] + "B"
            else:
                berth = berth[0][0] + berth[1][0]

            if berth != "NP":
                dropdown = self.driver.find_element(By.XPATH, berth_xpath)
                Select(dropdown).select_by_value(berth)

            if i != passengers[-1]:
                self.click(xpath["add"])

        print("Passengers added")

    def start_payment(self):
        self.send_keys(xpath["mobile"], self.values["MobileNo"])
        self.click(xpath["continue"])
        print("Payment Initiated")

    def main(self):
        self.driver = create_driver(headless=False)
        self.wait = WebDriverWait(self.driver, 10)

        self.driver.get("https://www.irctc.co.in/nget/train-search")

        self.signin()

        self.enter_form()

        self.select_ticket()

        self.add_passengers()

        self.start_payment()

        print("Please finish the payment.")

        while True:
            time.sleep(1)
