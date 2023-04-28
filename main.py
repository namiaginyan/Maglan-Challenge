import csv
import json
import socket

import requests
import argparse
import urllib3
import pandas as pd


def grade_calculator(url):

    urllib3.disable_warnings()
    grade = 0
    headers = []
    response = requests.get(url, verify=False)

    if "Content-Security-Policy" in response.headers:
        grade += 1
        headers.append("Content-Security-Policy")

    if response.headers.get('X-Frame-Options') and response.headers['X-Frame-Options'].lower() == 'sameorigin':
        grade += 1
        headers.append('X-Frame-Options')

    if response.headers.get('Referrer-Policy') and response.headers[
        'Referrer-Policy'].lower() == 'strict-origin-when-cross-origin':
        grade += 1
        headers.append('Referrer-Policy')

    if 'X-Content-Type-Options' in response.headers:
        grade += 1
        headers.append('X-Content-Type-Options')

    if 'Permissions-Policy' in response.headers:
        grade += 1
        headers.append('Permissions-Policy')

    return grade, headers

def challenge():
    urls = []
    report = []

    parser = argparse.ArgumentParser(description='Get the URLs in command line or text file')
    parser.add_argument('--URL', nargs='*', help="list of URLs")
    parser.add_argument('--path', help="text file path containing URLS")
    args = parser.parse_args()

    if args.URL:
        urls = args.URL
    else:
        with open(args.path, 'r') as file:
            for line in file:
                urls.append(line.strip())

    for url in urls:
        info = grade_calculator(url)
        report.append([url, info[0], info[1]])
        # dict.append({'URL': url, 'GRADE':grade_calculator(url)})

    fields = ['Site','Grade', 'Headers']

    # Creating a data frame using pandas
    df = pd.DataFrame(report, columns=fields)

    # Converting the data from list to dictionary
    dict = df.to_dict(orient='records')

    # Creating a csv file and writing the data
    # We set orient = 'records' to convert each row of the dataframe to a separate JSON object
    with open('report.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(dict)

    # Creating a json file and writing the data
    with open("report.json", "w") as outfile:
        json.dump(dict, outfile, indent=4)


if __name__ == '__main__':
    challenge()
