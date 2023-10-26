from abstra.workflows import get_stage
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from os import getenv

ABSTRA_SELENIUM_URL = getenv("ABSTRA_SELENIUM_URL")

# Get workflow variables
stage = get_stage()
print(stage["selected_option"])

# Set initial variables for selenium
url = "https://hackernoon.com/"
state = "IDLE"


# Run selenium
def run_selenium():
    print("Running selenium")

    try:
        if ABSTRA_SELENIUM_URL:
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            driver = webdriver.Remote(
                command_executor=ABSTRA_SELENIUM_URL, options=options
            )
        else:
            driver = webdriver.Chrome()

        driver.get(url)
        driver.implicitly_wait(5)

        # find headlines
        retrieved_headlines = driver.find_elements(by=By.CSS_SELECTOR, value="h2 a")

        # retrieve headline text
        headline_titles = [h.text for h in retrieved_headlines]

        # retrieve headline links
        headline_links = [h.get_attribute("href") for h in retrieved_headlines]

        # create dataframe
        df = pd.DataFrame({"Headline": headline_titles, "Link": headline_links})

        driver.quit()

        return df

    except Exception as e:
        print(e)


df = run_selenium()
stage["headlines_df"] = df.to_dict()
