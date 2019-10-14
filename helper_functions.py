import pandas as pd
import numpy as np
import warnings


def df_preview(df: pd.DataFrame, n_samples: int = 2):
    d = {'col_name' : [],
         'Num Nulls' : [],
         'Type' : [],
         'Num Unique' : [],
         'Sample Values' : []}
    for col_name in df.columns:
        col = df[col_name]
        d['col_name'].append(col_name)
        d['Num Nulls'].append(col.isna().sum())
        d['Type'].append(col.dtypes)
        d['Num Unique'].append(col.unique().shape[0])
        d['Sample Values'].append(col.values[:n_samples])
    print('Shape: ', df.shape)
    return pd.DataFrame(d)


def rename_col(df: pd.DataFrame, old_name: str, new_name: str):
    new_columns = df.columns.values
    col_ind = list(new_columns).index(old_name)
    new_columns[col_ind] = new_name
    df.columns = new_columns
    return df


def columns_mismatch(df: pd.DataFrame, col_name_1: str, col_name_2: str):
    set_unique1 = set(df[col_name_1].unique())
    set_unique2 = set(df[col_name_2].unique())
    difference = set_unique1 - set_unique2
    print('There are {} unique elements in Column_1'.format(len(set_unique1)))
    print('There are {} unique elements in Column_2\n'.format(len(set_unique2)))
    print('There are {} values that are present in Column_1, '
          'but not present in Column_2:\n\n{}'.format(len(difference), difference))
    return difference


def df_difference(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    assert df1.shape[1] == df2.shape[1], 'DataFrames have different number of columns'
    assert (df1.dtypes.values == df2.dtypes.values).all(), 'Columns type mismatch'
    col_names = ['df1_' + i + '_df2_' + j for i, j in zip(df1, df2)]
    df1.columns = col_names
    df2.columns = col_names
    return pd.concat([df2, df1, df1], sort=False).drop_duplicates(keep=False)


def verify_dates_integity(df: pd.DataFrame, date_col: str) -> None:
    dates = pd.to_datetime(df[date_col])
    date_start = df[date_col].min()
    date_end = df[date_col].max()
    date_range = pd.date_range(start=date_start, end=date_end, freq='D')
    print('Start Date: {}; End Date: {}, Range Length: {}'.format(date_start, date_end, len(date_range)))
    num_missing_dates = ~np.isin(date_range, dates)
    print('Number of missing dates: {}'.format(sum(num_missing_dates)))
    if sum(num_missing_dates) > 0:
        print('Missing dates: {}'.format(date_range[~np.isin(date_range, dates)]))


def duplicate(df: pd.DataFrame, how: str, n_times: int) -> pd.DataFrame:
    if how == 'whole':
        return pd.DataFrame(np.tile(df.values.T, n_times).T, columns=df.columns)
    elif how == 'element_wise':
        return pd.DataFrame(np.repeat(df.values, n_times, axis=0), columns=df.columns)


def groupby_to_list(df: pd.DataFrame, by_cols, col_to_list: str) -> pd.DataFrame:
    groupped = df.groupby(by_cols)
    return groupped[col_to_list].apply(list).reset_index()


def chunkenize(data_to_split, num_chunks, df_indices=[], copy=True):
    """
    :param data: list or pd.DataFrame
    :param num_chunks: int
    :param df_indices: can be provided if type(data)==pd.DataFrame
    :param copy: Boolean, defines whether the copy of data is created, so that the data in outer scope is not affected
    :return: list of objects with the same type as data
    """
    if copy:
        data = data_to_split.copy()
    else:
        data = data_to_split

    data_length = len(data)
    chunk_length = data_length // num_chunks

    if chunk_length * num_chunks < data_length:
        chunk_length += 1

    print('Splitting data into {} chunks with length {} (last chunk can be smaller)'.format(num_chunks, chunk_length))

    if isinstance(data_to_split, list):
        chunks = [data[i:i + chunk_length] for i in range(0, data_length, chunk_length)]
    elif isinstance(data_to_split, pd.DataFrame):
        if len(df_indices) > 0:
            columns = data.columns
            data.set_index(df_indices, inplace=True)
        chunks = [data[i:i + chunk_length] for i in range(0, data_length, chunk_length)]
        if len(df_indices) > 0:
            chunks = [chunk.reset_index()[columns] for chunk in chunks]
    else:
        warnings.warn("Incorrect type: data should be either list or Pandas DataFrame")
        chunks = 0

    return chunks
