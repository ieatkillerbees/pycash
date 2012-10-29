'''
Created on Oct 28, 2012

@author: samantha
'''

#===============================================================================
# Imports
#===============================================================================
from bs4 import BeautifulSoup
import argparse
import logging
import os
import pickle
import sys
import time
import urllib2
import json

#===============================================================================
# Global vars
#===============================================================================
__iso_curr_file__ = "http://www.currency-iso.org/dl_iso_table_a1.xml"
__currencies__    = None
__symbols__       = {"ALL": [76,101,107],"AFN": 1547,"ARS": 36,"AWG": 402,"AUD": 36,"AZN": [1084,1072,1085],"BSD": 36,"BBD": 36,"BYR": [112,46],"BZD": [66,90,36],"BMD": 36,"BOB": [36,98],"BAM": [75,77],"BWP": 80,"BGN": [1083, 1074],"BRL": [82,36],"BND": 46,"KHR": 6107,"CAD": 36,"KYD": 36,"CLP": 36,"CNY": 165,"COP": 36,"CRC": 8353,"HRK": [107,110],"CUP": 8369,"CZK": [75,269],"DKK": [107,114],"DOP": [82,68,36],"XCD": 36,"EGP": 163,"SVC": 36,"EEK": [107,114],"EUR": 8364,"FKP": 163,"FJD": 36,"GHC": 162,"GIP": 163,"GTQ": 81,"GGP": 164,"GYD": 36,"HNL": 76,"HKD": 36,"HUF": [70,116],"ISK": [107,114],"INR": 8377,"IDR": [52,70],"IRR": 65020,"IMP": 163,"ILS": 8362,"JMD": [74,36],"JPY": 165,"JEP": 163,"KZT": [1083,1074],"KPW": 8361,"KRW": 8361,"KGS": [1083,1074],"LAK": 8365,"LVL": [76,115],"LBP": 163,"LRD": 36,"LTL": [76,116],"MKD": [1076,1077,1085],"MYR": [82,77],"MUR": 8360,"MXN": 36,"MNT": 8366,"MZN": [77,84],"NAD": 36,"NPR": 8360,"ANG": 402,"NZD": 36,"NIO": [67,36],"NGN": 8358,"NOK": [107,114],"OMR": 65020,"PKR": 8360,"PAB": [66,47,46],"PYG": [71,115],"PEN": [83,47,46],"PHP": 8369,"PLN": [122,322],"QAR": 65020,"RON": [108,101,105],"RUB": [1088,1091,1073],"SHP": 163,"SAR": 65020,"RSD": [1044,1080,1085,46],"SCR": 8360,"SGD": 36,"SBD": 36,"SOS": 83,"ZAR": 82,"LKR": 8360,"SEK": [107,114],"CHF": [67,72,70],"SRD": 36,"SYP": 163,"TWD": [78,84,36],"THB": 3647,"TTD": [84,84,36],"TRL": 8378,"TVD": 36,"UAH": 8372,"GBP": 163,"USD": 36,"UYU": [36,85],"UZS": [1083,1074],"VEF": [66,115],"VND": 8363,"YER": 65020,"ZWD": [80,36]}


def get_symbol(code):
    '''
    Returns a unicode string representing a currency symbol, or the universal
    currency symbol if none is found.
    '''
    logger.debug(">>> Searching unicode symbol table for %s" % code)
    try:
        symbol = unichr(__symbols__[code])
        logger.debug(">>> Loaded symbol %s for %s" % (symbol, code))
    except KeyError:      # no symbol
        symbol = 164
        logger.debug(">>> No symbol for %s. Using default code 164." % code)
    except TypeError:          # symbol is not an int
        try:
            symbol = u''
            for char in __symbols__[code]:
                symbol = symbol + unichr(char)
            logger.debug(">>> Assembing multi-point symbol for %s." % code)
        except:
            print "Invalid symbol data found! Aborting."
            raise
    
    return symbol
    
def load_currencies(xml):
    '''
    Parses the data from the iso currency file to a dictionary.
    '''
    cdata = BeautifulSoup(xml, "xml")
    cdict = {}
    for currency in cdata.ISO_CCY_CODES.find_all("ISO_CURRENCY"):
        alpha_code = currency.find("ALPHABETIC_CODE").string
        digit_code = currency.find("NUMERIC_CODE").string or None

        logger.debug(">>> Processing currency %s(%s)" % (alpha_code, digit_code))
        
        cdict[alpha_code] = dict(
           alpha_code = unicode(alpha_code),
           digit_code = int(digit_code) if digit_code != "Nil" and digit_code != None else -1,
           name       = unicode(currency.find("CURRENCY").string),
           entity     = unicode(currency.find("ENTITY").string.title()),
           symbol     = unicode(get_symbol(alpha_code)))
    return cdict

def get_curr_file():
    '''
    Gets the iso currency file from the internets.
    '''
    logger.debug(">>> Requesting currency definition file from %s" % __iso_curr_file__)
    return urllib2.urlopen(__iso_curr_file__).read()


if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser("Create a new currecy driver for pycash")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("outfile", action="store", nargs="?", help="Output file", default="data/currency.dat")
    args = parser.parse_args()

    logger = logging.getLogger()
    logging.basicConfig(format="%(message)s")
    logger.setLevel("DEBUG") if args.verbose else logger.setLevel("INFO")

    logger.info("Retrieving currency data...")
    __currencies__ = load_currencies(get_curr_file())
    
    print "Building data file..."
    try:
        with open(args.outfile, "w+") as o_file:
            json.dump(__currencies__, o_file)
#            for code, currency in __currencies__.iteritems():
#                o_file.write(pickle.dumps(currency, protocol=pickle.HIGHEST_PROTOCOL)+"\r\n")
    except IOError:
        print "Unable to open output file."
    else:
        print "Driver written as %s" % os.path.abspath(args.outfile)

    logger.info("Processed %d currencies in %s seconds." % (len(__currencies__.keys()), time.time() - start_time))