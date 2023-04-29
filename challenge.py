import requests
import argparse
import urllib3
import pandas as pd
import csv
import json
import sys


def calculate_grade(num):
    """
        	:param num: the sum of OK headers
        	:return: return the URL grade based on the num
        """
    if num == 6 or num == 5:
        grade = "A"
    elif num == 4:
        grade = "B"
    elif num == 3:
        grade = "C"
    elif num == 1 or num == 2:
        grade = "D"
    else:
        grade = "F"

    return grade


def url_info(url):
    """
    	:param url: the url to check
    	:return: the grade of each url, the headers it contains and the report time
    """

    # Disable the ssl-warnings
    urllib3.disable_warnings()

    summ = 0
    headers = []

    # Make a GET request to the URL using the requests library
    response = requests.get(url, verify=False)

    # Get the date from the response headers
    date = response.headers.get('Date')

    # Calculate the grade according to the Rules. If the header is OK - add 1 to sum and to the headers list
    if "Content-Security-Policy" in response.headers:
        summ += 1
        headers.append("Content-Security-Policy")

    if response.headers.get('X-Frame-Options') and 'sameorigin' in response.headers['X-Frame-Options'].lower():
        summ += 1
        headers.append('X-Frame-Options')

    if response.headers.get('Referrer-Policy') and 'strict-origin-when-cross-origin' in response.headers[
        'referrer-policy'].lower():
        summ += 1
        headers.append('Referrer-Policy')

    if 'X-Content-Type-Options' in response.headers:
        summ += 1
        headers.append('X-Content-Type-Options')

    if 'Permissions-Policy' in response.headers:
        summ += 1
        headers.append('Permissions-Policy')

    if 'Strict-Transport-Security' in response.headers:
        summ += 1
        headers.append('Strict-Transport-Security')

    return date, calculate_grade(summ), headers


def challenge():
    urls = []
    report = []

    # Create an argument parser
    parser = argparse.ArgumentParser(description='Get the URLs in command line or text file')
    parser.add_argument('-url', nargs='*', help="list of URLs")
    parser.add_argument('-path', help="text file containing URLS")

    # Parse the command line arguments
    args = parser.parse_args()

    # Check if it's a list or a file and create a URLs list
    if args.url:
        urls = args.url
    elif args.path:
        with open(args.path, 'r') as file:
            for line in file:
                urls.append(line.strip())
    else:
        # Check if any arguments were provided
        parser.print_help()

        # Exit the code
        sys.exit(0)

    print("Creating the report...")

    for url in urls:

        # Get the information for each URL
        info = url_info(url)
        date = info[0]
        grade = info[1]
        headers = info[2]
        report.append([url, date, grade, headers])

    fields = ['Site', 'Report Time', 'Grade', 'Available Headers']

    # Create a data frame using pandas
    df = pd.DataFrame(report, columns=fields)

    # Convert the data from list to dictionary
    dict = df.to_dict(orient='records')

    # Create a csv file and write the data to the file
    # We set orient = 'records' to convert each row of the dataframe to a separate object
    with open('report.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(dict)

    # Create a json file and write the data to the file
    with open("report.json", "w") as outfile:
        json.dump(dict, outfile, indent=4)

    print("Done! report.csv and report.json created ")

if __name__ == '__main__':
    challenge()
