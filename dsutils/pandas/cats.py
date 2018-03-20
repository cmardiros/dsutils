import logging


def backup_categories(df, as_kind=None):
    """

    if as == list:
        return {'colA': ['level1', 'level2'...]}
    else:
        return {'colA': {0: 'level1', 1: 'level2', ...}}


    """

    as_kind = as_kind or 'list'
    df = remove_unused_cats(df)

    levels = dict()
    for col in df.columns:
        if df[col].dtype.name == 'category':
            if as_kind == 'list':
                levels[col] = list(df[col].cat.categories)
            elif as_kind == 'dict':
                levels[col] = dict(enumerate(df[col].cat.categories))

    return levels


def restore_categories(df, levels_dict):
    """
    Some transformation like concat or merge can destroy astype category.
    Sometimes it's useful to restore categories along with the levels that
    they had prior to that transformation.

    Parameters:

        levels_dict: dict, required
            {'colA': ['level1', 'level2'...],
             'colB': ['level1', 'level2'...]}

    """

    for col, levels in levels_dict.iteritems():

        if col in df.columns:
            # make sure the column is a category
            df[col] = df[col].astype('category')

            current_levels = list(df[col].cat.categories)

            # if current levels are fewer than new levels
            # keep only those which already exist but
            # use the order set by levels in levels_dict
            if len(current_levels) < len(levels):
                levels = [l for l in levels if l in current_levels]

            try:
                df[col] = df[col].cat.reorder_categories(levels)
            except Exception:
                sorted(current_levels)
                logging.debug("current_levels: {}".format(len(current_levels)))
                for l in current_levels:
                    logging.debug("l: {}".format(len(l)))

                sorted(levels)
                logging.debug("levels: {}".format(len(levels)))
                for l in levels:
                    logging.debug("l: {}".format(len(l)))

                raise

    return df


def make_categories(df,
                    cols,
                    precast=None,
                    levels_dict=None,
                    date_format=None):
    """
    Parameters:
        cols: list, required
            List of columns to cast to categories
        precast: str, optional
            If given, all columns will be cast as this type *first* before
            being cast to category.
        levels_dict: dict, optional
            If given, the levels for new categories will be overriden with this
    """

    levels_dict = levels_dict or dict()

    # {'what was passed': 'pandas equivalent'}
    precast_map = {
        'int': 'int',
        'date': 'datetime64[ns]'
    }

    fillna_map = {
        'int': 0,
    }

    df = df.copy()

    for col in cols:
        if col in df.columns:

            # cast to some dtype prior to converting to category
            if precast:

                try:
                    if fillna_map.get(precast):
                        df[col] = df[col].fillna(fillna_map.get(precast))

                    if precast_map.get(precast):
                        df[col] = df[col].precast(precast_map.get(precast))

                except Exception:
                    raise

                # extra step required for dates
                if precast == 'date':
                    df[col] = df[col].dt.date

            # finally, make as category
            df[col] = df[col].astype('category')

    if levels_dict:
        df = restore_categories(df, levels_dict=levels_dict)

    return df


def remove_unused_cats(df):
    df = df.copy()

    for col in df.columns:
        if df[col].dtype.name == 'category':
            df[col] = df[col].cat.remove_unused_categories()

    return df


def reorder_levels_by_estimate(df,
                               category,
                               measure,
                               estimator,
                               sort,
                               recast=False,
                               **kwargs):
    """
    Reorder category levels by an aggregation (typically count or sum) applied
    to it and return df with changed category levels.

    NOTES:
    This is sufficient for reordering categorical axis for Seaborn's factorplot
    even when there are multiple facets as this plot does not support
    different category level orders for different facets (TODO confirm if
    sharex=False) would do the trickself.


    If this is needed then it may make sense to display in different plots
    and run this function separately on different slices of the df.
    """

    kwargs = kwargs or dict()

    def _estimator(x):
        return estimator(x, **kwargs)

    ename = _estimator.__name__

    sort_dict = {
        'asc': True,
        'desc': False
    }

    sort = sort_dict.get(sort, False)

    # backup
    dfo = df.copy()

    # if the category isn't a pd categorical, make it so
    if recast and df[category].dtype.name != 'category':
        df[category] = df[category].astype('category')
        dfo[category] = dfo[category].astype('category')

    # create a groupby and pass it through estimator
    gb = df.groupby([category])

    reorder_by = kwargs.get('reorder_by')
    if reorder_by:
        del kwargs['reorder_by']
        agg = gb[reorder_by].agg([_estimator])
    else:
        agg = gb[measure].agg([_estimator])

    # sort by result of estimator
    agg = agg.sort_values(ename, ascending=sort)

    # get newly ordered levels
    new_levels = list(agg.index.values)

    # reorder category levels on original df
    dfo[category].cat.reorder_categories(new_levels, inplace=True)

    return dfo
