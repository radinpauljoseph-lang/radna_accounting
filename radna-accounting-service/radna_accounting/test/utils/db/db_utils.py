import pandas as pd

def convert_to_dict(data, column_names):
    new_data = []
    for row in data:
        temp = {}
        for index in range(len(row)):
            field = column_names[index]
            value = row[index]
            temp[field] = value
        new_data.append(temp)
    return new_data

def convert_to_df(data, column_names):
    return pd.DataFrame(data, columns=column_names)