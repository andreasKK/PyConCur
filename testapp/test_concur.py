#!bin/usr/python
"""
Just having some fun in Python.
//christianlindeneg, June, 2019//

Uses https://fixer.io API to get 'real' convertion data to check against
"""
from requests import get
from json import load, loads, dump, dumps
from os import remove
# This key is only for testing. Feel free to use it.
# However, you can get your own right here:
# https://fixer.io/product
DATAFIX = '1b04e58170154a44b44aca606f5704d9'
MEM = 'stored_results_test.json'
URL = 'http://data.fixer.io/api/latest?access_key=%s' % (DATAFIX)

class ConvertCurrency:
    # Simple Currency Converter
    def __init__(self, curFrom='eur', curTo='usd', amount=1):
        self.curFrom = curFrom.upper()
        self.curTo = curTo.upper()
        self.amount = amount
        self.convert_currency()

    def convert_currency(self):
        # get rates, find relationship, convert 
        data = self.get_rates()
        cfrom, cto = data[0], data[1]

        self.conversion = (float(cto) / float(cfrom)) * self.amount

    def get_rates(self):
        # checks local function
        # if false, query API
        # return the result 
        answer = self.check_local()
        if not answer:
            # if not true, query api
            try:
                query = get(URL).json()

                if query['success'] == True:
                    # write local json
                    self.write_local(query)
                    self.query_result = query['rates']
                    return  self.query_result[self.curFrom], self.query_result[self.curTo]
                
                else:
                    print('\nQuery Denied. Check API Key.')
                    exit()
            
            except Exception as e:
                print(e)
                exit()

        elif answer:
            # if true, return local storage
            self.query_result = answer['rates']
            return answer['rates'][self.curFrom], answer['rates'][self.curTo]
       
        else:
            print('\nAn error occured')
            exit()
            
    def check_local(self):
        # checks local storage
        # if more than one hour old
        # delete and make a new request
        try:
            with open(MEM) as stored_json:
                stored = load(stored_json)
                str_stored = loads(stored)
                return str_stored
        except:
            return False

    def write_local(self, data):
        # writes local json
        datan = dumps(data)
        with open(MEM, 'w') as stored_json:
            dump(datan, stored_json)

    def rev(self):
        return remove(MEM)

