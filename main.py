# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 19:24:08 2021

@author: Federico G Vega
"""

# -*- coding: utf-8 -*-
# Project
# Name: Global Warning Project
# Goals: Prove global warning is not a scam

import pandas as pd
import calendar
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename in a data frame.

        Args:
            filename: name of the csv file (str)
        """

        self.df = pd.read_csv(filename)
        self.df['DATE'] = pd.to_datetime(self.df['DATE'], format='%Y%m%d')
        self.df = self.df.set_index('DATE')
        self.df['YEAR'] = self.df.index.year
        self.df['MONTH'] = self.df.index.month.map(dict(enumerate(calendar.month_abbr)))
        self.df['DAY'] = self.df.index.day
        self.clean_data()

    def clean_data(self):
        # There was an error in the data stored in PHOENIX (-483°C 14-09-1964)
        self.df.loc[self.df.TEMP < -30, 'TEMP'] = 27

    def get_df(self):
        return self.df

    def get_cities(self):
        """
        Get the name of the cities recorded in the data frame.

        Return:
            list of string of the names of the cities.
        """
        return list(set(self.df['CITY']))

    def get_years(self):
        """
        Get the years column as a list.

        Args:
            city: city name (str)

        Return:
            list of string of ints for the years recorded.
        """

        return list(set(self.df['YEAR']))

    def filter_by(self, **kwargs):
        """
        Filter the climate date frame temperatures for the given list of years,
        cities, months or days.

        Args:
            cities: list of city names (str)
            years: list of the years to get the data for (int)
            months: list of the months to get the data for (int)
            days: list of the days to get the data for (int)

        Returns:
            a temporal series of temperatures for the specified parameters.
        """
        df = self.df
        for key, values in kwargs.items():
            if key == 'cities':
                assert set(values).issubset(self.get_cities()), "provided city is not available"
                df = df[df['CITY'].isin(values)]
            elif key == 'years':
                assert set(values).issubset(self.get_years()), "provided year is not available"
                df = df[df['YEAR'].isin(values)]
            elif key == 'months':
                df = df[df.index.month.isin(values)]
            elif key == 'days':
                df = df[df.index.day.isin(values)]
        return df['TEMP']

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d numpy array of daily temperatures for the specified year and
            city
        """

        return self.filter_by(cities=[city], years=[year]).values

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        date = calendar.datetime.date(year, month, day)
        assert city in self.get_cities(), "provided city is not available"
        assert date in self.df[self.df['CITY'] == city].index, "provided date is not available in the city"

        return self.df[self.df['CITY'] == city].loc[date].TEMP


def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: an 1-d np array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d np array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d np array of values estimated by a linear
            regression model
        model: a np array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = np.sum((estimated - y)**2)
    var_x = np.sum((x - x.mean())**2)
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d np array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d np array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of np arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    return [np.polyfit(x,y,deg) for deg in degs]


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.

    Args:
        y: 1-d np array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d np array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    mean = np.mean(y)
    return 1-sum((y-estimated)**2)/sum((y-mean)**2)

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope).

    Args:
        x: an 1-d np array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d np array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a np array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    fig, ax = plt.subplots(facecolor='#eeeeee')
    for coefficients in models:
        plt.plot(x, y, 'bo', label='Training Data')
        degree = len(coefficients) - 1
        estimated = np.polyval(coefficients, x)
        r_sq_error = r_squared(y, estimated)
        title = ''
        if degree == 1:
            se = se_over_slope(x, y, estimated, coefficients)
            title = 'Linear fit with '
            label2 = 'SE = '+str(round(se, 2))

        elif degree == 2:
            title = 'Cuadaratic fit with '
            label2 = 'Cuadratic model'
        else:
            label2 = ''
        title += r'$R^2 = $' + str(round(r_sq_error, 3))
        plt.plot(x, estimated, 'r', label=label2)

        plt.title(title, size=18, family='fantasy', fontweight="normal")
        plt.legend(loc='upper left', bbox_to_anchor=(1, 0.7),
           fancybox=True, shadow=True, ncol=1)
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.tick_params(axis='both', which='minor', labelsize=8)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))

        plt.xlabel('Years', size=16, weight='normal', color='black')
        plt.ylabel('Temperature [°C]', size=16, weight='normal', color='black')
        plt.show()

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a numpy 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    df = climate.filter_by(cities=multi_cities, years=years)
    return df.groupby('{:%Y}'.format).mean().values

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d np array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d numpy array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    n = window_length
    init_sum = [sum(y[:i+1])/(i+1) for i in range(n-1)]
    final_sum = [sum(y[i:i+n])/n for i in range(len(y)-n+1)]
    return np.array(init_sum + final_sum)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d np array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return np.sqrt(sum((y-estimated)**2)/len(y))


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a np 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual
        city temperatures for the given cities in a given year.
    """

    to_date = calendar.datetime.datetime.strptime
    df = climate.filter_by(cities=multi_cities, years=years)
    df = df.groupby('{:%Y-%m-%d}'.format).mean()
    df.index = df.index.map(lambda x: to_date(x, '%Y-%m-%d' ))

    return np.array([df[df.index.year == year].values.std() for year in years])


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    Args:
        x: an 1-d np array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d np array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a np array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    fig, ax = plt.subplots(facecolor='#eeeeee')
    for coefficients in models:
        plt.plot(x, y, 'bo', label='Testing Data')
        degree = len(coefficients) - 1
        estimated = np.polyval(coefficients, x)
        root_meam_sq_err = rmse(y, estimated)
        title = 'Prediction - '
        if degree == 1:
            title += 'Linear model -'
        elif degree == 2:
            title += 'Cuadaratic model -'

        label = r'$rmse = $' + str(round(root_meam_sq_err,2))
        plt.plot(x, estimated, 'r', label=label)
        plt.title(title, size=18, family='fantasy', fontweight="normal")
        plt.legend(loc='upper left', bbox_to_anchor=(1, 0.7),
           fancybox=True, shadow=True, ncol=1)
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.tick_params(axis='both', which='minor', labelsize=8)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))

        plt.xlabel('Years', size=16, weight='normal', color='black')
        plt.ylabel('Temperature [°C]', size=16, weight='normal', color='black')
        plt.show()


if __name__ == '__main__':

    climate = Climate('data.csv')
    sns.set_theme(style='darkgrid')
    TRAINING_INTERVAL = np.array(range(1961, 2010))
    TESTING_INTERVAL = np.array(range(2010, 2016))
    CITIES = climate.get_cities()

    # Part A
    national_yearly_temp = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    moving_avg_temp = moving_average(national_yearly_temp, window_length=5)
    model = generate_models(TRAINING_INTERVAL, moving_avg_temp, [1])
    evaluate_models_on_training(TRAINING_INTERVAL, moving_avg_temp, model)


    # Part B
    national_yearly_temp = gen_cities_avg(climate, CITIES, TESTING_INTERVAL)
    moving_avg_temp = moving_average(national_yearly_temp, window_length=5)
    evaluate_models_on_testing(TESTING_INTERVAL, moving_avg_temp, model)

    # Part C
    std_devs = gen_std_devs(climate, CITIES, TRAINING_INTERVAL)
    moving_aver = moving_average(std_devs, window_length=5)
    model = generate_models(TRAINING_INTERVAL, moving_aver, [1])
    evaluate_models_on_training(TRAINING_INTERVAL, moving_aver, model)

