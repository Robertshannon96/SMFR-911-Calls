import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from slices import get_columns, get_types, get_night_calls, get_place
plt.style.use('ggplot')


def bar_graph(data, colors, size, title, xlable, ylable):

    fig, ax = plt.subplots(tight_layout=True, figsize=(12, 8))
    ax.bar(*zip(*data.items()), color=colors)
    ax.set_title(title, size=size)
    ax.set_xlabel(xlable, size=size)
    ax.set_ylabel(ylable, size=size)
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('data/smfr_2019.csv')

    night_lock_outs_df = get_night_calls(df)
    inc_type_d = get_types(df)
    type_dict_d = get_columns(df)
    property_use_d = get_place(night_lock_outs_df)

    size = 22
    title = 'Distribution of all False Calls'
    xlable = 'Type of Call'
    ylable= 'Total number of calls'

    bar_graph(data=type_dict_d, colors=['b', 'b', 'b', 'r'], size=size, title=title,
              xlable='Type of Call', ylable='ylabel')

    bar_graph(data=inc_type_d, colors='b', size=size, title=title, xlable=xlable, ylable=ylable)

    bar_graph(data=property_use_d, colors='b', size=size, title='Location of Calls', xlable='location', ylable=ylable)



