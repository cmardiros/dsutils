import numpy as np
import pandas as pd

"""
Simple estimators to apply to 1d arrays
"""


def distinct_count(data,
                   notnull=False):
    """
    Return distinct count of some 1-d data.


    Parameters:
        notnull: bool, optional
            If true, nulls are dropped before computing distinct count
    """

    # make a pd series as that can drop nulls in non-numeric arrays
    if not isinstance(data, pd.Series):
        data = pd.Series(data)

    if notnull:
        data = data[~data.isnull()]

    return data.unique().shape[0]
