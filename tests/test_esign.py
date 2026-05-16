# test_esign.py
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://test-env-slim.synel-saas.com"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VALID_PDF = os.path.join(SCRIPT_DIR, "test_files", "valid.pdf")
INVALID_TXT = os.path.join(SCRIPT_DIR, "test_files", "invalid.txt")

def setup_driver():
    """Set up headless Chrome driver for CI or local run."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)

def test_positive_submission():
    """Positive test: all valid data should submit successfully."""
    driver = setup_driver()
    driver.get(BASE_URL)
    driver.find_element(By.ID, "Description").send_keys("Test")
    Select(driver.find_element(By.ID, "Recipient")).select_by_visible_text("John Smith")
    Select(driver.find_element(By.ID, "Category")).select_by_visible_text("Onboarding")
    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(VALID_PDF)
    driver.find_element(By.ID, "SenderEmail").send_keys("test@example.com")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    WebDriverWait(driver, 5).until(lambda d: d.current_url != BASE_URL)
    assert driver.current_url != BASE_URL
    driver.quit()

def test_no_file_selected_bug():
    """Bug: form submits without any file selected."""
    driver = setup_driver()
    driver.get(BASE_URL)
    driver.find_element(By.ID, "Description").send_keys("Test")
    Select(driver.find_element(By.ID, "Recipient")).select_by_visible_text("John Smith")
    Select(driver.find_element(By.ID, "Category")).select_by_visible_text("Onboarding")
    driver.find_element(By.ID, "SenderEmail").send_keys("test@example.com")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    if driver.current_url != BASE_URL:
        raise AssertionError("BUG: Form submitted without file")
    driver.quit()

def test_non_pdf_file_bug():
    """Bug: application accepts .txt (non-PDF) files."""
    driver = setup_driver()
    driver.get(BASE_URL)
    driver.find_element(By.ID, "Description").send_keys("Test")
    Select(driver.find_element(By.ID, "Recipient")).select_by_visible_text("John Smith")
    Select(driver.find_element(By.ID, "Category")).select_by_visible_text("Onboarding")
    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(INVALID_TXT)
    driver.find_element(By.ID, "SenderEmail").send_keys("test@example.com")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    if driver.current_url != BASE_URL:
        raise AssertionError("BUG: Application accepted .txt file")
    driver.quit()

def test_invalid_email_bug():
    """Bug: email without '@' is accepted."""
    driver = setup_driver()
    driver.get(BASE_URL)
    driver.find_element(By.ID, "Description").send_keys("Test")
    Select(driver.find_element(By.ID, "Recipient")).select_by_visible_text("John Smith")
    Select(driver.find_element(By.ID, "Category")).select_by_visible_text("Onboarding")
    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(VALID_PDF)
    driver.find_element(By.ID, "SenderEmail").send_keys("invalid_email")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    if driver.current_url != BASE_URL:
        raise AssertionError("BUG: Form submitted with invalid email")
    driver.quit()

if __name__ == "__main__":
    test_positive_submission()
    test_no_file_selected_bug()
    test_non_pdf_file_bug()
    test_invalid_email_bug()
    print("All tests completed.")
