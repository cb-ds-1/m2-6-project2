import pandas as pd
import sys
"""
USAGE:

1) Download the following table
    - https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=1710000501 : be sure to use the "Download Entire table" option"
2) make sure you save it as 'canada-population.csv' file inside of the data folder
3) create actionable dataframe like so:

import pop as getpop

pop = getpop()

Returns
 ________________
| Year | Bracket |
__________________
|  String  | Float |
"""
def cleanup_pop(pop):
    pop = pop.rename(
        columns={
            'REF_DATE': 'Year',
            'VALUE': 'Value',
            'Age group': 'Groups',
        }
    )
    pop = pop.loc[
        (pop['Groups'] == 'All ages') 
        | (pop['Groups'] == '4 years') 
        | (pop['Groups'] == '5 years') 
        | (pop['Groups'] == '6 years') 
        | (pop['Groups'] == '7 years') 
        | (pop['Groups'] == '8 years') 
        | (pop['Groups'] == '9 years') 
        | (pop['Groups'] == '10 years') 
        | (pop['Groups'] == '11 years') 
        | (pop['Groups'] == '12 years')
    ]
    pop = pop.loc[(pop['GEO'] == 'Canada')]
    pop = pop.loc[(pop['Sex'] == 'Both sexes')]
    pop = pop.drop(['GEO', 'Sex', 'UOM'], axis=1)
    unique_groups = pop.Groups.unique()
    newpop = pd.DataFrame({
        "Year": pop.Year.unique()
    })
    for group in unique_groups:
        newpop = newpop.merge(
            pd.DataFrame({
                    group: list(pop[pop['Groups'] == group].Value)
                }),
            left_index=True,
            right_index=True,
            right_on=group
        )
    return newpop

def get_pop_df():
    cols_to_use = ['GEO', 'Age group', 'REF_DATE', 'VALUE', 'UOM', 'Sex']
    pop = pd.read_csv('data/canada-population.csv',usecols =cols_to_use)
    pop = cleanup_pop(pop)
    return pop

sys.modules[__name__] = get_pop_df