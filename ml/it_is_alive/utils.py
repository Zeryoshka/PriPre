import pandas as pd

def normalise(df, n, max_):
    '''
    function for normalise data_frame
    '''
    new_df = pd.DataFrame()
    if 'begin' in df:
        new_df['begin'] = df['begin']
    if 'close' in df:
        new_df['close'] = df['close'] / max_
    for i in range(1, n + 1):
      new_df[f'close{i}'] = df[f'close{i}'] / max_
    return new_df

def predict_reshaper(df, n):
    '''
    function for reshape predict df in line
    '''
    new_df = pd.DataFrame()
    for i, n in enumerate(df['close'].loc[-n:], 1):
        new_df[f'close{i}'] = n
    return new_df

def reshaper(df, n):
    '''
    function for reshape test df
    '''
    new_df = pd.DataFrame(df, )
    for i in range(1,n + 1):
        # Он убирает последние i элементов, заменяя их нулями
        new_df[f'close{i}'] = pd.Series([0]*i).append(
                df['close'],
                ignore_index=True
            )[:-i]
    return new_df[n:]