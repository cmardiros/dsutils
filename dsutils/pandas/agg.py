import pandas as pd

from dask import delayed
import dask.threaded
import dask.multiprocessing

from dsutils.dask import utils as dask_utils


"""
Utilities for aggregation in Pandas.
"""


def groupby_parallel(df,
                     gb_keys,
                     agg_dict):
    """
    A parallel implementation of groupby. Useful when the cardinality of the
    groups is high.

    Returns: dataframe

    Example:

    gb = groupby_parallel(df=df,
                          gb_keys=['user_fk'],
                          agg_dict={'session_id': [distinct_count]})

    """

    tasks = list()

    gb = df.groupby(gb_keys)

    def _agg(group):
        gb = group.groupby(gb_keys).agg(agg_dict)
        # TODO: is it ok to hardcode this?
        gb.columns = ['_'.join(c) for c in gb.columns]
        gb.reset_index(inplace=True)

        return gb

    for name, group in gb:
        tasks.append(delayed(_agg)(group))

    with dask_utils.ProgressBar(identifier='groupby_parallel'):
        task_set = delayed(lambda x: x)(tasks)
        results = task_set.compute(get=dask.threaded.get)

    dfm = pd.concat(results)
    dfm.reset_index(drop=True, inplace=True)

    return dfm
