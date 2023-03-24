## Team Kite Major Group project

### Team members
- Alexandru Godoroja (K20010163)
- Tanish Kejriwal
- Timi Disu (K20041416)
- Dylan Barker (K20001430)
- Joshua Bebbington
- Muhammad Jawad
- Saurav Miah (K20038361)
- Tejveer Nag

### Project structure
The project is called `bookclub` (The Kite Club). It currently consists of a single app `clubs` where all functionality resides.

### Deployed version of the application
The deployed version of the application can be found at *<[enter URL here](URL)>*.

### Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```sh
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```sh
$ pip3 install -r requirements.txt
```

Migrate the database:

```sh
$ python3 manage.py migrate
```

Clear data and seed the database with:
```sh
$ python3 manage.py seed
````
 - Clear data and seed the database with: `python3 manage.py seed --mode=refresh`
 - Clear data and and don't seed the database with: `python3 manage.py seed --mode=clear`
  
Load books into the database with:
```bash
$ python3 manage.py populate_books
```

Run all tests with:
```sh
$ python3 manage.py test
```

### Sources
The packages used by this application are specified in [requirements.txt](requirements.txt).

Favicon information [here](static/favicon/about.txt).

All images taken from [here](https://pexels.com).

#### Front-end technologies
[Font awesome](https://fontawesome.com/)

[Bootstrap bundle](https://getbootstrap.com)

[Bootstrap icons](https://icons.getbootstrap.com/)

[JQuery](https://jquery.com/)

[Datatables](https://datatables.net/)

#### Fonts
[MonaqiBold](https://fontlot.com/393802/monaqi-sans-serif-font/)

[Nexus](https://fontlot.com/386697/nexus-display-font)

[Zilap Minimalist](https://fontlot.com/265624/zilap-minimalist-sans-serif-font/)

