"""
Just having some fun in Python.
//christianlindeneg, June, 2019//
"""
# scraping URL
URL = 'http://www.x-rates.com/table/?from=EUR&amount=1'
URL_ALT = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'

# xpaths from DOM
NAME_PATH = '/html/body/div[2]/div/div[3]/div[1]/div/div[1]/div[1]/table[2]/tbody/tr/td[1]'
FROM_PATH = '/html/body/div[2]/div/div[3]/div[1]/div/div[1]/div[1]/table[2]/tbody/tr/td[2]'
TO_PATH = '/html/body/div[2]/div/div[3]/div[1]/div/div[1]/div[1]/table[2]/tbody/tr/td[3]'
ALT_PATH = '/html/body/div[1]/div[2]/div[2]/main/div[1]/table/tbody/tr'

# local json
MEM = 'stored_results.json'

# supported currencies thus far
CURRENCY = {
"ARS": "Argentine Peso",
"AUD": "Australian Dollar",
"BHD": "Bahraini Dinar",
"BWP": "Botswana Pula",
"BRL": "Brazilian Real",
"BND": "Bruneian Dollar",
"BGN": "Bulgarian Lev",
"CAD": "Canadian Dollar",
"CLP": "Chilean Peso",
"CNY": "Chinese Yuan Renminbi",
"COP": "Colombian Peso",
"HRK": "Croatian Kuna",
"CZK": "Czech Koruna",
"DKK": "Danish Krone",
"HKD": "Hong Kong Dollar",
"HUF": "Hungarian Forint",
"ISK": "Icelandic Krona",
"INR": "Indian Rupee",
"IDR": "Indonesian Rupiah",
"IRR": "Iranian Rial",
"ILS": "Israeli Shekel",
"JPY": "Japanese Yen",
"KZT": "Kazakhstani Tenge",
"KRW": "South Korean Won",
"KWD": "Kuwaiti Dinar",
"LYD": "Libyan Dinar",
"MYR": "Malaysian Ringgit",
"MUR": "Mauritian Rupee",
"MXN": "Mexican Peso",
"NPR": "Nepalese Rupee",
"NZD": "New Zealand Dollar",
"NOK": "Norwegian Krone",
"OMR": "Omani Rial",
"PKR": "Pakistani Rupee",
"PHP": "Philippine Peso",
"PLN": "Polish Zloty",
"QAR": "Qatari Riyal",
"RON": "Romanian New Leu",
"RUB": "Russian Ruble",
"SAR": "Saudi Arabian Riyal",
"SGD": "Singapore Dollar",
"ZAR": "South African Rand",
"LKR": "Sri Lankan Rupee",
"SEK": "Swedish Krona",
"CHF": "Swiss Franc",
"TWD": "Taiwan New Dollar",
"THB": "Thai Baht",
"TTD": "Trinidadian Dollar",
"TRY": "Turkish Lira",
"AED": "Emirati Dirham",
"GBP": "British Pound",
"USD": "US Dollar",
"VEF": "Venezuelan Bolivar",
"EUR": "Euro"
}
"""
ECB_SUPPORTED = {
    "AUD": "Australian dollar",
    "BGN": "Bulgarian lev",
    "BRL": "Brazilian real",
    "CAD": "Canadian dollar",
    "CHF": "Swiss franc",
    "CNY": "Chinese yuan renminbi",
    "CZK": "Czech koruna",
    "DKK": "Danish krone",
    "GBP": "Pound sterling",
    "HKD": "Hong Kong dollar",
    "HRK": "Croatian kuna",
    "HUF": "Hungarian forint",
    "IDR": "Indonesian rupiah",
    "ILS": "Israeli shekel",
    "INR": "Indian rupee",
    "ISK": "Icelandic krona",
    "JPY": "Japanese yen",
    "KRW": "South Korean won",
    "MXN": "Mexican peso",
    "MYR": "Malaysian ringgit",
    "NOK": "Norwegian krone",
    "NZD": "New Zealand dollar",
    "PHP": "Philippine peso",
    "PLN": "Polish zloty",
    "RON": "Romanian leu",
    "RUB": "Russian rouble",
    "SEK": "Swedish krona",
    "SGD": "Singapore dollar",
    "THB": "Thai baht",
    "TRY": "Turkish lira",
    "USD": "US dollar",
    "ZAR": "South African rand"
    "EUR": "Euro"
}
"""