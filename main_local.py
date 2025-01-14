import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from dotenv import load_dotenv

class ReserveDate:
    def __init__(self, chromedriver_path):
        load_dotenv()
        self.service = Service(executable_path=chromedriver_path)
        self.driver = webdriver.Chrome(service=self.service)
        self.wait = WebDriverWait(self.driver, 10)
        self.calendar_wait = WebDriverWait(self.driver, 20)

    def login(self, username, password):
        self.driver.get("https://reservenski.parkbrightonresort.com/login")
        
        email_element = self.wait.until(EC.presence_of_element_located((By.ID, "emailAddress")))
        email_element.send_keys(username)
        
        password_element = self.driver.find_element(By.ID, "password")
        password_element.send_keys(password)
        
        try:
            login_button = self.wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, "button.Login_submitButton__fMHAq"
            )))
        except:
            try:
                login_button = self.wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign In')]"
                )))
            except:
                login_button = self.wait.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, "button[type='submit']"
                )))
        
        login_button.click()

    def navigate_to_calendar(self):
        reserve_link = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[contains(text(), 'Reserve a Parking Spot')]"
        )))
        reserve_link.click()
        time.sleep(2)

    def check_date_availability(self, target_date_element):
        """Helper method to check if date has the available (green) background color"""
        try:
            background_color = target_date_element.value_of_css_property('background-color')
            target_color = "rgba(49, 200, 25, 0.2)"
            return background_color == target_color
        except Exception as e:
            print(f"Error checking date availability: {e}")
            return False

    def select_date(self, target_date_text, max_attempts, sleep_duration):
        attempt = 0
        
        while attempt < max_attempts:
            try:
                calendar_iframe = None
                
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                for iframe in iframes:
                    src = iframe.get_attribute('src') or ''
                    if 'doubleclick' not in src.lower() and 'analytics' not in src.lower():
                        calendar_iframe = iframe
                        break
                
                if calendar_iframe:
                    self.driver.switch_to.frame(calendar_iframe)
                
                calendar_container = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "mbsc-calendar-wrapper"))
                )
                
                date_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, "div.mbsc-calendar-cell-text.mbsc-calendar-day-text"
                )
                
                target_date = None
                for date in date_elements:
                    if date.is_displayed() and date.text == str(target_date_text):
                        target_date = date
                        break
                
                if target_date:
                    if self.check_date_availability(target_date):
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", target_date)
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", target_date)
                        print(f"Successfully selected available date {target_date_text}")
                        break
                    else:
                        print(f"Date {target_date_text} not available yet. Refreshing...")
                        time.sleep(sleep_duration)
                        self.driver.refresh()
                        attempt += 1
                else:
                    print(f"Could not find date element {target_date_text}")
                    break
                    
                if calendar_iframe:
                    self.driver.switch_to.default_content()
                    
            except Exception as e:
                print(f"Error in select_date: {e}")
                if calendar_iframe:
                    self.driver.switch_to.default_content()
                attempt += 1
                time.sleep(5)
                self.driver.refresh()

        if attempt >= max_attempts:
            raise Exception(f"Failed to find available date after {max_attempts} attempts")

    def select_carpool(self):
        try:
            carpool_element = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[text()='4+ Carpool (Occupancy will be verified by Parking Ambassador upon arrival)']"
            )))
            
            try:
                carpool_element.click()
            except:
                try:
                    self.driver.execute_script("arguments[0].click();", carpool_element)
                except:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(carpool_element).click().perform()
                    
        except Exception as e:
            print(f"Error in select_carpool: {e}")

    def checkout(self):
        try:
            checkout_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, 'PlainButton--noStyle')]//div[contains(text(), 'Pay $10.00 & Park')]"
            )))
            
            parent_button = checkout_button.find_element(
                By.XPATH, "./ancestor::button[contains(@class, 'PlainButton--noStyle')]"
            )
            
            try:
                parent_button.click()
            except:
                try:
                    self.driver.execute_script("arguments[0].click();", parent_button)
                except:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(parent_button).click().perform()
                    
        except Exception as e:
            print(f"Error in checkout: {e}")

    def confirm_reservation(self):
        try:
            # Look for the confirmation button using the specific class
            confirm_button = self.wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, "button.oGMkMQAoYbD7f3oxRBJI.ButtonComponent"
            )))
            print("Found confirmation button")
            
            # Try multiple clicking methods
            try:
                # Method 1: Regular click
                confirm_button.click()
            except:
                try:
                    # Method 2: JavaScript click
                    self.driver.execute_script("arguments[0].click();", confirm_button)
                except:
                    # Method 3: Action chains
                    actions = ActionChains(self.driver)
                    actions.move_to_element(confirm_button).click().perform()
            
            print("Clicked confirmation button")
            
            # Verify the click worked
            try:
                # Wait for URL change or confirmation message
                WebDriverWait(self.driver, 10).until(
                    lambda driver: "confirmation" in driver.current_url.lower() or 
                    len(driver.find_elements(By.CSS_SELECTOR, "[class*='success'], [class*='confirm']")) > 0
                )
                print("Successfully completed reservation")
                print("Current URL:", self.driver.current_url)
            except Exception as e:
                print(f"Failed to verify confirmation: {e}")
                print("Current URL:", self.driver.current_url)
            
        except Exception as e:
            print(f"Error clicking confirmation button: {e}")
            # Alternative approach using text content
            try:
                confirm_button = self.wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//button[text()='Confirm']"
                )))
                self.driver.execute_script("arguments[0].click();", confirm_button)
                print("Clicked confirmation button using text content")
            except Exception as e:
                print(f"Failed to find confirmation button with both methods: {e}")
                print("Current page source:")
                print(self.driver.page_source[:1000])

    def close(self):
        self.driver.quit()

    def make_reservation(self, username, password, target_date, max_attempts, sleep_duration):
        """Main method to execute the full reservation process"""
        try:
            self.login(username, password)
            self.navigate_to_calendar()
            self.select_date(target_date, max_attempts, sleep_duration)
            self.select_carpool()
            self.checkout()
            self.confirm_reservation()
        except Exception as e:
            print(f"Error during reservation process: {e}")
        finally:
            self.close()

def main():
    print("--------------------------------")
    print("Brighton Bot")
    print("\nBefore using, make sure on Honk mobile you have:")
    print("1. Your credit card info saved at: https://parking.honkmobile.com/payment-cards")
    print("2. Only one license plate saved at: https://parking.honkmobile.com/vehicles")
    print("--------------------------------")
    # Get credentials from environment variables or user input
    username = os.getenv('HONK_USERNAME') or input('Enter your Honk mobile email: ')
    password = os.getenv('HONK_PASSWORD') or input('Enter your Honk mobile password: ')
    target_date = input('Enter target date (day of month): ')
    max_attempts = int(input('Maximum number of attempts (default 100): ') or 100)
    sleep_duration = float(input('Sleep duration between attempts in seconds (default 5): ') or 5)
    
    chromedriver_path = "./chromedriver"  # Update this path to your chromedriver location
    bot = ReserveDate(chromedriver_path)
    bot.make_reservation(
        username,
        password,
        target_date,
        max_attempts,
        sleep_duration
    )

if __name__ == "__main__":
    main()
