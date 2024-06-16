This is a robot that opens LATimes.

It accepts 2 args, a search phrase and a number.

The search phrase will be used to search for the latest news on latimes, the number will determine what's the period the robot needs to extract the news from.
The number has the followin logic 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on

The robot is made using Selenium and pure Python, Pandas and a few other libraries were used as well.

The output of the robot will be stored in an "output" folder in which all the news images will be stored alongside the "output.xlsx" file with data about the news.
A file with logs will also be created inside the project's folder.
