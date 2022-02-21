# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

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
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

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
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]


def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    estimated_error = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    standard_error = pylab.sqrt(estimated_error/(len(x)-2)/var_x)
    return standard_error/model[0]


"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    return_value = []
    for degree in degs:
        return_value.append(pylab.polyfit(x, y, degree))
    return return_value


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    res = ((y - estimated) ** 2).sum()
    total = ((y - pylab.average(y)) ** 2).sum()
    return 1 - (res / total)


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
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        global fig_num
        pylab.figure(fig_num)
        degree = len(model) - 1
        est_y = pylab.polyval(model, x)
        r_sq = round(r_squared(y, est_y), 4)
        pylab.plot(x, y, color='blue', marker='.', linestyle='-',
                   label='Measurements'
                   )
        pylab.plot(x, est_y, color='red', label='Model')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature (C)')
        if degree > 1:
            pylab.title(str(degree) + ' Degree Model with $R^2 =$ '
                        + str(r_sq)
                        )
        elif degree == 1:
            se = round(se_over_slope(x, y, est_y, model), 4)
            pylab.title('Linear  Model with $R^2 =$ ' + str(r_sq)
                        + '\n$SE/Slope =$ ' + str(se)
                        )
        pylab.legend()
        pylab.show()
        fig_num += 1


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    yearly_averages = pylab.array([])
    for year in years:
        cities_temps = pylab.array([])
        for city in multi_cities:
            city_temps = climate.get_yearly_temp(city, year)
            cities_temps = pylab.hstack((cities_temps, city_temps))
        yearly_avg = pylab.average(cities_temps)
        yearly_averages = pylab.hstack((yearly_averages, yearly_avg))
    return yearly_averages


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    return_value = []
    for i in range(1, len(y) + 1):
        if i < window_length:
            return_value.append(pylab.average(y[:i]))
        else:
            return_value.append(pylab.average(y[i - window_length:i]))
    return pylab.array(return_value)


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return pylab.sqrt(((y - estimated) ** 2).sum() / len(y))


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    std_dev = []
    for year in years:
        yearly_temps = None
        for city in multi_cities:
            if yearly_temps is None:
                yearly_temps = climate.get_yearly_temp(city, year)
            else:
                yearly_temp = climate.get_yearly_temp(city, year)
                yearly_temps = pylab.vstack((yearly_temps, yearly_temp))
        if yearly_temps.ndim > 1:
            yearly_temps = pylab.average(yearly_temps, axis=0)
        std_dev.append(pylab.std(yearly_temps))
    return pylab.array(std_dev)


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
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        pylab.figure(fig_num)
        degree = len(model) - 1
        estimate_y = pylab.polyval(model, x)
        model_rmse = round(rmse(y, estimate_y), 4)
        pylab.plot(x, y, color='blue', marker='.', linestyle='', label='Measurements')
        pylab.plot(x, estimate_y, color='red', label='Model')
        pylab.xlabel('Year')
        pylab.ylabel('Temperature (C)')
        if degree > 1:
            pylab.title(str(degree) + ' Degree Model with $RMSE =$ ' +
                        str(model_rmse)
                        )
        elif degree == 1:
            pylab.title('Linear  Model with $RMSE =$ ' + str(model_rmse))
        pylab.legend()
        pylab.show()
        fig_num += 1


if __name__ == '__main__':
    fig_num = 1
    climate = Climate('data.csv')
    pla_training_years = pylab.array(TRAINING_INTERVAL)
    pla_testing_years = pylab.array(TESTING_INTERVAL)

    # Part A.4 I
    temps = []
    for year in TRAINING_INTERVAL:
        temp = climate.get_daily_temp('NEW YORK', 1, 10, year)
        temps.append(temp)
    pla_temps = pylab.array(temps)
    models = generate_models(pla_training_years, pla_temps, [1])
    evaluate_models_on_training(pla_training_years, pla_temps, models)
    # Part A.4 II
    temps = []
    for year in TRAINING_INTERVAL:
        temp = pylab.average(climate.get_yearly_temp('NEW YORK', year))
        temps.append(temp)
    pla_temps = pylab.array(temps)
    nyc_avg_models = generate_models(pla_training_years, pla_temps, [1])
    evaluate_models_on_training(pla_training_years, pla_temps, nyc_avg_models)
