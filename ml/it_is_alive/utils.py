
def normalise(df, n, max_):
    '''
    function for normalise data_frame
    '''
    new_df = pd.DataFrame(df['begin'])
    new_df['close'] = df['close'] / max_
    for i in range(1, n + 1):
      new_df[f'close{i}'] = df[f'close{i}'] / max_
    return new_df

def reshaper(df, n):
    for i in range(1,n+1):
        df[f'close{i}'] = pd.Series([0]*i).append(df['close'], ignore_index=True)[:-i] # Он убирает последние i элементов, заменяя их нулями
    return df[n:]