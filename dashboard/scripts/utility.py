import pandas as pd
import numpy as np
import random

def create_random_quartile(length):
    choices = ['1st-quartile', '2nd-quartile', '3rd-quartile', '4th-quartile']
    quartiles = [random.choice(choices) for _ in range(length)]
    return pd.Series(quartiles)


class Slice:
    def __init__(self, df, value_slice={}, range_slice={}):

        # Slice by values
        for key, value in value_slice.items():
            df = df[df[key] == value]

        # Slice by range
        for key, value in range_slice.items():
            if value[0] >= value[1]:
                print("ERROR: 1st element in range must be smaller than the 2nd element.")
                return    #This part should actually raise Exception to terminate
            df = df[(df[key] >= value[0]) & (df[key] <= value[1])]

        self.slice = df