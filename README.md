# DSCI522-2425-28-five_guys
## Seoul Bike Share Predictor
- Author: Elaine Chu, Lukman Lateef, Dhruv Garg, Eugene You & Shawn Xiao Hu

This data analysis project is about the prediction of rental bikes in the Metro city of Seoul.

## About The Project

Currently Rental bikes are introduced in many urban cities for the enhancement of mobility comfort. It is important to make the rental bike available and accessible to the public at the right time as it lessens the waiting time. Eventually, providing the city with a stable supply of rental bikes becomes a major concern. The crucial part is the prediction of bike count required at each hour for the stable supply of rental bikes.

The data set that was used in this project is dataset contains count of public bicycles rented per hour in the Seoul Bike Sharing System, with corresponding weather data and holiday information created by Sathishkumar V E, Jangwoo Park, Yongyun Cho, "Using data mining techniques for bike sharing demand prediction in Metropolitan city", Computer Communications. It was sourced from the UCI Machine Learning Repository (Dua and Graff 2017) and can be found [here](https://archive.ics.uci.edu/dataset/560/seoul+bike+sharing+demand).

## Report

The comprehensive report and the analysis of the Seoul Bike Share Prediction can be found [here](https://github.com/UBC-MDS/DSCI522-2425-28-five_guys/blob/main/rental_bike_prediction.ipynb)


## Usage

To run this project, install the virtual environment from the root of this repository, and run below command:

```
conda-lock install --name seoul-bike-share-predictor conda-lock.yml
```

Instantiate jupyter lab from the root of this repository to run the analysis, run below command to begin:

```
jupyter lab
```

Navigate to the project folder in jupyper lab and open the `rental_bike_prediction.ipynb` notebook and under Select Kernel choose "Python [conda env:seoul-bike-share-predictor]".

After selecting the appropriate kernel, go under the "Kernel" menu and click "Restart Kernel and Run All Cells..."

## Dependencies

- `conda` (version 24.9.1 or higher)
- `conda-lock` (version 2.5.7 or higher)
- `jupyperlab` (version 4.2.4 0r higher)
- Python and other packages listed in environment.yml file

## Licence

The Seoul Bike Share Predictor software code contained in this project are licensed under MIT license. See the [licence file](https://github.com/UBC-MDS/DSCI522-2425-28-five_guys/blob/main/LICENSE) here for more information. The project report is licensed under [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) License. See the license file for more information. For proper referencing, when re-using any part of this code and/or report, please include the link to this webpage.


## References

Dua, Dheeru, and Casey Graff. 2017. “UCI Machine Learning Repository.” University of California, Irvine, School of Information; Computer Sciences. (https://archive.ics.uci.edu/).

Sathishkumar V E, Jangwoo Park, Yongyun Cho, "Using data mining techniques for bike sharing demand prediction in Metropolitan city", Computer Communications, vol. 153, pp. 353-366, 2020. 

Sathishkumar V E, Yongyun Cho, "A rule-based model for Seoul Bike sharing demand prediction using Weather data", European Journal of Remote Sensing, Vol. 52, no. 1, pp. 166-183, 2020.