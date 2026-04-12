# Functional Testing

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Example: Google Search Test
def test_google_search():
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Python testing" + Keys.RETURN)

    assert "Python" in driver.title
    driver.quit()

# Note: Requires Selenium WebDriver and browser driver installed.
