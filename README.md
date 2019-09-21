# PyConCur

*Just learning Python and having fun*

**Converts one currency to another by web scraping currency rates.**

[List of Available Currencies](https://pastebin.com/raw/pMbhnuiM)

## Module Usage
```
$ ls -1
example_your_project.py

$ git clone https://github.com/Funkallero/PyConCur.git

$ ls -1
example_your_project.py
PyConCur/
```
```
usage   : ConCur([TO], [FROM], [AMOUNT])
default : ConCur('USD', 'EUR', 1)

examples:

c = ConCur ('dkk', 'usd', 100) >>> c.conversion returns 100 USD in DKK
c = ConCur ('dkk', 100)        >>> c.conversion returns 100 EUR in DKK
c = ConCur ()                  >>> c.conversion returns   1 EUR in USD
```
### Examples
```python
>>> from PyConCur.concur import ConCur
>>> c = ConCur()
>>> c.conversion
1.136991
>>> c.timestamp
'2019-06-30 08:02:00'
>>> y = ConCur('nok', 'sek', 42)
>>> y.conversion
38.57582323046362
>>> y.all_rates()
```
```
Src : x-rates.com
Base: EUR
Date: '2019-06-30 08:45:59' UTC

                  Country Currency     Rate From   Rate To
0          Argentine Peso      ARS     61.479698  0.016266
1       Australian Dollar      AUD      1.663562  0.601120
2          Bahraini Dinar      BHD      0.421699  2.371358
3           Botswana Pula      BWP     12.390234  0.080709
4          Brazilian Real      BRL      4.619463  0.216475
5         Bruneian Dollar      BND      1.558730  0.641548
6           Bulgarian Lev      BGN      1.955830  0.511292
7         Canadian Dollar      CAD      1.488455  0.671838
8            Chilean Peso      CLP    807.165778  0.001239
9   Chinese Yuan Renminbi      CNY      7.954439  0.125716
10         Colombian Peso      COP   3859.088521  0.000259
11          Croatian Kuna      HRK      7.435511  0.134490

# .... and so on (it will display all rates)
```
###### Run a test to check accuracy. Testing PyConCur against https://fixer.io API. 
```python
>>> from PyConCur.concur import test_concur
>>> test_concur()
```
```
Running 100 conversions in total.
Each conversion must score above 99% accuracy in order to pass.
The test itself is passed, if the average accuracy of all conversions is above 99.8%.

RESULT: TEST PASSED

TEST SUMMARY:
Passed: 99
Failed: 1
Avg Accuracy: 99.873%

TEST ERRORS:

Test 73 returned below or equal to 99% accuracy.

Conversion from 200 OMR to MUR.
Tried Conversion: 18725.565 MUR
Actual Conversion: 18522.166 MUR
Error Margin: 98.91%
```
### CLI Usage
```
usage: concur.py [-h] [-a A] [-f F] [-t T] [-p P] [-test TEST]

optional arguments:
  -h, --help  show this help message and exit
  -a A        A = the amount to convert (default: -a 1).
  -f F        F = the currency to convert from (default: -f EUR).
  -t T        T = the currency to convert to (default: -t USD).
  -p P        Get all rates in relation to EUR in a dataframe. (usage: -p all)
  -test TEST  Test conversion accuracy. Runs 100 tests. (usage: -test on)
```
### Examples
```
$ python3 concur.py

Converting Euro to US Dollar
Rates from 2019-07-07 00:15:57 UTC
Source: ecb.europa.eu

1 EUR = 1.126 USD
```
```
$ python concur.py -t dkk -a 10

Converting Euro to Danish Krone
Rates from 2019-07-07 00:15:57 UTC
Source: ecb.europa.eu

10.0 EUR = 74.635 DKK
```
```
$ python concur.py -t aud -f usd -a 1857.35

Converting US Dollar to Australian Dollar
Rates from 2019-07-07 00:15:57 UTC
Source: ecb.europa.eu

1857.35 USD = 2658.621 AUD
```
```
$ python concur.py -p all

Src : x-rates.com
Base: EUR
Date: 2019-07-07 00:17:34 UTC

                  Country Currency     Rate From   Rate To
0          Argentine Peso      ARS     61.479698  0.016266
1       Australian Dollar      AUD      1.663562  0.601120
2          Bahraini Dinar      BHD      0.421699  2.371358
3           Botswana Pula      BWP     12.390234  0.080709
4          Brazilian Real      BRL      4.619463  0.216475
5         Bruneian Dollar      BND      1.558730  0.641548
6           Bulgarian Lev      BGN      1.955830  0.511292
7         Canadian Dollar      CAD      1.488455  0.671838
8            Chilean Peso      CLP    807.165778  0.001239
9   Chinese Yuan Renminbi      CNY      7.954439  0.125716
10         Colombian Peso      COP   3859.088521  0.000259
11          Croatian Kuna      HRK      7.435511  0.134490
12           Czech Koruna      CZK     25.972408  0.038502
13           Danish Krone      DKK      7.494460  0.133432

# .... and so on (it will display all rates)
```
###### Run a test to check accuracy. Testing PyConCur against https://fixer.io API. 
```
$ python concur.py -test on

Running 100 conversions in total. Each conversion must score above 99% accuracy in order to pass.
The test itself is passed, if the average accuracy of all conversions is above 99.8%.

RESULT: TEST PASSED

TEST SUMMARY:
Passed: 99
Failed: 1
Avg Accuracy: 99.869%

TEST ERRORS:

Test 35 returned below or equal to 99% accuracy.

Conversion from 347 BHD to MUR.
Tried Conversion: 33223.278 MUR
Actual Conversion: 32813.637 MUR
Error Margin: 98.76%
```
### Error Example
```sh
$ python concur.py -t aud -f usda -a 1857.35

Input Error. Currency 'USDA' cannot be found.
Try again.
```
```sh
$ python concur.py -t audt -f usda -a 1857.35

Input Error. Both currencies 'AUDT' and 'USDA' cannot be found.
Try again.
```
**To do:**

**[1]** 
###### Implement re.match() to match input and scrape ecb if match else x-rates
**[2]**
###### Scrape more sites other than x-rates.com and ecb.europa.eu
**[3]**
###### Add more currencies. Currently supports 53
**[4]**
###### Extend DataFrame to easily change base currency

*/Christian Lindeneg*