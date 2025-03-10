import asyncio
import time
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def fetch_by_licence_no(licence_no):
    async with async_playwright() as p:
        start_time = time.time()  # Start the timer

        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to the webpage
        await page.goto("https://www.cea.gov.sg/aceas/public-register/ea/11")
        await page.wait_for_selector("input[name='licenseNumber']")
        
        # Enter the agent ID and submit the form
        await page.fill("input[name='licenseNumber']", licence_no)
        await page.click("button[type='submit']")
        await page.wait_for_load_state('networkidle')

        # Click on the "View more details" link
        await page.wait_for_selector("a[title='View']")
        await page.click("a[title='View']")
        
        # Wait for the new page to load
        await asyncio.sleep(1)
        pages = page.context.pages
        new_page = pages[-1]  # The last opened page should be the details page
        await new_page.wait_for_load_state('networkidle')

        # Get the new page content and parse it with BeautifulSoup
        content = await new_page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Extracting agent details
        name = soup.find("h1", class_="has-text-primary")
        agent_name = name.text.strip() if name else "No name found"

        fields = soup.find_all("div", class_="field xb-input is-horizontal")
        data = {"Agent Name": agent_name}

        for field in fields:
            label = field.find("label")
            value = field.find("span")
            if label and value:
                data[label.text.strip()] = value.text.strip()
        
        # Close the browser
        await browser.close()
        end_time = time.time()
        print(f"Total time taken: {end_time - start_time:.2f} seconds.")

        return data

async def fetch_by_registration_No(agent_id):
    async with async_playwright() as p:
        start_time = time.time()  # Start the timer

        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to the webpage
        await page.goto("https://www.cea.gov.sg/aceas/public-register/sales/1")
        await page.wait_for_selector("input[name='registrationNumber']")
        
        # Enter the agent ID and submit the form
        await page.fill("input[name='registrationNumber']", agent_id)
        await page.click("button[type='submit']")
        await page.wait_for_load_state('networkidle')

        # Click on the "View more details" link
        await page.wait_for_selector("a[title='View']")
        await page.click("a[title='View']")
        
        # Wait for the new page to load
        await asyncio.sleep(1)
        pages = page.context.pages
        new_page = pages[-1]  # The last opened page should be the details page
        await new_page.wait_for_load_state('networkidle')

        # Get the new page content and parse it with BeautifulSoup
        content = await new_page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Extracting agent details
        name = soup.find("h1", class_="has-text-primary")
        agent_name = name.text.strip() if name else "No name found"

        fields = soup.find_all("div", class_="field xb-input is-horizontal")
        data = {"Agent Name": agent_name}

        for field in fields:
            label = field.find("label")
            value = field.find("span")
            if label and value:
                data[label.text.strip()] = value.text.strip()
        
        # Close the browser
        await browser.close()
        end_time = time.time()
        print(f"Total time taken: {end_time - start_time:.2f} seconds.")

        return data

def fetchDetails(identifier):
    if identifier.startswith("L"):
        return asyncio.run(fetch_by_licence_no(identifier))
    elif identifier.startswith("R"):
        return asyncio.run(fetch_by_registration_No(identifier))
    else:
        return "Invalid identifier format. It should start with 'L' or 'R'."
