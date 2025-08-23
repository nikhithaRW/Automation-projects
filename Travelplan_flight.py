import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TravelPlan:
    flight_details = {}
    target_date_str = '25 September 2025'
    boarding_city = 'Bengaluru'
    arrival_city = 'Hyderabad'

    def __init__(self, timeout: int, browser: str):
        self.timeout = timeout
        if browser.lower() == "chrome":
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        elif browser.lower() == "edge":
            self.driver = webdriver.Edge()
            self.driver.maximize_window()
        else:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()

    def flight_booking(self):
        self.driver.get("https://www.booking.com")
        self.driver.maximize_window()

        select_category = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='flights']")))
        select_category.click()

        select_way = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='search_type_option_ONEWAY']")))
        select_way.click()

    # Selects from place
        boarding_place=WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-ui-name='input_location_from_segment_0']")))
        boarding_place.click()
        button=WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[@fdprocessedid='y5yfan']")))
        button.click()

        input_boarding=WebDriverWait(self.driver,self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Airport or city']")))
        input_boarding.click()
        input_boarding.send_keys(self.boarding_city)
        # input_boarding.send_keys(Keys.RETURN)

        checkbox = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='flights-searchbox_suggestions']/li")))
        checkbox.click()

        # Selects to place
        arrival_place=WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-ui-name='input_location_to_segment_0']")))
        arrival_place.click()

        input_arrival=WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Airport or city']")))
        input_arrival.click()
        input_arrival.send_keys(self.arrival_city)
        # input_arrival.send_keys(Keys.RETURN)

        checkbox=WebDriverWait(self.driver,self.timeout).until(
        EC.element_to_be_clickable((By.XPATH,"//*[@id='flights-searchbox_suggestions']/li")))
        checkbox.click()

        date_picker=WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[@placeholder='Choose departure date']")))
        date_picker.click()

        #navigate to correct year and month
        target_date=datetime.strptime(self.target_date_str, '%d %B %Y')
        while True:
            month_element=WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=':R4ll19d5:']/div/div/div/div/div/div[1]/h3")))
            displayed_month_year=datetime.strptime(month_element.text, '%B %Y')

            if displayed_month_year.year== target_date.year and displayed_month_year.month== target_date.month:
                break
            elif displayed_month_year > target_date:
                prev_button=WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id=':R4ll19d5:']/div/div/div/div/button[1]")))
                prev_button.click()
            else:
                next_button=WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id=':R4ll19d5:']/div/div/div/div/button[2]")))
                next_button.click()

        select_date=WebDriverWait(self.driver,self.timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@aria-label='{self.target_date_str}']")))
        select_date.click()

        time.sleep(3) #to verify, the correct date is selected

        search= WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-ui-name="button_search_submit"]')))
        search.click()
        
        durations =[]
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='flight_card_segment_duration_0']")))

        elements = self.driver.find_elements (By.XPATH,  "//div[@data-testid='flight_card_segment_duration_0']")
        for element in elements:
            durations.append(element.text)

        # Convert all durations to minutes and find the minimum

        hours, mins, total_mins=[], [], []
        for duration in durations:
            parts=duration.split(' ')
            hours.append(parts[0].strip('h'))
            if len(parts) > 1:
                mins.append(parts[1].strip('m'))
            else:
                mins.append('0')  # Default to 'On' if minutes part is missing
        for htime, mtime in zip(hours, mins):
            total_mins.append((60*(int(htime))+int(mtime)))

        min_duration = min(total_mins)

        min_duration_str=durations[total_mins.index(min_duration)]
        durations_dict = {}
        view_details = []

        for index in range(len(durations)):
            view_details.append(f"//*[@id='flight-card-{index}']/div/div/div[2]/div[2]/button")
            durations_dict[durations[index]] = view_details[index]

        # clicking details of minimum duration flight

        view_details_button = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, durations_dict[min_duration_str])))
        view_details_button.click()

        details_list=['boarding_time', 'flight_name', 'flight_number', 'arrival_time']
        xpaths_of_details_list = [
                    "//div[@data-testid='timeline_location_timestamp_departure']",
                    "//div[@data-testid='timeline_leg_info_carrier']",
                    "//div[@data-testid='timeline_leg_info_flight_number_and_class']",
                    "//div[@data-testid='timeline_location_timestamp_arrival']"]

        for i in range(len(details_list)):
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, xpaths_of_details_list[i])))
            self.flight_details[details_list[i]] = element.text

        check_in_flight=WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH,"//div[@data-testid='flight_details_inner_modal_select_button']//button")))
        check_in_flight.click()

        print(f"let's book flight with minimum duration of {min_duration_str}")
        time.sleep(10)
        self.driver.quit()

travel = TravelPlan( 50,  'chrome')
travel.flight_booking()
