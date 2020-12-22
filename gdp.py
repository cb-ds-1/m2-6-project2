import pandas as pd
import numpy as np
import sys
"""
USAGE:

1) Download the following table
    - https://www150.statcan.gc.ca/t1/tbl1/en/cv!recreate.action?pid=3610043401&selectedNodeIds=2D1,3D1,4D16,4D17,4D19,4D20,4D21,4D22,4D23,4D24,4D25,4D26,4D27,4D28,4D31,4D44,4D45,4D46,4D47,4D48,4D49,4D50,4D51,4D52,4D53,4D54,4D55,4D65,4D70,4D73,4D77,4D80,4D81,4D84,4D92,4D95,4D98,4D104,4D113,4D121,4D127,4D132,4D142,4D146,4D160,4D161,4D162,4D163,4D164,4D165,4D166,4D167,4D168,4D169,4D170,4D171,4D189,4D198,4D199,4D206,4D209,4D274,4D276,4D277,4D287&checkedLevels=0D1&refPeriods=19970501,20201101&dimensionLayouts=layout2,layout2,layout2,layout3,layout2&vectorDisplay=false
    : be sure to use the "Download Entire table" option"
2) make sure you save it as 'gdp-canada.csv' file inside of the data folder
3) create actionable dataframe like so:

import gdp as getgdp

gdp = getgdp()

NB: all values are in millions

getgdp takes in 1 optional argument, if you specify one, it must be a potential NAICS industry name (not including it's classification code)
if no option is provided, a dict is returned with all Industries read in the file as keys, whose values are DataFrame objects of their 
Period and Values.

Key: Industry
Value:
 ________________
| Period | Value |
__________________
|  Date  | Float |
"""

def unique_cols(gdp):
    uniques = gdp['Class'].unique()
    return uniques

def cleanup_gdp(gdp):
    gdp = gdp.rename(columns={'North American Industry Classification System (NAICS)': 'Class',
                             'REF_DATE': 'Period',
                             'VALUE': 'Value',
                             'Seasonal adjustment': 'Adj'})
    gdp['Period'] = pd.to_datetime(gdp['Period'])
    gdp = gdp[gdp.Adj == 'Seasonally adjusted at annual rates']
    gdp = gdp[gdp.Prices == '2012 constant prices']
    gdp = gdp.drop(columns=['Adj', 'Prices'])
    gdp['Class'] = gdp['Class'].map(lambda x: " ".join(x.split(" ")[:-1]))
    def cleanup(gdp):
        gdp = gdp.drop(columns=['Class'])
        return gdp
    frames = {industry: cleanup(gdp[gdp['Class'] == industry]) for industry in gdp['Class'].unique()}
    return frames

def get_gdp_df(for_ind=None):
    cols_to_use = ['North American Industry Classification System (NAICS)', 'REF_DATE', 'VALUE', 'Seasonal adjustment', 'Prices']
    gdp = pd.read_csv('data/gdp-canada.csv',usecols =cols_to_use)
    gdp = cleanup_gdp(gdp)
    return gdp if for_ind == None else gdp[for_ind]


sys.modules[__name__] = get_gdp_df