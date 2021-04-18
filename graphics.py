# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 11:09:09 2021

@author: Federico G Vega
"""

# Collaborators: Karina Canziani.

import main
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import seaborn as sns
import calendar
import datetime


weeks = [1, 2, 3, 4, 5, 6]
days = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']


def split_months(climate, city, year):
    """
    Take a df, slice by year, and produce a list of months,
    where each month is a 2D array in the shape of the calendar
    :param df: dataframe or series
    :return: matrix for daily values and numerals
    """
    df = climate.get_df()
    df = df[(df.index.year == year) & (df.CITY == city)]

    # Empty matrices
    a = np.empty((6, 7))
    a[:] = np.nan

    day_nums = {m: np.copy(a) for m in range(1, 13)}  # matrix for day numbers
    day_vals = {m: np.copy(a) for m in range(1, 13)}  # matrix for day values

    # Logic to shape datetimes to matrices in calendar layout
    for d in df.index:

        day = d.day
        month = d.month
        year = d.year
        col = d.dayofweek

        if d.is_month_start:
            row = 0

        day_nums[month][row, col] = day  # day number (0-31)
        day_vals[month][row, col] = df.loc[d].TEMP # day value (the heatmap data)

        if col == 6:
            row += 1

    return day_nums, day_vals


def create_year_calendar(climate, city, year):
    day_nums, day_vals = split_months(climate, city, year)
    temps = climate.filter_by(cities=[city]).values
    h_min, h_max = min(temps), max(temps) # min and max temp in historical data
    fig, ax = plt.subplots(3, 4, figsize=(14.85, 10.5), constrained_layout=True)

    for i, axs in enumerate(ax.flat):
        # heatmap
        im = axs.imshow(day_vals[i+1], cmap='jet', vmin=h_min, vmax=h_max)
        axs.set_title(month_names[i])

        # Labels
        axs.set_xticks(np.arange(len(days)))
        axs.set_xticklabels(days, fontsize=10, fontweight='bold', color='#555555')
        axs.set_yticklabels([])

        # Tick marks
        axs.tick_params(axis=u'both', which=u'both', length=0)
        axs.xaxis.tick_top()

        # Modify tick locations for proper grid placement
        axs.set_xticks(np.arange(-.5, 6, 1), minor=True)
        axs.set_yticks(np.arange(-.5, 5, 1), minor=True)
        axs.grid(which='minor', color='w', linestyle='-', linewidth=2.1)

        # Despine
        for edge in ['left', 'right', 'bottom', 'top']:
            axs.spines[edge].set_color('#FFFFFF')

        # Annotate
        for w in range(len(weeks)):
            for d in range(len(days)):
                day_val = day_vals[i+1][w, d]
                day_num = day_nums[i+1][w, d]

                # Value label
                axs.text(d, w+0.3, f"{day_val:0.0f}",
                         ha="center", va="center",
                         fontsize=7, color="w", alpha=0.8)

                # If value is 0, draw a grey patch
                if day_val == 0:
                    patch_coords = ((d - 0.5, w - 0.5),
                                    (d - 0.5, w + 0.5),
                                    (d + 0.5, w + 0.5),
                                    (d + 0.5, w - 0.5))

                    square = Polygon(patch_coords, fc='#DDDDDD')
                    axs.add_artist(square)

                # If day number is a valid calendar day, add an annotation
                if not np.isnan(day_num):
                    axs.text(d+0.45, w-0.31, f"{day_num:0.0f}",
                             ha="right", va="center",
                             fontsize=6, color="#003333", alpha=0.8)  # day

                # Aesthetic background for calendar day number
                patch_coords = ((d-0.1, w-0.5),
                                (d+0.5, w-0.5),
                                (d+0.5, w+0.1))

                triangle = Polygon(patch_coords, fc='w', alpha=0.7)
                axs.add_artist(triangle)

    # adding the color bar
    cb = fig.colorbar(im, ax=ax[-1, 1:3], shrink=0.6, location='bottom')
    cb.ax.set_xlabel(r'Temperature in °C', labelpad=-40, y=1.05)

    # Final adjustments
    fig.suptitle(r'$\bf{' + city + '}$' +'\n- '+str(year)+' -', fontsize=16)
    # plt.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.04)

    # Save to file
    plt.savefig('calendar_plots\\'+city+'\\'+city+str(year)+'.pdf')
    plt.clf()

# =============================================================================
# import os
# climate = main.Climate('data.csv')
# YEARS = climate.get_years()
# CITIES = climate.get_cities()
#
# for city in CITIES:
#     path = os.path.join('calendar_plots\\', city)
#     os.mkdir(path)
#
#     for year in YEARS:
#         create_year_calendar(climate, city, year)
# =============================================================================


def heat_map(climate, city):
    """
    Graph the monthly mean temperature for a given city as function of the
    years.

    Args:
        climate: climate object.
        city: city name in capital letters (str).

    Retunrs:
        A seaborn heatmap plot of the mean monthly temperature for each month
    for each year in the climate object.

    """
    # Size set up
    plt.rcParams['figure.figsize'] = (80.0, 15.0)
    plt.rcParams['font.family'] = "serif"

    # Prepearing the data frame.
    df = climate.get_df()
    mean_month = df.groupby(['YEAR','MONTH','CITY'])['TEMP'].agg(media='mean')
    mean_month.reset_index(inplace=True)
    df = mean_month[mean_month['CITY'] == city]
    df = pd.pivot_table(df, index='MONTH', values='media', columns='YEAR')
    lista = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Oct',
             'Nov', 'Dec']
    df = df.reindex(reversed(lista))

    # Plot configuration
    sns.set(font_scale=1.4)
    p = sns.heatmap(df, cmap='coolwarm', annot=True,
                    cbar_kws={"shrink": 0.8}, annot_kws={'size': 16})
    p.set_title(city, fontsize=50)
    fig = p.get_figure()
    fig.savefig('heatmaps\\'+city+'.pdf', bbox_inches='tight', pad_inches=0.3)
    fig.clf()

# =============================================================================
# CITIES = main.Climate('data.csv').get_cities()
# climate = main.Climate('data.csv')
# for city in CITIES:
#     heat_map(climate, city)
# =============================================================================


def graph_by_year(climate, city, year):
    """
    Graph the temperature as a function of the days of the given climate, city
    and year. It also plots the historical mean temperature within one standar
    deviation for each day and shadows the historical max and min temperature
    for each day.

    Args:
        climate: climate object.
        city: city name in capital letters (str).
        year: the year to get the data for (int).

    Retunrs:
        A seaborn lineplot of (14x6) inches of temperatures vs months.

    """

    temps = climate.filter_by(cities=[city])

    t_min_max = temps.groupby('{:%m-%d}'.format)
    t_min_max = t_min_max.agg(t_min='min', t_max='max', t_mean='mean', t_std='std')

    if not calendar.isleap(year):
        t_min_max = t_min_max.drop('02-29')

    temps = pd.DataFrame(temps[temps.index.year == year])
    t_min_max.reset_index(inplace=True), temps.reset_index(inplace=True)
    df = pd.concat([temps, t_min_max[['t_min', 't_max', 't_mean', 't_std']]],
                   axis=1)

    # Plot Labels
    label1 = '$\mu_H$'
    label2 = 'T'
    label3 = '$max_H - min_H$'
    label4 = '$\mu_H\pm\sigma_H$'
    # Set up the plots
    fig, ax = plt.subplots(figsize=(14, 6))
    ax = sns.lineplot(x='DATE', y='t_mean', data=df, color='sandybrown',
                      label=label1, linewidth=2.5)
    ax = sns.lineplot(x='DATE', y='TEMP', data=df, linewidth=2, label=label2)
    ax.fill_between(x='DATE', y1='t_max', y2='t_min', data=df, alpha=0.25,
                    label=label3)
    ax.fill_between(x=df.DATE, y1=(df.t_mean-df.t_std),
                    y2=(df.t_mean+df.t_std), label=label4, alpha=0.18)

    # Plot details
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=4)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=16)) # 16 is a slight approximation since months differ in number of days.
    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
    for tick in ax.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center')
    ax.set_xlim(datetime.date(year, 1, 1), datetime.date(year, 12, 31))
    ax.set_xlabel(None)
    ax.set_ylabel('Temperature (ºC)')

    ax.set_title('{} - {} - '.format(city, year))
    ax.grid(axis='x', c='gray', ls='--')
    path = 'yearly_temp_plots\\'+city+'\\'+city+str(year)+'.pdf'
    plt.savefig(path, bbox_inches = 'tight')
    fig.clf()


# =============================================================================
# import os
# climate = main.Climate('data.csv')
# YEARS = climate.get_years()
# CITIES = climate.get_cities()
#
# for city in CITIES:
#     path = os.path.join('yearly_temp_plots\\', city)
#     os.mkdir(path)
#     for year in YEARS:
#         graph_by_year(climate, city, year)
# =============================================================================

def graph_by_period(climate, cities, days, months, years, w_length=1, title=''):
    """
    Graph the average temperature as a function of the years of a list of
    cities, days and months.
    The average temperature is computed by taking the mean value across the
    cities for a given day and month, and then computing the mean value of the
    temperatures in the same period for each year.
    At last, we average this period temperature for a moving average of len
    w_length across the years.

    Args:
        climate: a climate object.
        city: a str or list of str of cities names in capital letters.
        days: int or list of ints the days
        months: int or list of ints the months
        w_length: compute the moving average of temperatures with
        specified window length of years.

    Retunrs:
        A seaborn lineplot of (14x6) inches of temperatures vs years.
    """
    # Handling different input types
    if isinstance(cities, str):
        cities = [cities]

    if isinstance(days, int):
        days = [days]

    if isinstance(months, int):
        months = [months]

    # Filtering the data frame by cities, months, days
    temps = climate.filter_by(cities=cities, days=days, months=months, years=years)

    # Mean value of cities temperatures remaining constant every day and month.
    temps = temps.groupby('{:%Y-%m-%d}'.format).mean()

    # Mean value of the period temperatures remaining constant every year.
    to_date = calendar.datetime.datetime.strptime
    temps.index = temps.index.map(lambda x: to_date(x, '%Y-%m-%d'))
    y = np.array([temps[temps.index.year == year].values.mean()
                      for year in years])

    # Computing the moving average and seting up the data frame.
    y = main.moving_average(y, w_length)
    df = pd.DataFrame({'YEAR': years, 'TEMP': y})

    # Minimal and Maximal temperatures after all the averages
    temp_min, temp_max = min(y)-0.2, max(y)+0.2

    fig, ax = plt.subplots(figsize=(14, 6))
    ax = sns.lineplot(x='YEAR', y='TEMP', data=df, linewidth=4)
    ax.fill_between(x='YEAR', y1=temp_min, y2=temp_max, data=df, alpha=0.25)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.4))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    ax.set_xlim(min(df.YEAR), max(df.YEAR))
    ax.set_ylim(temp_min, temp_max)
    ax.set_xlabel(None)
    ax.set_ylabel('Temperature (ºC)')
    ax.set_title(title, size=20)
    ax.grid(axis='x', c='gray', ls='--')


climate = main.Climate('data.csv')
# =============================================================================
# CITIES = climate.get_cities()
# title = 'Mean Temperature Evolution in USA'
# days = range(1,32)
# months = range(1,13)
# years = climate.get_years()
# graph_by_period(climate, CITIES, days=days, months=months, years=years ,
#                 w_length=5, title=title)
# plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
# =============================================================================

# =============================================================================
# CITIES = climate.get_cities()
# days = range(1,32)
# months = range(1,13)
# years = climate.get_years()
# for city in CITIES:
#     title = city
#     graph_by_period(climate, city, days=days, months=months, years=years ,
#                 w_length=5, title=title)
#     plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
#
# =============================================================================



def graph_std(climate, cities, w_length=1):
    """
    Plot the std for a given city across the years.

    Args:
        climate: a climate object.
        city: a str or list of str of cities names in capital letters.
        w_length: compute the moving average of temperatures with
        specified window length of years.

    Retunrs:
        A seaborn lineplot of (14x6) inches of std temperatures vs years.
    """
    years = climate.get_years()
    # Filtering the data frame by cities, months, days
    temps = climate.filter_by(cities=cities)

    # std value of the period temperatures remaining constant every year.
    y = np.array([temps[temps.index.year == year].values.min()
                      for year in years])
    z = np.array([temps[temps.index.year == year].values.max()
                      for year in years])

    # Computing the moving average and seting up the data frame.
    y = main.moving_average(y, w_length)
    z = main.moving_average(z, w_length)
    w = z - y
    df = pd.DataFrame({'YEAR': years, 'MIN': y, 'MAX': z, 'Delta': w})

    # Minimal and Maximal temperatures after all the averages
    temp_min, temp_max =-30, 52

    fig, ax = plt.subplots(figsize=(14, 6))
    ax = sns.lineplot(x='YEAR', y='MIN', data=df, linewidth=4)
    ax = sns.lineplot(x='YEAR', y='MAX', data=df, linewidth=4)
    ax.fill_between(x='YEAR', y1=temp_min, y2=temp_max, data=df, alpha=0.25)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    ax.set_xlim(min(df.YEAR), max(df.YEAR))
    ax.set_ylim(temp_min, temp_max)
    ax.set_xlabel(None)
    ax.set_ylabel('Temperature (ºC)')
    # ax.set_title(title, size=20)
    ax.grid(axis='x', c='gray', ls='--')

# graph_std(climate, ['SEATTLE'], w_length=5)

def graphdensity_bycity(climate, city, years):
    """
    Density plot for a given city across the years.

    Args:
        climate: a climate object.
        city: a str or list of str of cities names in capital letters.
        years: list of years (int)

    Retunrs:
        A seaborn ridge plot of (14x6) inches of std temperatures vs years.
    """

    if isinstance(city, str):
        city = [city]

    if isinstance(years, int):
        years = [years]

    temps = climate.filter_by(cities=city, years=years)
    y = temps.groupby('{:%Y-%m-%d}'.format).mean()
    to_date = calendar.datetime.datetime.strptime
    y.index = y.index.map(lambda x: to_date(x, '%Y-%m-%d'))
    df = pd.DataFrame(temps)
    df['YEAR'] = df.index.year

    # plot Set up
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

    # Initialize the FacetGrid object
    pal = sns.cubehelix_palette(len(years), rot=-.25, light=.7)

    g = sns.FacetGrid(df, row="YEAR", hue="YEAR", aspect=15, height=.5,
                      palette=pal)
    # Draw the densities in a few steps
    g.map(sns.kdeplot, "TEMP", bw_adjust=.5, clip_on=False, fill=True, alpha=1,
          linewidth=1.5)
    g.map(sns.kdeplot, "TEMP", clip_on=False, color="w", lw=2, bw_adjust=.5)
    g.map(plt.axhline, y=0, lw=2, clip_on=False)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)
    g.map(label, "TEMP")

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-.25)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)
    t_min, t_max = min(df.TEMP), max(df.TEMP)
    g.set(yticks=[], xlim=[t_min, t_max])
    g.set_xlabels('')
    g.fig.suptitle('Distribution of temperatures in ' + str(city[0]), size=14,
                   weight='bold', color='#45818e')
    plt.savefig(str(city[0]) + '.pdf')
    plt.clf()



# =============================================================================
# climate = main.Climate('data.csv')
# years= np.arange(1965, 2016, 5)
# CITIES= climate.get_cities()
# for city in CITIES:
#     graphdensity_bycity(climate, city, years)
# =============================================================================
