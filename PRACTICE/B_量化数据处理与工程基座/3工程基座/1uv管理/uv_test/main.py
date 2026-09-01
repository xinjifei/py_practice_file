import pandas as pd
import pandas_ta_classic as ta

source_list = my_list = [
    {'close': 100.2},
    {'close': 101.5},
    {'close': 100.8},
    {'close': 99.4},
    {'close': 98.6},
    {'close': 99.9},
    {'close': 101.2},
    {'close': 102.5},
    {'close': 103.1},
    {'close': 102.7},
    {'close': 103.9},
    {'close': 105.2},
    {'close': 104.8},
    {'close': 103.5},
    {'close': 102.1},
    {'close': 101.8},
    {'close': 100.5},
    {'close': 99.7},
    {'close': 98.9},
    {'close': 99.3},
    {'close': 100.6},
    {'close': 101.9},
    {'close': 102.3},
    {'close': 103.7},
    {'close': 104.1},
    {'close': 105.6},
    {'close': 106.2},
    {'close': 105.8},
    {'close': 104.5},
    {'close': 103.8}
]

df = pd.DataFrame(source_list)
print(df[["close"]].head(20))
print("test_1")
