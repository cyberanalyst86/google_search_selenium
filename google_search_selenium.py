from selenium.webdriver.common.by import By
from selenium import webdriver
import re
import pandas as pd
import requests
import os

def write_pdf_to_directory(response, filename):

  isExist = os.path.exists(filename)

  if isExist == False:

    with open(filename, 'wb') as f:
      for chunk in response.iter_content(1024):
        f.write(chunk)

    print(f"Downloaded PDF: {filename}")

  else:

    print("error writing PDF to directory")


  return


def download_pdf(url, filename):

    print(url)

    try:

        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for unsuccessful downloads
        write_pdf_to_directory(response, filename)

    except requests.exceptions.HTTPError:

        print("error downloading PDF")

    return

def search_google(query):

    PDF_url_list = []

    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)

    search_box.submit()
    driver.implicitly_wait(0.1)

    response = requests.get(driver.current_url)
    driver.close()

    count = 1

    for i in response.text.split("href=\"/url?q="):

        for j in re.findall(".*pdf&|.*PDF&", i):

            https_match = re.findall("http://.*.pdf&|https://.*.pdf&", j)
            non_url_match = re.match("/search%3.*", j)

            if not non_url_match:

                if len(https_match) > 0:

                    PDF_url_list.append(j.replace("pdf&", "pdf").replace("%25", "%"))

                    count+=1

                else:

                    continue

            else:

                continue

    return PDF_url_list


def main():

    query = input("Enter query: ")

    site = " site:cisa.gov | site:crowdstrike.com | site:recordedfuture.com | site:mandiant.com | site:IBM.com | site:microsoft.com"
    file_type = " filetype:pdf"

    google_dork = query + site + file_type

    print("Search: \"" + str(google_dork) + "\"")

    PDF_url_list = search_google(google_dork)

    print("Download PDF")

    for PDF_url in PDF_url_list:

        filename = PDF_url.split("/")[-1]

        download_pdf(PDF_url, filename)

    print("completed......")

if __name__ == '__main__':
  main()