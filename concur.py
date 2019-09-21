#!bin/usr/python3
"""
Just having some fun in Python.
//christianlindeneg, June, 2019//

To do:
[1] - Implement re.match() to match input and scrape ecb if match else x-rates
[2] - Scrape more sites other than x-rates.com and ecb.europa.eu
[3] - Add more currencies. Currently supports 53
[4] - Extend DataFrame to easily change base currency
"""
try:
    # will work from terminal
    from utilities import CURRENCY, NAME_PATH, FROM_PATH, TO_PATH, ALT_PATH, URL, URL_ALT, MEM
except Exception:
    # will work as module
    from PyConCur.utilities import CURRENCY, NAME_PATH, FROM_PATH, TO_PATH, ALT_PATH, URL, URL_ALT, MEM

from os import system
import argparse
from json import load, loads, dump, dumps
from re import findall as fa
from time import time, gmtime, strftime
from datetime import datetime

try:
    from requests import get
except ImportError:
    system('pip3 install requests')
try:
    from lxml import html
except ImportError:
    system('pip3 install lxml')

class GetData:
    """
    Class holding functions for validating user-input and
    getting the actual data either from a query or local JSON.
    """
    def __init__(self, curTo, curFrom, amount, panda):
        self.amount = amount
        try:
            self.curFrom = curFrom.upper()
        except AttributeError:
            """
            likely means that  amount was entered as curFrom
            """
            self.amount = curFrom
            self.curFrom = 'EUR'

        self.curTo = curTo.upper()
        self.panda = panda
    
    def find_floats(self, n):
        """
        extracts floating numbers string
        """
        return fa(r"[-+]?\d*\.\d+|\d+", str(n))
    
    def get_data(self):
        """
        If input is valid, query local JSON file and 
        if rates are less than half-hour old, return them.

        If JSON rates are more than half-hour old, query x-rates.com for new rates.
        """
        if not self.check_format():
            # error msg already printed
            exit()

        else:
            # first check local storage
            checker = self.check_local()
            if checker != False and self.panda == False:
                self.rates = checker[0]
                self.rates_alt = checker[1]
                self.source = checker[2]

            else:
                # if false, query x-rates.com
                scraping = self.visit_xrates()
                if scraping != False:
                    self.rates = scraping[0]
                    self.rates_alt = scraping[1]
                else:
                    # if error, query ecb.europa.eu
                    scraping_two = self.visit_ecb()
                    if scraping_two != False:
                        self.rates = scraping_two[0]
                        self.rates_alt = scraping_two[1]
                    else:
                        # if all fails, likely due to internet con
                        print('\nRequest Error. Check internet connection.')
                        exit()

    def visit_xrates(self):
        """
        Scrapes x-rates.com and extracts currency-rates against 1 EUR. 
        Stores JSON file containing timestamp, currencies and respective rates.
        """
        try:
            request = get(URL)
            if request.status_code != 200:
                return False
        except:
            return False
        try:
            answer = html.fromstring(request.content)
        except NameError:
            print('\npip module \'lxml\' not installed\nor installed for the wrong Python version')
            exit()

        """
        uses xpaths from DOM to get what we need from the html 
        it'll contain each line in answer as an item in a list
        """ 
        names_ans = answer.xpath(NAME_PATH)
        from_cur_ans = answer.xpath(FROM_PATH)
        to_cur_ans = answer.xpath(TO_PATH)

        """
        converts the items of all three lists
        into type string to utilize string methods 
        """
        names_raw = [html.tostring(i) for i in names_ans]
        from_cur_raw = [html.tostring(i) for i in from_cur_ans]
        to_cur_raw = [html.tostring(i) for i in to_cur_ans]

        # contains all the currency abbreviations
        self.abb_names = [i for i in CURRENCY.keys()]

        """
        extracts the name from the html string
        it uses re.findall() to match currencies
        from utilities with the actual html string.
        if statement ensures that negative matches are ignored
        """
        self.names = []
        for check in CURRENCY.values():
            self.names.append([fa(check, str(name))[0] for name in names_raw if int(len(fa(check, str(name)))) > 0])

        """
        uses find_floats() to extract
        floating numbers from html string
        """
        self.from_cur = [self.find_floats(i) for i in from_cur_raw]
        self.to_cur = [self.find_floats(i) for i in to_cur_raw]

        # concatenate names, from-rate and to-rate, against 1 EUR, in a list
        self.rates = [n + f + t for n, f, t in zip(self.names, self.from_cur, self.to_cur)]

        # makes an alternative rates list with a timestamp
        rates_alt = {'timestamp': int(time()), 'rates': []}

        # the alt rates list uses abbreviations
        k = 0
        while k < len(self.rates):
            rates_alt['rates'].append({'currency': self.abb_names[k], 'from': self.rates[k][1], 'to': self.rates[k][2]})
            k += 1

        # data-source, displayed with output
        self.source = 'x-rates.com'

        # write it all to local file
        local_json = {'rates': self.rates, 'rates_alt': rates_alt, 'source': self.source}
        self.write_local(local_json)

        if not self.panda:
            return self.rates, rates_alt
        else:
            self.all_rates()

    def visit_ecb(self):
        """
        Scrapes ecb.europa.eu and extracts currency-rates against 1 EUR. 
        
        Then stores JSON file containing timestamp,
        the currencies and the respective rates.
        """
        try:
            request = get(URL_ALT)
            if request.status_code != 200:
                return False
        except:
            return False
        try:
            answer = html.fromstring(request.content)
        except NameError:
            print('\npip module \'lxml\' not installed\nor installed for the wrong Python version')
            exit()

        """
        I could not manage to get the respective 
        xpaths for names, cur_from and cur_to but I did 
        manage to get all of them in one big string. 

        Thus, raw_list contains each html-line 
        with type string as an item in a list. 
        """
        raw = answer.xpath(ALT_PATH)
        raw_list = [html.tostring(i) for i in raw]

        """
        This is all extractions from visit_xrates()
        basically cramped into a nested for loop.
        Extrats name and 1 EUR to that given name,
        then finds the inverse of that and appends all of it. 
        """
        rates = []
        for item in raw_list:
            for curenncy in CURRENCY:
                if int(len(fa(curenncy, str(item)))) > 0:
                    rates.append({'currency': ((([fa(curenncy, str(item))[0]])))[0], 'from': self.find_floats(item)[0], 'to': (1/float(self.find_floats(item)[0]))})

        # makes the alternative rates list with currency abbreviations
        rates_alt = []
        k = 0
        while k < len(rates):
            rates_alt.append((CURRENCY[rates[k]['currency']], rates[k]['from'], rates[k]['to']))
            k += 1

        """
        sort() returns TypeError on rates
        thus using the value for key 'currency' 
        in order to sort alphabetically
        """
        rates.sort(key=lambda value: value['currency'], reverse=False)
        rates_alt.sort()

        self.source = 'ecb.europa.eu'

        """
        adds timestamp to make sure the two scraping functions
        saves in the exact same structure for consistent extraction
        """
        local_json = {'rates': rates_alt, 'rates_alt': {'timestamp': int(time()), 'rates': rates}, 'source': self.source}

        # write it all to local file
        self.write_local(local_json)

        if not self.panda:
            return rates_alt, rates
        else:
            self.all_rates()

    def all_rates(self):
        """
        Display all rates, against 1 EUR, in a DataFrame.
        By default, all rates are made from a new query,
        thus the timestamp is always the current time.
        """
        try:
            import pandas as pd
        except ImportError:
            system('pip3 install pandas')

        try:
            self.panda_d = []
            i = 0
            while i < len(self.rates):
                self.panda_d.append(
                    (self.names[i][0], self.abb_names[i], 
                    round(float(self.from_cur[i][0]), 8), 
                    round(float(self.to_cur[i][0]), 8)))
                i += 1
        except:
            self.panda = True
            self.visit_xrates()

        df = pd.DataFrame(self.panda_d)
        df.rename(columns={0: 'Country', 1: 'Currency', 2: 'Rate From', 3: 'Rate To'}, inplace=True)

        print('\nSrc : %s\nBase: %s\nDate: %s UTC\n' 
            % (self.source, self.curFrom, strftime("%Y-%m-%d %H:%M:%S", gmtime())))

        print(df)

    def check_format(self):
        """
        Checks the user-input.

        If one or both of the inputs are not valid currencies,
        then return an error and exit.
        """
        match_f = 0
        match_t = 0

        for c in CURRENCY: 
            if str(c) == self.curFrom:
                match_f += 1
            if str(c) == self.curTo:
                match_t += 1
            else:
                continue

        if match_f + match_t == 2:
            return True

        else:

            if match_t != 1 and match_f == 1:
                print('Input Error. Currency \'%s\' cannot be found.\nTry again.' 
                    % self.curTo)
                return False

            elif match_f != 1 and match_t == 1:
                print('Input Error. Currency \'%s\' cannot be found.\nTry again.' 
                    % self.curFrom)
                return False

            elif match_t != 1 and match_f != 1:
                print('Input Error. Both currencies \'%s\' and \'%s\' cannot be found.\nTry again.' 
                    % (self.curTo, self.curFrom))
                return False
    
    def check_local(self):
        """
        Checks local JSON file. 

        If less than half-hour since last query,
        return the local JSON file rates.

        If more than half-hour since last query,
        return False so a new query can be made.
        """
        try:
            with open(MEM) as stored_json:
                stored = load(stored_json)
                str_stored = loads(stored)
            
            if abs(int(time()) - int(str_stored['rates_alt']['timestamp'])) > 1800:
                # if query has been stored for more than an half-hour, make a new query
                return False
            
            else:
                # if it's under half-hour, return the local result
                return str_stored['rates'], str_stored['rates_alt'], str_stored['source']
        except:
            return False

    def write_local(self, data):
        """
        Simply writes a local JSON file.
        """
        datan = dumps(data)
        with open(MEM, 'w') as stored_json:
            dump(datan, stored_json)

