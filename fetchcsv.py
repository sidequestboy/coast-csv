"""
FetchCSV

Usage:
    fetchcsv.py [-ta] <start-date> <end-date> <output-file>

Options:
    -h --help         Show this screen
    -t --transactions=(ALL|DEPOSITS|WITHDRAWALS|CHEQUES|BILLPAYMENTS)
        default ALL
    -a --account=num
    -p --pac=num
    start-date and end-date must be like this: 27/03/2017
"""

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":

    # commandline arguments
    import argparse, sys
    parser = argparse.ArgumentParser(description="FetchCSV")
    
    parser.add_argument("start-date")
    parser.add_argument("end-date")
    parser.add_argument("output-file")
    parser.add_argument("-t", "--transactions", default="ALL")
    parser.add_argument("-a", "--account", default=None)
    parser.add_argument("-p", "--pac", default=None)

    options = vars(parser.parse_args(sys.argv[1:]))
    
    import getpass
    if options["account"] is None:
        options["account"] = input("enter account: ")
    if options["pac"] is None:
        options["pac"] = getpass.getpass("enter personal access code: ")
    
    root = "https://www.coastcapitalsavings.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {
            "action": "panlogin",
            "branch": "001",
            "Continue": "Sign+in",
            "fromStep": "Step1",
            "fromUsecase": "Logon",
            "LOGON": "LOGON2",
            "pac": options["pac"],
            "acctnum": options["account"]}
    
    # begin session
    session = requests.Session()
    
    # log in to web banking
    r = session.post(root + "/OnlineBanking/", headers=headers, data = payload)
    
    # get link to account page bc it has some long token in it
    soup = BeautifulSoup(r.text, 'html.parser')
    accountpage = soup.select(".summarydata .value")[0].get("href") # chequing account
    # soup.select(".summarydata .value")[1].get("href") # membership shares account
    
    # navigate to account page
    r = session.get(root + accountpage)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # get form action link
    formactionlink = soup.select(".searchActivityForm")[0].get("action")
    
    # submit form
    r = session.post(root + formactionlink, headers=headers, data = {
        "fromAcct": "banking:0:0", # "banking:1:0" is stake account
        "StartDateValue": options["start-date"],
        "EndDateValue": options["end-date"],
        "OptionFilterNameValue": options["transactions"], # "ALL", "DEPOSITS", "WITHDRAWALS", "CHEQUES", "BILLPAYMENTS",
        "RadioTimeTypeValue": "DateRangeFilter",
        "srchvalue": "",
        "stype": "reverse_csv", # "csv" is newest to oldest, "pdfstmt" is pdf
        }
        )
    soup = BeautifulSoup(r.text, 'html.parser')
    # get csv link
    csvlink = soup.select(".control > a")[0].get("href")
    
    # download csv
    csv = session.get(root + csvlink, headers=headers)
    
    with open(options["output-file"], "w") as f:
        print(csv.text, file=f)
    
