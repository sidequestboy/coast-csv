# coast csv
This set of scripts pulls transaction data from coast capital web banking

## usage
* requires python3
```
pip install -r requirements.txt
python fetchcsv.py -t DEPOSITS -a 12345678 -p 1234567 01/01/2017 31/12/2017 2017-deposits.csv
python preprocess.py 2017-deposits.csv 2017-deposits.formatted.csv
```


