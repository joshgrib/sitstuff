# course-scheduler

[Website](http://www.sitstuff.com)

This is a website I made to be a resource for the students of Stevens Institute of Technology

##Background
So at Stevens the only way to reasonably figure out your schedule for future semesters is to use the course scheduler available [here](https://web.stevens.edu/scheduler/). You can search for classes and see different offerings, and work out a schedule that suits you best.To figure out your schedule you basically just need to use trial and error until you create one that works and you're relatively happy with. I want to make it so that you can enter the courses you need to take, and all possible schedules will be generated.

That's what inspired me to make a tool to see all possible schedules you could have, given the classes you want to take. Then I wanted to make it a web app, then it inherited the goal of another website I had to host course info.

##Approach
So using [the scheduler API](https://www.thegreatco.com/projects/scheduler-api/), you can request the XML for any semester. I take the XML and a list of courses and pull out the info I need, and turn it into a big nested dictionary. Then I go through all the courses and sections, find all possible combinations, and check for conflicts. Any schedules with no conflicts are put into a new dictionary, and sent through flask to make the HTML to display for the user.

##Python libraries
**flask** - the web framework that kinda runs everything

**json** - Course combos are stored as JSON in a cookie

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

**course_class.py** - a python class to represent a course

**scheduler.py** - the script to get feasible schedules

**secrets.py** - the secret stuff to keep stuff secure

**settings.py** - some macro-type-stuff to control how the app works

**templates/** - all the HTML files

##Important processes
**Parsing XML** - The XML file is iterated over in different ways to pull out the info I need to schedule the courses, and all the info is saved as a (pretty nested) dictionary

**Scheduling** - Given the list of courses to be scheduled, all possible combinations are found. Then each combination is checked against the dictionary from "Parsing XML" to find conflicts. If no conflicts are found, the combination is added to a list of good combos

**`Course` object** - all courses for the `Courses` page are stored in the class defined by the `course_class` module. Department, number, name, lecture, recitation, lab, homework, exams, and final are attributes, books are a dictionary with the key/value pair file_name/name, where file_name is the name of the file in the location specified in the `getHTML()` method of the class.

**Data storage** - The xml file is not stored, it is saved temporarily, parsed and deleted. This allows each schedule to always have the most recent info. The course info is stored in `courses.dat`. All the `Course` objects are stored in a list, then that list is saved to (and loaded from) the file through pickle. The functions `save_data(data)` and `load_data()` are in the `course_class` module.

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

**Optional(but suggested):**Make a virtualenv for the project.
`virtualenv venv`, `source venv/bin/activate`, then `pip install -r requirements.txt`.
this should install everything you need with the right versions. A virtualenc also lets you use different versions than you have installed globally.
`pip freeze` will printout the current pip installs

Then you should be able to run it locally by going to the main directory and running `python run.py` and then pointing your browser to `127.0.0.1:5000`. The stylesheet is pulled from my server, but you can easily add your own or modify mine by making a new file and changing `templates/base.html` to use the new one.

Mess around on your own, or add a feature and create a pull request.
