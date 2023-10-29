from selenium import webdriver
import csv
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

chrome_options = Options()
chrome_options.add_argument("--headless")


##################################################################################################
                            #MOBALYTICS PART OF THE CODE TO GET TRAITS PLAYED
##################################################################################################
# Get our desired URL
# Define the variable
def run_main(username, region):

    driver = webdriver.Chrome(options=chrome_options)
    # Use the variable in the URL
    url = f'https://mobalytics.gg/tft/profile/{region}/{username}/overview'
    driver.get(url)
    print("Opening Web Page..")

    section_selector = '#container > div > main > div.m-0 > div.m-150a24d > div > section > div.m-dk3zxg > div.m-shxquu > div:nth-child(2) > div.m-9q6abw > div > div.m-1cm5is6 > div:nth-child(1) > div > div.m-1340igm'
    wait = WebDriverWait(driver, 2)
    section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, section_selector)))

    synergy_selector = '#container > div > main > div.m-0 > div.m-150a24d > div > section > div.m-dk3zxg > div.m-shxquu > div:nth-child(2) > div.m-9q6abw > div > div.m-1cm5is6 > div:nth-child(1) > div > div.m-yyfeiv'
    wait = WebDriverWait(driver, 2)
    comp_synergy = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, synergy_selector)))
    print("Getting synergies section..")

    # Open our CSV file and write the data
    with open('traits.csv', 'w', newline='') as csvFile:
        wr = csv.writer(csvFile)
        print("Creating a CSV file..")

        # Extract synergy data
        synergies = comp_synergy.find_elements(By.CSS_SELECTOR, '.m-1y4rea4')
        for synergy in synergies:
            synergy_name = synergy.find_element(By.CSS_SELECTOR, 'img').get_attribute('alt')
            synergy_number = synergy.find_element(By.CSS_SELECTOR, '.m-14hlyo4').text
            wr.writerow([synergy_name, synergy_number])
            
        print("Finished writing to results file.")

    ##################################################################################################
                    #MOBALYTICS PART OF THE CODE TO COMP AND QUANTITY OF CHARACTERS
    ##################################################################################################

    new_selector = '#container > div > main > div.m-0 > div.m-150a24d > div > section > div.m-dk3zxg > div.m-shxquu > div:nth-child(2) > div.m-9q6abw > div:nth-child(1) > div.m-1cm5is6 > div > div > div.m-1340igm > div.m-w9u5u2'
    wait = WebDriverWait(driver, 2)
    new_section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, new_selector)))
    print("Getting the new section data..")

    # Open our CSV file and write the data
    data_list = []
    with open('comp.csv', 'w', newline='') as csvFile:
        wr = csv.writer(csvFile)
        print("Creating a CSV file..")

        # Extract data
        items = new_section.find_elements(By.CSS_SELECTOR, 'div')  # Assuming each item is a div inside the container
        for item in items:
            text_content = item.text.strip()  # Getting text and stripping off any spaces
            if text_content:  # Making sure it's not an empty string
                data_list.append(text_content)
                wr.writerow([text_content])

        # Adding a total count variable character_ammount
        character_ammount = len(data_list)
        
        print("Finished writing to data.csv.")

    ##################################################################################################
                                #TACTICS.TOOLS PART OF THE CODE
    ##################################################################################################
    # Read all workable traits from workable_traits.csv
    workable_traits = set()
    with open('workable_traits.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            workable_traits.add(row[0])

    # Step 1: Read top 3 rows from results.csv
    synergies = []
    with open('traits.csv', 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 3:  # Only the top 3 rows
                break
            synergies.append(f"{row[1]} {row[0]}")  # In the format "number words"

    # Step 2: Navigate to the URL using Selenium
    ##driver = webdriver.Chrome()
    driver.get('https://tactics.tools/explorer')


    # Step 3: Input the data into the specified fields
    # Individual input field selector template (we will modify the nth-child for each input)
    input_field_template = '#__next > div > div > div > div.flex.w-full.pb-8.lg\\:max-w-\\[calc\\(100vw-30px\\)\\] > div > div.flex.w-full.justify-evenly > div > div > div > div.flex.flex-col.items-center.xl\\:flex-row.xl\\:items-start.xl\\:justify-start.xl\\:sticky.xl\\:top-\\[108px\\].gap-8.justify-center.mt-4 > div.w-\\[260px\\].md\\:w-full.xl\\:w-\\[260px\\].p-4.self-start.rounded.bg-bg.flex.flex-col.md\\:flex-row.xl\\:flex-col.gap-6.justify-center.sticky.top-\\[108px\\] > div:nth-child({index}) input'


    for i, synergy in enumerate(synergies):
        try:
            if synergy not in workable_traits and i < 2:
                synergy_parts = synergy.split()
                adjusted_number = str(int(synergy_parts[0]) + 1)
                synergy = f"{adjusted_number} {synergy_parts[1]}"
            # Find the specific input field using the template selector
            input_field_selector = input_field_template.format(index=i+1)
            input_field = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_field_selector)))

            # Send the synergy to the input field
            input_field.send_keys(synergy)

            # Send the ENTER key to populate the field
            input_field.send_keys(Keys.ENTER)
            

            # If the results section reloads after each input, we need to add a wait condition here
            # For example, if there's a specific element in the results section that appears every time it reloads:
            result_element_selector = 'YOUR_SELECTOR_FOR_AN_ELEMENT_IN_THE_RESULTS_SECTION'
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, result_element_selector)))

        except Exception as e:
            print(f"Error inputting {synergy}. Error: {e}")

    # 4. Wait for the page to update and extract unit names
    units_container_selector = '#__next > div > div > div > div.flex.w-full.pb-8.lg\\:max-w-\\[calc\\(100vw-30px\\)\\] > div > div.flex.w-full.justify-evenly > div > div > div > div.flex.flex-col.items-center.xl\\:flex-row.xl\\:items-start.xl\\:justify-start.xl\\:sticky.xl\\:top-\\[108px\\].gap-8.justify-center.mt-4 > div.bg-bg.rounded.w-screen.max-w-\\[780px\\].min-h-\\[240px\\].py-2.relative > div > div:nth-child(3) > div.font-medium.font-montserrat.text-\\[15px\\].leading-\\[22px\\] > div:nth-child(3) > div > div.sticky.left-0.z-10.tbl-body-inner-md.pl-\\[4px\\].css-1uy059i'
    try:
        units_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, units_container_selector))
        )
    except TimeoutException:
        print("The traits being inputted are not of the right value for tactics.tools")
        with open('units.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Insufficient data"])
        driver.quit()
        exit()

    unit_elements = units_container.find_elements(By.TAG_NAME, "div")

    # Initialize a set to keep track of unique unit names
    unique_units = set()
    character_total = []

    # Extract unique unit names until you get 10 of them
    for unit in unit_elements:
        unit_name = unit.text.split('\n')[0].strip()  # Strip to remove any surrounding whitespace
        if unit_name and unit_name not in unique_units:  # Check if unit_name is not empty
            unique_units.add(unit_name)
            character_total.append(unit_name)
            if len(character_total) == character_ammount:
                break


    print(character_total)  # To display the extracted unit names

    # 5. Write the results to units.csv
    with open('units.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Unit Name"])  # Header row
        for unit in character_total:
            writer.writerow([unit])  # Writing each unit name as a new row

    # Step 6: Navigate to the 'augments' section
    augments_tab_selector = '#__next > div > div > div > div.flex.w-full.pb-8.lg\:max-w-\[calc\(100vw-30px\)\] > div > div.flex.w-full.justify-evenly > div > div > div > div.flex.flex-col.items-center.xl\:flex-row.xl\:items-start.xl\:justify-start.xl\:sticky.xl\:top-\[108px\].gap-8.justify-center.mt-4 > div.bg-bg.rounded.w-screen.max-w-\[780px\].min-h-\[240px\].py-2.relative > div > div.p-2 > div > div > div > button:nth-child(4)'
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, augments_tab_selector))
    ).click()

    # Step 7: Click on the 'Place' header to ensure results are sorted in descending order
    place_header_selector = '#tbl-header > div > div.flex.items-center.px-\[14px\].css-1og9gw0.justify-end.cursor-pointer.h-full.tbl-cell-right-border > span'
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, place_header_selector))
    ).click()

    # Step 8: Extract augment columns data

    augment_rows_selector = '#__next > div > div > div > div.flex.w-full.pb-8.lg\\:max-w-\\[calc\\(100vw-30px\\)\\] > div > div.flex.w-full.justify-evenly > div > div > div > div.flex.flex-col.items-center.xl\\:flex-row.xl\\:items-start.xl\\:justify-start.xl\\:sticky.xl\\:top-\\[108px\\].gap-8.justify-center.mt-4 > div.bg-bg.rounded.w-screen.max-w-\\[780px\\].min-h-\\[240px\\].py-2.relative > div > div:nth-child(4) > div > div:nth-child(3) > div > div.sticky.left-0.z-10.tbl-body-inner-md.pl-\\[4px\\].css-ptqyv3'
    augment_rows = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, augment_rows_selector))
    )
    augment_elements = augment_rows.find_elements(By.TAG_NAME, "div")

    # Initialize a set to keep track of unique unit names
    unique_augments = set()
    augment_total = []

    # Extract unique unit names until you get 10 of them
    for augment in augment_elements:
        augment_name = augment.text.split('\n')[0].strip()  # Strip to remove any surrounding whitespace
        if augment_name and augment_name not in unique_augments:  # Check if unit_name is not empty
            unique_augments.add(augment_name)
            augment_total.append(augment_name)
            if len(augment_total) == 25:
                break


    print(augment_total)  # To display the extracted unit names

    # Step 9: Extract augment place data
    rows_selector = "#tbl-body > div > div"
    place_values = []

    # Get all the rows
    rows = driver.find_elements(By.CSS_SELECTOR, rows_selector)

    # Iterate over the rows to get the Place value for each one
    for index, row in enumerate(rows, start=1):
        try:
            # Construct the CSS selector for each row's Place value
            place_selector = f"#tbl-body > div > div:nth-child({index}) > div.flex.items-center.justify-end.px-\\[14px\\].css-1og9gw0.tbl-cell-right-border"
            
            place_element = driver.find_element(By.CSS_SELECTOR, place_selector)
            place_values.append(place_element.text.strip())

            # Break after fetching 25 values
            if len(place_values) == 25:
                break
        except Exception as e:
            print(f"Error fetching the Place value for row {index}. Error: {e}")

    print(place_values)


    # Step 10: Write the augment and place data to a new CSV
    with open('augments.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Augment Name", "Place"])  # Header row
        for augment, place in zip(augment_total, place_values):
            writer.writerow([augment, place])  # Writing both augment name and its place value as the same row

    print("Finished writing to augments.csv.")


    driver.quit()
