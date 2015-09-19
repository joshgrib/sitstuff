# course-scheduler

[Website](http://www.sitstuff.com)

This is a website I made to be a resource for the students of Stevens Institute of Technology

##Background
So at Stevens the only way to reasonably figure out your schedule for future semesters is to use the course scheduler available [here](https://web.stevens.edu/scheduler/). You can search for classes and see different offerings, and work out a schedule that works.To figure out your schedule you basically just need to do trial and error until you find one that works and you're relatively happy with. I want to make it so you enter the courses you need to take, and you can see all the schedules you could have.

That's what inspired me to make a tool to see all possible schedules you could have, given the classes you want to take. Then I wanted to make it a web app, then it inherited the goal of another website I had to host course info.

##Approach
So using [the scheduler API](https://www.thegreatco.com/projects/scheduler-api/), you can request the xml for any semester. I take the xml and a list of courses and pull out the info I need, and turn it into a big nested dictionary. Then I go through all the courses and sections, find all possible combinations, and check for conflicts. Any schedules with no conflicts are put into a new dictionary, and sent through flask to make the HTML to display them for the user.

##Python libraries
**flask** - the web framework that kidna runs everything

**json** - Course combos are store as JSON in a cookie

**os** - to remove files that are temporarily saved (like the xml from the Scheduler API)

**random** - to get a random number as a temporary password for the admin area

**smtplib** - to text me the password for the admin area

**hashlib** - to encrypt the password for the admin area

**pickle** - to store course info as a list of class objects

**urllib** -  to get the xml from the scheduler api

**xml.etree.ElementTree** - to turn the xml into something python can work with

**re** - regex matching used in xml parsing

**itertools** - to find all possible course combos

##Key files
**run.py** - the main file for flask - runs the website

**course_class.py** - a class to represent a course

**scheduler.py** - the script to get feasible schedules

**secrets.py** - the secret stuff to keep stuff secure

**settings.py** - some macro-type-stuff to control how the app works

**templates/** - all the HTML files

##Contributing
Clone the repo, make a secrets.py with the following:
```
def send_message():
    login={}
    login['emailUsername'] = "USERNAME@gmail.com"
    login['emailPassword'] = "PASSWORD"
    login['phone_number']  = '##########@vtext.com'
    return login
def app_secret():
    return "Some_secret_thing_for_the_app"
```

**Optional(but suggested):**Make a virtualenv for the project, then `pip install Flask`. After that `pip freeze` should be something like:
```
Flask==0.10.1
itsdangerous==0.24
Jinja2==2.8
MarkupSafe==0.23
Werkzeug==0.10.4
```
and then you don't have to worry about changing versions or whatever, and you won't mess up any other project's dependencies that you might have on your machine. Just be sure you're in the virtual environment whenever you're running the app or stuff won't work.

Then you should be able to run it locally by going to the main directory and running `python run.py` and then pointing your browser to `127.0.0.1:5000`. The stylesheet is pulled from my server, but you can easily add your own or modify mine by making a new file and changing `templates/base.html` to use the new one.

Mess around on your own, or add a feature and create a pull request.
