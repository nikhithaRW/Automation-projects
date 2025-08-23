import time
from datetime import datetime
from Travelplan_flight import TravelPlan
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TravelPlan2(TravelPlan):
    flight_boarding_time=""
    flight_arrival_time=""

    def __init__(self, timeout: int, browser: str):
        super().__init__(timeout, browser)

    def booking_cab(self):
        self.driver.get("https://www.uber.com/")
        time.sleep(5)
        cab_pickup_point = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Pickup location' and @data-testid='dotcom-ui.pickup-destination.input.pickup']")))
        cab_pickup_point.click()
        pickup_point_address = "sai skanda apartments NRI layout"
        cab_pickup_point.send_keys(pickup_point_address)
        # cab_pickup_point.send_keys(Keys.ENTER)
        time.sleep(5)
        #
        # confirm_pickup_button = WebDriverWait(self.driver, self.timeout).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, "css-kSEpAB")))
        # confirm_pickup_button.click()

        cab_dropping_point = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Dropoff location' and @data-testid='dotcom-ui.pickup-destination.input.destination.drop0']")))
        cab_dropping_point.click()
        dropping_point_address = "Kempegowda international airport"
        cab_dropping_point.send_keys(dropping_point_address)

        confirm_dropping_button = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-kSEpAB")))
        confirm_dropping_button.click()

        date_elements = self.target_date_str.split(" ")
        day = date_elements[0]
        month = date_elements[1]
        year = date_elements[2]
        target_date = datetime.strptime(self.target_date_str, '%d %B %Y')
        day_of_week = target_date.strftime('%A')

        date_picker = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-testid='dotcom-ui.date-picker.input'][1]")))
        date_picker.click()

        year_button = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='dotcom-ui.date-picker.month-year-select-button'][2]")))
        year_button.click()

        time.sleep(3)

        ul_year_element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='css-kvIDFy']")))

        list_items = ul_year_element.find_elements(By.TAG_NAME, "li")
        list_year_dict = {}
        for item in list_items:
            item_id = item.get_attribute("id")
            list_year_dict[item.text] = item_id

        year_selection = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.ID, f"{list_year_dict.get(year)}"))
        )
        year_selection.click()
        time.sleep(3)

        # Select month
        month_button = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='dotcom-ui.date-picker.month-year-select-button'][1]"))
        )
        month_button.click()
        time.sleep(3)
        ul_month_element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='css-kvIDFy']"))
        )
        list_items = ul_month_element.find_elements(By.TAG_NAME, "li")
        list_month_dict = {}
        for item in list_items:
            item_id = item.get_attribute("id")
            list_month_dict[item.text] = item_id
        month_selection = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.ID, f"{list_month_dict.get(month)}"))
        )
        month_selection.click()

        # Select day
        day_selection = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@aria-label=\"Choose {day_of_week}, {month} {day}th {year}. It's available.\"]"))
        )
        day_selection.click()
        time.sleep(3)

        self.flight_boarding_time = self.flight_details.get('boarding_time')[-7:]
        self.flight_arrival_time = self.flight_details.get('arrival_time')[-7:]

        time_button = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '12:00 PM')]"))
        )
        time_button.click()
        time.sleep(5)

        ul_time_element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='css-eoEJt']"))
        )
        list_items = ul_time_element.find_elements(By.TAG_NAME, "li")
        list_time_dict = {}
        for item in list_items:
            item_id = item.get_attribute("id")
            list_time_dict[item.text] = item_id

        # Calculate nearest time
        flight_boarding_time_24 = datetime.strptime(self.flight_boarding_time, '%I:%M %p')
        hours = flight_boarding_time_24.hour - 2
        if hours < 0:
            hours += 24
        boarding_time_24_less_4hrs = flight_boarding_time_24.minute + hours * 60
        nearest_time = None
        for time_str in list_time_dict:
            if time_str == 'Now':
                continue
            time_24 = datetime.strptime(time_str, '%I:%M %p')
            time_24_minutes = time_24.minute + time_24.hour * 60
            if boarding_time_24_less_4hrs < time_24_minutes:
                nearest_time = time_str
                break
        print(nearest_time)

        nearest_time_selection = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.ID, f"{list_time_dict.get(nearest_time)}")))
        nearest_time_selection.click()

        print(f"Your boarding time will be {self.flight_boarding_time} and your arrival time will be {self.flight_arrival_time}. Please arrive at the airport before 2 hours.")

        see_prices_link = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//a[@data-baseweb='button' and text()='See prices']")))
        see_prices_link.click()

        login_using_qr = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='qr-code-button']")))
        login_using_qr.click()

        pickup_now = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH,
            "//button[@data-baseweb='button' and @data-tracking-name='date_time_button']//div[contains(text(), 'Pickup: ')]")))
        pickup_now.click()

        drop_off_by = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Dropoff by')]")))
        drop_off_by.click()

        pickup_time_element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Pickup time')]/following-sibling::span")))
        pickup_time = pickup_time_element.text
        print(
            f"Your pickup time will be {pickup_time}. Please be ready by that time so you will reach your destination on time. Don't miss your flight!")

        next_button = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Next')]")))
        next_button.click()

        self.driver.quit()
cab = TravelPlan2(120, "chrome")
cab.booking_cab()


