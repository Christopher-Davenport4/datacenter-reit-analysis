
def transform(data, column):
    try:
        # The table intially started in a multilayered column format. The following code adjusts it to row format to match the format of the MYSQL databases
        raw_pivot = data.stack([0,1])
        raw_pivot = raw_pivot.unstack(1)
        raw_pivot = raw_pivot.reset_index([0,1])
        raw_pivot.columns.name = None

        #renaming the columns to match the sql schema
        raw_pivot = raw_pivot.rename(columns=column)
        raw_pivot["volume"] = raw_pivot["volume"].astype(int)

        # grouping by ticker so that the shift doesn't pull the previous ticker's last close
        # into the next ticker's first row
        raw_pivot['previous_return'] = raw_pivot.groupby('ticker')['adjusted_close'].shift(1)
        raw_pivot['daily_return'] = (raw_pivot['adjusted_close'] - raw_pivot['previous_return']) / raw_pivot['previous_return']
        raw_pivot = raw_pivot.drop(columns=['previous_return'])
        return raw_pivot
    except Exception as e:
        print(f"Error in transform function: {e}")
        return None