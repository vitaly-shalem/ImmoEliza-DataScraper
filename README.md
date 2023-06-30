
# Immoweb scraping

This is the first stage of the project wich purpose is to create a Machine Learning model to make price predictions on real estate sales in Belgium.

The task of the stage is to build a dataset gathering information about 15.000 properties all over Belgium. This dataset will be used later as a training set for your prediction model.

This dataset is a `csv` file with the following columns:

- id number of a property at www.immoweb.be;
- url of a property;
- price;
- type;
- locality and address;
- floor if it is an appartment;
- number of bedrooms;
- surface;
- construction year;
- facade count;
- floor count;
- if its has elevator;
- type of kitchen;
- garden and its surface;
- terace and its surface;
- land and its surface;
- if a property has fireplace;
- if its has swimming pool;
- airconditioner;
- number of bathrooms, showers and toilets;
- parkinglot;
- ammount of energy consumption per square meter;
- energy consumption score;
- doubleglazing;
- saletype.

The script scrapes from the www.immoweb.be pages assential information about the properties using BeatifulSoup and Selenium. All the data are situated into the distionary where the property's ids are keys and the values are nesteed dictionaries with scraped datas. Then this dictionary is converted into Pandas' dataframe where rows are ids of the properties and columns are properties' attributes listed above. Then the script cleans up data from undesirable mistakes, marks and characters. After that Pandas' dataframe is converted into ".csv" file.

## How to Install and Run the Project
To run the stage of the project you need to install folowing libraries:
beautifulsoup4==4.12.2 (pip install beautifulsoup4)
lxml==4.9.2 (pip install lxml)
requests==2.31.0 (pip install requests)
pandas==2.0.3 (pip install pandas)
selenium==4.0.0. (pip install selenium)

Then you have to copie from GitHub repository https://github.com/vitaly-shalem/ImmoEliza-DataScraper to your local computer all folders and run "main.py" file using command "python main.py" from your current folder where you copied files and folders are situated.

## How to Use the Project
The script scrapes from the www.immoweb.be pages assential information about the properties. 

The output of the code will be a ".csv" file where rows are properties according to their ids and columns are properties' attributes. At the next stages this file will be used for a Machine Learning model to make price predictions on real estate sales in Belgium.

## Credits
This stage of the project has lasted 5 days (June 26-30, 2023) as part of the AI Bootcamp at BeCode.org in Gent https://becode.org/.
The stage was made by group of Junior AI & Data Scientists:

Vitaly Shalem https://github.com/vitaly-shalem https://www.linkedin.com/in/vitaly-shalem-26aab265/ 

Félicien De Hertogh https://github.com/feldeh https://www.linkedin.com/in/feliciendehertogh/

Cesar E. Mendoza V. https://github.com/mendoce24 https://www.linkedin.com/in/mendoce24/

Mykola Senko https://github.com/MykolaSenko https://www.linkedin.com/in/mykola-senko-683510a4/.

The stage was made under the supervision of Vanessa River Quinones https://www.linkedin.com/in/vriveraq/ and Samuel Borms https://www.linkedin.com/in/sam-borms/?originalSubdomain=be

## License

This project is under GPL License which allows to make modification to the code and use it for commercial purposes.

Gent, June 30, 2021