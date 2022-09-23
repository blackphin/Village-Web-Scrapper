from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

url = "https://villageinfo.in/andaman-&-nicobar-islands/nicobars/car-nicobar/arong.html"
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


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


driver.get(url)
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
driver.close()
