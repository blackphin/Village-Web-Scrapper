# %% [markdown]
# Imports

# %%
import json

from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager


# %% [markdown]
# Webdriver Initialization

# %%
url = "https://villageinfo.in"

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
driver.get(url)

# %% [markdown]
# Scroll to the Bottom of the Page

# %%
def scroll_bottom(scroll_pause_time=0):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script(
            "window.scrollTo({top: document.body.scrollHeight-7000,left: 0,behavior: 'smooth'});"
        )

        # Wait to load page
        sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# %% [markdown]
# Collect Village Link List

# %%
village_links = []
state_elements = driver.find_elements(by=By.CSS_SELECTOR, value=".tab span a")

state_links = []
for state_element in state_elements:
    state_link = state_element.get_attribute("href")
    state_links.append(state_link)
    # break

for state_link in state_links:
    driver.get(state_link)
    scroll_bottom()
    district_elements = driver.find_elements(
        by=By.CSS_SELECTOR, value=".vict tbody tr td a"
    )

    district_links = []
    for district_element in district_elements:
        district_link = district_element.get_attribute("href")
        district_links.append(district_link)
        # break

    for district_link in district_links:
        driver.get(district_link)
        scroll_bottom()
        tehsil_elements = driver.find_elements(
            by=By.CSS_SELECTOR, value=".vict tbody tr td a"
        )

        tehsil_links = []
        for tehsil_element in tehsil_elements:
            tehsil_link = tehsil_element.get_attribute("href")
            tehsil_links.append(tehsil_link)
            # break

        for tehsil_link in tehsil_links:
            driver.get(tehsil_link)
            scroll_bottom()
            village_elements = driver.find_elements(
                by=By.CSS_SELECTOR, value=".vict tbody tr td a"
            )

            for village_element in village_elements:
                village_link = village_element.get_attribute("href")
                village_links.append(village_link)
    # break


# %% [markdown]
# Collect Data

# %%
data = []
for village_link in village_links:
    driver.get(village_link)
    scroll_bottom()
    dict_data = {}

    dict_data["state_name"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vi tbody tr:nth-child(4) td:nth-child(2)"
    ).text
    dict_data["district_name"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vi tbody tr:nth-child(3) td:nth-child(2)"
    ).text
    dict_data["tehsil_name"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vi tbody tr:nth-child(2) td:nth-child(2)"
    ).text
    dict_data["village_name"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".left-column h2"
    ).text
    dict_data["village_link"] = village_link
    dict_data["pincode"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vi tbody tr:nth-child(5) td:nth-child(2)"
    ).text
    dict_data["area"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vi tbody tr:nth-child(6) td:nth-child(2)"
    ).text
    dict_data["population"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vi tbody tr:nth-child(7) td:nth-child(2)"
    ).text
    dict_data["households"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vi tbody tr:nth-child(8) td:nth-child(2)"
    ).text
    dict_data["nearest_town"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vi tbody tr:nth-child(9) td:nth-child(2)"
    ).text

    dict_data["total_population"] = {}
    dict_data["total_population"]["total"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vict tbody tr:nth-child(1) td:nth-child(2)"
    ).text
    dict_data["total_population"]["male"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vict tbody tr:nth-child(1) td:nth-child(3)"
    ).text
    dict_data["total_population"]["female"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vict tbody tr:nth-child(1) td:nth-child(4)"
    ).text

    dict_data["literate_population"] = {}
    dict_data["literate_population"]["total"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vict tbody tr:nth-child(2) td:nth-child(2)"
    ).text
    dict_data["literate_population"]["male"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vict tbody tr:nth-child(2) td:nth-child(3)"
    ).text
    dict_data["literate_population"]["female"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vict tbody tr:nth-child(2) td:nth-child(4)"
    ).text

    dict_data["illiterate_population"] = {}
    dict_data["illiterate_population"]["total"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vict tbody tr:nth-child(3) td:nth-child(2)"
    ).text
    dict_data["illiterate_population"]["male"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vict tbody tr:nth-child(3) td:nth-child(3)"
    ).text
    dict_data["illiterate_population"]["female"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".vict tbody tr:nth-child(3) td:nth-child(4)"
    ).text

    dict_data["public_bus_service"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".table .row:nth-child(2) .column:nth-child(2)"
    ).text
    dict_data["private_bus_service"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".table .row:nth-child(3) .column:nth-child(2)"
    ).text
    dict_data["railway_station"] = driver.find_element(
        by=By.CSS_SELECTOR, value=".table .row:nth-child(4) .column:nth-child(2)"
    ).text

    about_elements_list = driver.find_elements(
        by=By.CSS_SELECTOR, value=".left-column .text-justify"
    )
    about = ""
    for about_element in about_elements_list:
        about += " " + about_element.text
        # about+="\n\n"
    dict_data["about"] = about

    nearby_villages_elements_list = driver.find_elements(
        by=By.CSS_SELECTOR, value=".vi-nbvli a"
    )
    nearby_villages = []
    for nearby_villages_element in nearby_villages_elements_list:
        nearby_villages.append(nearby_villages_element.text)
    dict_data["nearby_villages"] = nearby_villages

    print(dict_data)
    data.append(dict_data)
    # break


# %% [markdown]
# Dump Data to JSON

# %%
with open("data.json", "w") as file1:
    json.dump(data, file1)

# %% [markdown]
# Quit Webdriver

# %%
driver.close()
