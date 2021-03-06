**Due to [Microsoft's acquisition of GitHub](https://arstechnica.com/gadgets/2018/06/microsoft-snaps-up-github-for-7-5-billion/) I have moved [all my projects to GitLab](https://gitlab.com/guillaumedsde) and have stopped using GitHub, all further development will take place on GitLab**

![alt text](https://raw.githubusercontent.com/guillaumedsde/Placeholdr/master/static/images/logonobg.png)


## Description
placeholdr is a Django web application with the objective of allowing people to browse through places of interest and create trips based on those places, with a user community that provides ratings, comments, pictures.
This is a fork of [the original Placeholdr webapp](https://github.com/WADPlaceholdr/Placeholdr)

## Demo
a live demo is not yet available, clone repo to demo

## Requirements
(see [requirements.txt](https://github.com/WADPlaceholdr/Placeholdr/blob/master/requirements.txt))
* Python 3.6.x
* pip3
* Django==1.11.7
* django-bootstrap4==0.0.6
* django-csp==3.3
* django-mathfilters==0.4.0
* django-referrer-policy==1.0
* django-geoposition==0.3.1
* Pillow==5.0.0
* pytz==2018.3
* selenium==3.11.0

## Installation
clone this repository
```
git clone https://github.com/guillaumedsde/Placeholdr.git
```

install requirements
```
cd Placeholdr
pip install –r requirements.txt --yes
```

**optional** create deployment_variables.py
(don't use for development/test environment, deployment only)
(default conf file uses HTTPS with HTST and all security headers strictly configured
```
mv placeholdr/deployment_variables.py.conf placeholdr/deployment_variables.py
```


create database
```
python manage.py migrate
```

**optional** populate placeholdr with sample data
```
python population_script.py
```


## Support
for support please submit an issue on [GitHub](https://github.com/guillaumedsde/Placeholdr/issues)
