# airports
Website that can be used to compare the routes of the main airports of the world.

The website can be found at https://airports-6e281.web.app/index.html. The loading time of the maps is approximmately 20 seconds.

The website is hosted on *Google Firebase*

The python Flask server that generates the maps is hosted on *pythonanywhere.com*

## Backend

The Flask server runs a python script that returns the image showing the air routes starting from the chosen airport.

The script uses the Matplotlib Basemap Toolkit to generate maps.

## Frontend

The website can be used to easily compare maps created with the python scripts.

This is the first version of the website, which will soon be improved.

These screenshots show the comparison between the main London airports:

![Screenshot 1](/Screenshot1.png)
![Screenshot 2](/Screenshot2.png)

## Local version

The following command can be used to see the map locally on your machine

```
python3 script.py
```
## Author

* **Federico Stazi** - [FedericoStazi](https://github.com/FedericoStazi)
