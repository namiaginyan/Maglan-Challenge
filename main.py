import csv
import json

import requests
import argparse
import urllib3
import pandas as pd

def grade_calculator(url):
    urllib3.disable_warnings()

    grade = 0
    response = requests.get(url, verify=False)

    if "Content-Security-Policy" in response.headers:
        grade += 1

    if response.headers.get('X-Frame-Options') and response.headers['X-Frame-Options'] == 'sameorigin':
        grade += 1

    if response.headers.get('Referrer-Policy') and response.headers['Referrer-Policy'] == 'strict-origin-when-cross-origin':
        grade += 1

    if 'X-Content-Type-Options' in response.headers:
        grade += 1

    if 'Permissions-Policy' in response.headers:
        grade += 1

    return grade

def challenge():
    urls = []
    report = []
    dict = []

    parser = argparse.ArgumentParser(description='Get the URLs in command line or text file')
    parser.add_argument('--URL', nargs='*', help="list of URLs")
    parser.add_argument('--path', help = "text file path containing URLS")
    args = parser.parse_args()

    if args.URL:
        urls = args.URL
    else:
        with open(args.path, 'r') as file:
            for line in file:
                urls.append(line.strip())

    for url in urls:
        report.append([url, grade_calculator(url)])
        #dict.append({'URL': url, 'GRADE':grade_calculator(url)})

    fields = ['URL', 'GRADE']

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
