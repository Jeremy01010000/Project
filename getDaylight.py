import requests
from bs4 import BeautifulSoup
import csv

def get_page_info(url, month, year):
    ## Send a GET request to the URL
    response = requests.get(url)

    ## Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        ## Extract information from the page
        table = soup.find(id='as-monthsun').find('tbody')
        rows = table.find_all('tr')

        info = []

        ## Keep only sun rise/set times
        for row in rows:
            info.append(row.find_all('td')[:2])

        ## Extract all text values from elements
        raw_info = [data.text for lst in info for data in lst]

        ## Format times to military times
        clean_data = []
        for data in raw_info:
            if data.find('am') != -1:
                clean_data.append(data[:data.find('am')-1].replace(":", ""))
            elif data.find('pm') != -1:
                clean_data.append(str(int(data[:data.find('pm')-1].replace(":", ""))+1200))
            else:
                continue

        ## Pair day's times together
        clean_data = [[clean_data[i], clean_data[i + 1]] for i in range(0, len(clean_data), 2)]

        ## Dump info in CSV
        with open('daylightLA.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            for day, info in enumerate(clean_data):
                spamwriter.writerow([f'{month:02d}/{day+1:02d}/{year}', *info])

    else:
        print("Failed to retrieve the page.")


def populate_csv():

    ## Writting the headers in CSV
    schema = ["Date", "Time AM", "Time PM"]
    with open('daylightLA.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow([g for g in schema])

    ## Get info throughout the years
    for year in range(2020, 2024):
        for month in range(1, 13):        
            url = f'https://www.timeanddate.com/sun/usa/los-angeles?month={month}&year={year}'
            get_page_info(url, month, year)


if __name__ == "__main__":
    populate_csv()