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

### <ins>Density plots across the years.</ins>
First, I plotted the evolution of the temperature densities distribution for every city in the data base. There is a slight tendency in most of the cities to more compact shape in the recent years compared to a more sparse distribution in the first years recorded. This observation is align with the plot of the standard distribution below where I discussed the hypothesis that global warming makes temperatures more extreme. As far as I can analyze with this data, the yearly lowest temperature is hotter today than in the past, while the highest temperature remains almost constant across the years.

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/density_plot_eg.png" width="800">

### <ins>Calendar plots.</ins>


<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/ALBUQUERQUE-1961.jpg" width="1000">


<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/ALBUQUERQUE-2015.jpg" width="1000">


### <ins>Heatmap plots across the years.</ins>
First, I plotted the densities for every city and every year:


<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/heatmap.png" width="2000">



### <ins>Mean Temperature.</ins>

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Mean%20Temperature%20Evolution%20ALB.jpg" width="800">





<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Mean%20Temperature%20Evolution%20in%20USA.jpg" width="800">

### <ins>Mean Temperature.</ins>

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Monthly%20ALBL.jpg" width="800">


<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/ALBUQUERQUE.gif" width="800">


### <ins>TESTING AND ETC.</ins>

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Prediction.png" width="800">

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Training.png" width="800">

<img src="https://github.com/federicogaspar/Climate-Warming/blob/main/README%20IMG/Std.png" width="800">