class ConCur(GetData):
    """
    Class for making the actual conversion 
    and formatting the result into a neat string. 
    """
    def __init__(self, curTo='usd', curFrom='eur', amount=1, panda=False):
        super().__init__(curTo, curFrom, amount, panda)
        
        try:
            self.get_data()
        except TypeError:
            """
            If -p all is used from CLI and a new query is made
            which is true by default, then it will return TypeError.
            This ignores that case. Nothing breaks. (at least thus far)
            """
            pass

        if not self.panda:
            self.convert_cur()

    def convert_cur(self):
        """
        Find the relation of both inputs to 1 EUR
        and multiply it by the amount. Default 1. 
        """
        data = self.get_user_input()
        try:
            f, k = data[0], data[1]
        except TypeError:
            f, k = self.get_user_input()[0], self.get_user_input()[1]

        if not self.curTo == 'EUR':
            self.conversion = ((float(k)/float(f)) * self.amount)
        if self.curTo == 'EUR':
            self.conversion = (float(k) * self.amount)

        # gets the saved timestamp in unix-time and converts to utc
        self.timestamp = datetime.utcfromtimestamp(self.rates_alt['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
       
    def np(self, n):
        """
        Reformats the conversion to 5 decimal places.
        """
        return '%s %s' % (round(n, 5), self.curTo)

    def get_user_input(self):
        """
        Get the specific rates from the user-inputs
        and return the appropiate results.
        """
        try:
            self.rates_alt['rates']
        except TypeError:
            self.rates_alt = self.check_local()[1]

        for i in self.rates_alt['rates']:
            if str(i['currency']) == str(self.curFrom):
                tmp_from = self.rates_alt['rates'].index(i)
                convert_from = i['from']
            if str(i['currency']) == str(self.curTo):
                convert_to = i['from']

        # conversion to euros
        if 'EUR' == self.curTo and not 'EUR' == self.curFrom:
            convert_to = self.rates_alt['rates'][tmp_from]['to']

        # conversion from euros to ... well ... euros
        if 'EUR' == self.curTo and 'EUR' == self.curFrom:
            convert_to = 1

        try:
            # default conversion
            if self.curFrom == 'EUR':
                return 1, convert_to
        except UnboundLocalError:
            """
            a valid input was entered but x-rates.com is
            likely not available and ecb does not support input
            """
            print('\necb.europa.eu has no rate for input currency %s' % self.curTo)
            from os import remove
            try:
                remove(MEM)
            except FileNotFoundError:
                pass
            exit()
        try:
            # return user inputs
            return convert_from, convert_to
        except UnboundLocalError:
            """
            a valid input was entered but x-rates.com is
            likely not available and ecb does not support input
            """
            print('\necb.europa.eu has no rate for input currency %s' % self.curTo)
            from os import remove
            try:
                remove(MEM)
            except FileNotFoundError:
                pass
            exit()

    def __repr__(self):
        """
        The final string containing the result.
        """
        return '\nConverting %s to %s\nRates from %s UTC\nSource: %s\n\n%s %s = %s' % (
                CURRENCY[str(self.curFrom)], 
                CURRENCY[str(self.curTo)],
                self.timestamp,
                self.source, 
                self.amount,
                self.curFrom, 
                self.np(self.conversion) 
                )

def test_concur(number=100):
    """
    Tests the conversion accuracy by testing against https://fixer.io API.
    Each conversion must have an accuracy of 99% or better in order to pass.

    The test itself is passed, if the avg accuracy of all conversions is above 99.8%.
    """
    try:
        from testapp.test_concur import ConvertCurrency
    except Exception:
        from PyConCur.testapp.test_concur import ConvertCurrency

    try:
        from numpy.random import randint
    except ImportError:
        system('pip3 install numpy')

    from time import sleep
    from os import remove

    cur_list = [i for i in CURRENCY]
    match = 0
    err = 0
    tests = 0
    margin = []
    err_msg = []
    print('''
Running %s conversions in total. 
Each conversion must score above 99%% accuracy in order to pass.
The test itself is passed, if the average accuracy of all conversions is above 99.8%%.''' 
        % number)
    while tests < number:
        cur_from = cur_list[randint(len(cur_list))]
        cur_to = cur_from
        while cur_to == cur_from:
            cur_to = cur_list[randint(len(cur_list))]
        
        amount = randint(10000)

        # run an instance of the conversion classes
        test_con = ConCur(curFrom=cur_from, curTo=cur_to, amount=amount)
        test_against = ConvertCurrency(curFrom=cur_from, curTo=cur_to, amount=amount)

        # get the actual conversion
        test_con_conversion = test_con.conversion
        test_against_conversion = test_against.conversion

        # find the error margin
        div = abs(test_con_conversion - test_against_conversion)
        avg = (test_con_conversion + test_against_conversion) / 2

        try:
            acc = 100 - ((div / avg) * 100)
        except ZeroDivisionError:
        
        # same currency being checked against
            
        #   div = 1 - 1       = 0           
        #   avg = (0 + 0) / 2 = 0
           
            acc = 100

        #print('\ncAm: %s\ncFr: %s\ncTo: %s\nPre: %s %s\nAct: %s %s\nAcc: %s%%' % (amount, CURRENCY[cur_from], CURRENCY[cur_to], test_con_conversion, cur_from, test_against_conversion, cur_to,  round(acc, 5)))

        if acc <= 99:
            err_msg.append('''
Test #{t} returned below or equal to 99% accuracy.

Conversion from {a} {f} to {to}.
Tried Conversion: {tc} {to}\nActual Conversion: {ta} {to}
Error Margin: {acc}%'''.format(
                t=(round(tests, 3)), 
                a=amount,
                f=cur_from,
                to=cur_to, 
                tc=round(test_con_conversion, 3),
                ta=round(test_against_conversion, 3),
                acc=round(acc, 2)))
            margin.append(acc)
            err += 1
            tests += 1
        if acc > 99:
            margin.append(acc)
            match += 1
            tests += 1

    total_avg = sum(margin) / len(margin)

    if total_avg > 99.8:
        print('\nRESULT: TEST PASSED')
        print('\nTEST SUMMARY:\nPassed: {p}\nFailed: {f}\nAvg Accuracy: {a}%\n\nTEST ERRORS:'.format(
            p=match, f=err, a=round(total_avg, 3)))
        [print(i) for i in err_msg]
        sleep(2)
        test_against.rev()
        remove(MEM)
    else:
        print('\nRESULT: TEST FAILED')
        print('\nTEST SUMMARY:\nPassed: {p}\nFailed: {f}\nAvg Accuracy: {a}%\n\nTEST ERRORS:'.format(
            p=match, f=err, a=round(total_avg, 3)))
        [print(i) for i in err_msg]
        sleep(2)
        test_against.rev()
        remove(MEM)

def main():
    """
    Parses input from terminal and returns appropiate result.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', 
        help='A = the amount to convert (default: -a 1).', type=float, default=1)

    parser.add_argument('-f', 
        help='F = the currency to convert from (default: -f EUR).', type=str, default='EUR')

    parser.add_argument('-t', 
        help='T = the currency to convert to (default: -t USD).', type=str, default='USD')

    parser.add_argument('-p', 
        help='Get all rates in relation to EUR in a dataframe. (usage: -p all)', type=str, default='off')

    parser.add_argument('-test', 
        help='Test conversion accuracy. Runs 100 tests. (usage: -test on)', type=str, default=False)

    args = parser.parse_args()
    
    if args.p == 'all' or args.p == 'ALL':
        ConCur(panda=True)
    elif args.test == 'on' or args.test == 'ON':
        test_concur()
    elif args.a == 1 and args.f == 'EUR' and args.t == 'USD':
        print(ConCur())
    else:
        print(ConCur(curFrom=str(args.f), curTo=str(args.t), amount=float(args.a)))

if __name__ == '__main__':
    main()