# DataAnalysis_PizzaRestaurant

## A simple data analysis of a year worth of orders from a pizza restaurant with the goal of optimizing each week's ingredients

This project consists of a simple pandas program which calculates the mode of the quantity spent each week for each ingredient.
Also, it supplies a data analysis of nulls and nans for each table.
This was done as a pandas practice and does not have the aim to make real recommendations on supply management.
To really recommend on that aspect, a more advanced algorythm that takes into account more variables should be used.

### Instructions:
To execute the program, run "pizzas.py"
Also, it is possible to create a docker image to safely deploy the program
To do that, just run the following command in the console, inside the directory where you clone this repository:
docker build . -t DataAnalysis_PizzaRestaurant