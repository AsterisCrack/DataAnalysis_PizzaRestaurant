# DataAnalysis_PizzaRestaurant

## A simple data analysis of a year worth of orders from a pizza restaurant with the goal of optimizing each week's ingredients

This project consists of a simple pandas program which calculates the mode of the quantity spent each week for each ingredient.
Also, it supplies a data analysis of nulls and nans for each table.
This was done as a pandas practice and does not have the aim to make real recommendations on supply management.
To really recommend on that aspect, a more advanced algorythm that takes into account more variables should be used.

Update: 
Added support for analyzing data from 2016. This new data had to be cleaned so I also added a new python script to do this.
New files to support this, identified with their original name + _2016, were also created by modifying the original ones.

Update 2:
Added support to save data into XML files. Data is now being saved in different XML files, including the data analysis of each table and
the final results. Added multiple python files to support this change.

Update 3:
Added support for creating an executive report in pdf. Using fpdf and matplotlib+seaborn to analyze and visualize the data. Added a python file to support this change.

### Instructions:
To execute the program, run "pizzas.py" or "pizzas_2016.py".
Also, it is possible to create a docker image to safely deploy the program
To do that, just run the following command in the console, inside the directory where you clone this repository:

docker build . -t DataAnalysis_PizzaRestaurant
