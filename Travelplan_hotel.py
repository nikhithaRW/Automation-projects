import time
from datetime import datetime, timedelta
from Travelplan_cab import TravelPlan2
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TravelPlan3(TravelPlan2):
    def __init__(self, timeout: int, browser: str):
        super().__init__(timeout, browser)

    def booking_hotel(self):
        self.driver.get("https://www.booking.com")
        self.driver.maximize_window()

        select_category = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Where are you going?']")))
        select_category.click()
        select_category.send_keys(self.arrival_city)
        select_category.send_keys(Keys.RETURN)

        # Set target dates
        no_of_days_you_want_to_stay=2 #here need to provide no of days
        target_date = datetime.strptime(self.target_date_str, '%d %B %Y')
        next_date = target_date + timedelta(days=no_of_days_you_want_to_stay)
        combined_dates = [self.target_date_str, next_date.strftime("%d %B %Y")]

        # Navigate to correct month
        while True:
            month_element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, "//h3[@class='eleebb6ale ee7ec6b631']")))

            displayed_month_year = datetime.strptime(month_element.text, '%B %Y')
            if displayed_month_year.year == target_date.year and displayed_month_year.month == target_date.month:
                break
            elif displayed_month_year > target_date:
                prev_button = WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Previous month']"))
                )
                prev_button.click()
            else:
                next_button = WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next month']")))
                next_button.click()

        # Select dates
        for date_str in combined_dates:
            select_date = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, f"//span[@aria-label='{date_str}']")))
            select_date.click()
        time.sleep(3)

        # Search button
        search = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Search')]")))

        search.click()

        self.driver.find_element(By.XPATH, "//div[@data-testid='title']").click()
        print("Please select the category of room and provide the details and complete the payment process")
        time.sleep(10)
        self.driver.quit()


stay = TravelPlan3(50, 'chrome')
stay.booking_hotel()


