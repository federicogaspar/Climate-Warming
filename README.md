# Climate Warming
The idea of this project is to prove that climate change is not a scam.

I used regression analysis to model the climate of different areas in the United States in order to find evidence of global warming. The main goals were

- Create models to analyze and visualize climate change in terms of temperature, and then consider ways to make the data less noisy and obtain clearer temperature change trends. 
- Test the models to see how well historical data can predict future temperatures.
- Investigate a way to model the extremity of temperature, rather than just the increasing temperature.

## Dataset Information and Atributtes
The dataset contains temperature data obtained from the National Centers for Environmental Information (NCEI). 
The data, stored in data.csv, contains the daily temperatures observed in 21 U.S. cities from 1961 to 2015.

-  Date (DD/MM/YYYY)
-  CITIES (see above)
-  TEMP ([°C])

List of cities: ['BOSTON', 'SEATTLE', 'SAN DIEGO', 'PHILADELPHIA', 'PHOENIX', 'LAS VEGAS', 'CHARLOTTE', 'DALLAS', 'BALTIMORE', 'SAN JUAN', 'LOS ANGELES', 'MIAMI', 'NEW ORLEANS', 'ALBUQUERQUE', 'PORTLAND', 'SAN FRANCISCO', 'TAMPA', 'NEW YORK', 'DETROIT', 'ST LOUIS', 'CHICAGO']

## Data Analysis and Visualization.
#### Packages required: numpy, pandas, calendar, matplotlib and seaborn.

### <ins>Density plots.</ins>
First, I plotted the evolution of the temperature densities distribution for every city in the data base. There is a slight tendency in most of the cities to more compact shape in the recent years compared to a more sparse distribution in the first years recorded. This observation is align with the plot of the standard distribution below where I discussed the hypothesis that global warming makes temperatures more extreme. As far as I can analyze with this data, the yearly lowest temperature is hotter today than in the past, while the highest temperature remains almost constant across the years.

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/density_plot_eg.png" width="800">

### <ins>Calendar plots.</ins>


Here I plotted the temperature of each day in the calendar for the range of years given in the data set of every city.

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/ALBUQUERQUE-1961.jpg" width="800">


<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/ALBUQUERQUE-2015.jpg" width="800">


### <ins>Heatmap plots across the years.</ins>

Heatmap plot packs the whole data into a single plot. X – axis represents the year, while Y – axis represents the months. The color scale represent the mean temperature. We can  observe how since 1965 monthly mean temperature has been increasing. In fact, for 11/12 months 2015 had higher monthly mean temperatures compared to 1965. Again, the months with lower temperatures are more affected than the months with higher temperatures, indicating that lower temperatures are raising but higher temperatures remains almost constant along the years.


<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/heatmap.png" width="2000">



### <ins>Rollin average mean temperature.</ins>
 
 
Here, I plotted the 5 year rolling average of the yearly mean temperature as a function of the years for each city. First, the yearly mean temperature was computed. Then, I smoothed the plot by taking the moving average across the previous 5 years. Here the trend is evident. The mean temperature have raisened for all cities in at least 1°.
    
<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Mean%20Temperature%20Evolution%20ALB.jpg" width="800">


This plot is similar to the previous one but taking the average over cities. The conclusion is that mean temperature have raisened ~1.4°C in agreement with the literature.


<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Mean%20Temperature%20Evolution%20in%20USA.jpg" width="800">

### <ins>Daily temperature.</ins>

Here, the blue line represents the daily temperature for a given year and city. The orange line represents the historical daily mean temperature (the mean temperature for a particular day across the years) for the given city. The blue shadow represents the historical range between the minimal and maximal temperatures for a given day in the city. At last, the orange shadow represent the standard deviation of the historical daily mean temperature for each day in a given city. 

In this plot we observe from the blue shadow area that the dispersion of temperatures is greater in the low temperature region (from Octover to April included) than in summer.
<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Monthly%20ALBL.jpg" width="800">

The gif plotted below is a representation of the evolution of the precious graph across the years.

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/ALBUQUERQUE.gif" width="800">

## Linear Regression Model
### <ins>Trainning model.</ins>


We train a linear regression model from years in range 1961, 2010. We plotted above the 5 years moving average of the yearly mean temperature in USA (averaging over the cities).  We decided to evaluate how well the model performs by computing the model’s R^2 value, also known as its coefficient of determination. This value provides a measure of how well the total variation of samples is explained by the model. In this case we obtained a value of ~0.93. This shows that the fit the linear model succesfully explain the trend in the data.

We have alse included the ratio of the standard error of this fitted curve's slope to the slope. This ratio measures how likely it is that the trend in the data (upward/downward) and fitting curve just by chance. The larger the absolute value of this ratio is, the more likely it is that the trend is by chance. We obtained a value of 0.04.

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Training.png" width="800">

### <ins>Testing model.</ins> 
Now we have all the components we need to investigate the trend and cuantify the performance of the linear regression on test data, we are going to use our models to “predict the future”. We compared the model´s predictions to the real data from 2010-2015 (i.e. the TESTING_INTERVAL ) to simulate the future and we evaluated the model´s performance with Root Mean Square Error (RMSE), which measures the deviation of predicted values from true values. 

We can’t use R^2 here, since R^2 does not have a clear meaning on testing data -- R^2 measures how closely a model matches the data used to generate the model, but we are generating the model with 1961-2009 and testing on 2010-2015. We obtained a value for RMSE of 0.09.

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Prediction.png" width="800">

## Modeling Extreme Temperatures.

Our intuition predicted that in addition to raising temperature, global warming also makes temperatures more extreme (e.g., very hot or very cold). We surmise that we can model this effect by measuring the standard deviation in our data. A small standard deviation would suggest that the data is very close together around the mean. A larger standard deviation, however, would suggest that the data varies a lot (i.e., more extreme weather). Therefore, we expected that over time, the standard deviation should increase. On contrary we evidenced the oposite effect. This plot is in agreement with the previous plots. 

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Std.png" width="800">

## Conclusions
I investigated the global warming effect from a data set of the daily temperatures for 21 cities in the US. We observe a raise on the temperatures in the coolest range of the year. The US yearly mean temperature have raisened about 1.4°C. I also trainned a linear regression model to predict futures yearly mean temperatures. I tested the performance of the model in the range 2010-2015. Although the size of the data is small, the model matches the data. Finally, I explored the variance of the temperatures in data. There is no evidence that temperatures are getting more extreme, on the contrary, it seems that the the tendency is to a more compact uniform distribution. 


## Vega Federico Gaspar
