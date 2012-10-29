import os, sys


__version__ = '0.1'
__author__  = 'Samantha Quinones <ieatkillerbees@gmail.com'

__all__     = ['currency']

__currency_file__ = os.path.abspath(os.path.join(os.path.dirname(__file__),"../data/currency.dat")) 
__currency_data__ = None

#===============================================================================
# Exceptions
#===============================================================================
class DriverFileError(Exception): pass

def load_driver(currency_file=__currency_file__):
    import json
    try:
        with open(currency_file, "r") as drv:
            data = json.load(drv)
    except IOError:
        raise DriverFileError("Unable to read driver file. Please attempt to execute 'load_cdata.py' from the package root directory, or re-install pycash!")
    else:
        __currency_data__.update(data)

def set_driver(filename):
    if os.path.exists(filename) and os.access(filename, "r"):
        global __currency_file__; __currency_file__ = filename
        


from currency import Currency
