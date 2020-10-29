import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import folium
from folium.plugins import HeatMap
from slice import *
import seaborn as sns

plt.style.use('ggplot')


def bar_graph(data, colors, size, title, xlabel, ylabel):

    fig, ax = plt.subplots(tight_layout=True, figsize=(12, 8))
    ax.bar(*zip(*data.items()), color=colors)
    ax.set_title(title, size=size)
    ax.set_xlabel(xlabel, size=size)
    ax.set_ylabel(ylabel, size=size)
    # location =
    # plt.savefig(location)
    plt.show()


def make_heat(name, df_x, df_y):
    heat_map = folium.FeatureGroup(name = name)
    max_amount = float(60)
    heat_map.add_child(HeatMap(list(zip(df_x, df_y)),
                       min_opacity=0.8,
                       max_val=max_amount,
                       radius=5.5, blur=1.5,
                       max_zoom=1,
                     ))
    return heat_map


def plot_human_factors_and_time(df, ax):
    y = incidents['hour']
    x = incidents['incident_type']

    sns.violinplot(x=y, y=x, data=incidents, ax=ax, bw=.1)
    ax.set_title('Hour of day vs Type of Call', fontsize=25)
    ax.set_ylabel('Type of Call', fontsize=22)
    ax.set_xlabel('Hour of day', fontsize=22)

    return ax


if __name__ == '__main__':
    df = pd.read_csv('smfr_2019.csv')

    night_lock_outs = get_night_calls(df)
    inc_type_d = get_types(df)
    type_dict_d = get_columns(df)
    property_use_d = get_place(night_lock_outs)
    incidents = get_incidents(df)
    lock_outs, night_lock_out = lockout(df, night_lock_outs)
    unintentional, unintentional_night = get_unintentional(df, night_lock_outs)
    malfunction, malfunction_night = get_malfunction(df, night_lock_outs)



    size = 22
    title = 'Distribution of the Top 9-11 Calls'
    xlabel = 'Type of Call'
    ylabel= 'Total number of calls'

    bar_graph(data=type_dict_d, colors=['b', 'b', 'r', 'b'], size=size, title=title,
              xlabel='Type of Call', ylabel=ylabel)
    bar_graph(data=inc_type_d, colors='r', size=size, title='All False Calls', xlabel=xlabel, ylabel=ylabel)
    bar_graph(data=property_use_d, colors='b', size=size, title='Location of Calls', xlabel='location', ylabel=ylabel)

    fig3, ax3 = plt.subplots(1, 1, figsize=(10, 10), tight_layout=True)
    plot_human_factors_and_time(incidents, ax3)
    plt.show()

    denver_map = folium.Map(location=[39.616890, -104.950508], zoom_start=11, tiles="Cartodbpositron")

    add_incidents = make_heat(name='All incidents',
                              df_x=incidents['x_trans'],
                              df_y=incidents['y_trans'])

    add_lockouts = make_heat(name='All Lockouts',
                             df_x=lock_outs['x_trans'],
                             df_y=lock_outs['y_trans'])

    add_lockouts_night = make_heat(name='Lockouts at night',
                                   df_x=night_lock_out['x_trans'],
                                   df_y=night_lock_out['y_trans'])

    add_smoke_dector = make_heat(name='743 unintentional smoke alarm',
                                 df_x=unintentional['x_trans'],
                                 df_y=unintentional['y_trans'])

    add_smoke_dector_night = make_heat(name='743 night call',
                                       df_x=unintentional_night['x_trans'],
                                       df_y=unintentional_night['y_trans'])

    add_malfunction = make_heat(name='733 smoke alaram malfunction',
                                df_x=malfunction['x_trans'],
                                df_y=malfunction['y_trans'])

    add_malfunction_night = make_heat(name='733 night call',
                                      df_x=malfunction_night['x_trans'],
                                      df_y=malfunction_night['y_trans'])

    denver_map.add_child(add_incidents)

    denver_map.add_child(add_lockouts)
    denver_map.add_child(add_lockouts_night)

    denver_map.add_child(add_smoke_dector)
    denver_map.add_child(add_smoke_dector_night)

    denver_map.add_child(add_malfunction)
    denver_map.add_child(add_malfunction_night)

    folium.LayerControl().add_to(denver_map)
    denver_map.save('denver_heatMapA.html')
