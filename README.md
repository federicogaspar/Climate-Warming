# Climate Warming
The idea of this project is to prove that climate change is not a scam.

I used regression analysis to model the climate of different areas in the United States in order to find evidence of global warming. The main goals were

- Create models to analyze and visualize climate change in terms of temperature, and then consider ways to make the data less noisy and obtain clearer temperature change trends. 
- Test the models to see how well historical data can predict future temperatures.
- Investigate a way to model the extremity of temperature, rather than just the increasing temperature.

## Dataset Information and atributtes
The dataset contains temperature data obtained from the National Centers for Environmental Information (NCEI). 
The data, stored in data.csv, contains the daily temperatures observed in 21 U.S. cities from 1961 to 2015.

- 0 Date (DD/MM/YYYY)
- 1 CITIES
- 2 TEMP ([°C])

## Data Analysis and Visualization.
#### Packages required: numpy, pandas, calendar, matplotlib and seaborn.

### <ins>Density plots.</ins>
First, I plotted the evolution of the temperature densities distribution for every city in the data base. There is a slight tendency in most of the cities to more compact shape in the recent years compared to a more sparse distribution in the first years recorded. This observation is align with the plot of the standard distribution below where I discussed the hypothesis that global warming makes temperatures more extreme. As far as I can analyze with this data, the yearly lowest temperature is hotter today than in the past, while the highest temperature remains almost constant across the years.

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/density_plot_eg.png" width="800">

### <ins>Calendar plots.</ins>


Here I plotted the temperature of each day in the calendar for the range of years given in the data set of every city.

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/ALBUQUERQUE-1961.jpg" width="1000">


<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/ALBUQUERQUE-2015.jpg" width="1000">


### <ins>Heatmap plots across the years.</ins>

Heatmap plot packs the whole data into a single plot. X – axis represents the year, while Y – axis represents the months. The color scale represent the mean temperature. We can  observe how since 1965 monthly mean temperature has been increasing. In fact, for 11/12 months 2015 had higher monthly mean temperatures compared to 1965. Again, the months with lower temperatures are more affected than the months with higher temperatures, indicating that lower temperatures are raising but higher temperatures remains almost constant along the years.


<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/heatmap.png" width="2000">



### <ins>Rollin average mean temperature.</ins>
 
 
Here, I plotted the 5 year rolling average of the yearly mean temperature as a function of the years for each city. First, the yearly mean temperature was computed. Then, I smoothed the plot by taking the moving average across the previous 5 years. Here the trend is evident. The mean temperature have raisened for all cities in at least 1°.
    
<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Mean%20Temperature%20Evolution%20ALB.jpg" width="800">


This plot is similar to the previous one but taking the average over cities. The conclusion is that mean temperature have raisened ~1.4°C in agreement with the literature.


<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Mean%20Temperature%20Evolution%20in%20USA.jpg" width="800">

### <ins>Daily temperature.</ins>

Here, the blue line represents the daily temperature for each month of a particular year in a given city. The orange line represents the historical daily mean temperature for the given city. The blue shadow represents the historical range between the minimal and maximal temperatures for a given day in the city. At last, the orange shadow represent the, standard deviation of the historical daily mean temperature for each day in a given city. 

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Monthly%20ALBL.jpg" width="800">

The gif pltted below is a representation of the evolution of the precious graph across the years.

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/ALBUQUERQUE.gif" width="800">


### <ins>TESTING AND ETC.</ins>

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Prediction.png" width="800">

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Training.png" width="800">

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Std.png" width="800">


