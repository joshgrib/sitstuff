# course-scheduler

[Website](http://www.sitstuff.com)

I'm pretty sure a few CS students at Stevens have tried something like this already, but I'm doing it anyway. This is a tool to take all the classes you need to take and look at the xml that the calendar runs off, then show you your possible schedules

##Background
So at Stevens the only way to reasonably figure out your schedule for future semesters is to use the course scheduler available [here](https://web.stevens.edu/scheduler/). You can search for classes and see different offerings, and work out a schedule that works.

To figure out your schedule you basically just need to do trial and error until you find one that works and you're relatively happy with. I want to make it so you enter the courses you need to take, and you can see all the schedules you could have.

##Approach
So using [the scheduler API](https://www.thegreatco.com/projects/scheduler-api/), which I'm surprised is documented as well as it is for anyone to use, you can request the xml for any semester. I take the xml and a list of courses and pull out the info I need, and turn it into a big nested dictionary. Then I go through all the courses and sections, find all possible combinations, and check for conflicts. Any schedules with no conflicts are put into a new dictionary, and sent through flask to make the HTML to display them for the user.

###Python libraries
####flask
The web app framework I'm using to make the program run online and keep everything organized. It was annoying to learn but it was worth refactoring everything. Its much easier when everything is working the way it's supposed to
####xml.etree.ElementTree
For XML parsing. This library turn XML data into nested dictionaries. Then I can go through, edit them, and pull out what I need
####re
Regex
####itertools
For finding all possible combinations, and for finding all possible comparisons to make within a combination
####urllib
Gets the XML data from the API using the url
####os
Delete files

###Files
```
/course-scheduler               #Holds the app
    /static                     #
        style.css               #The CSS for the site
    /templates                  #
        add_course_form.html    #Allows admin to add a course
        admin_form.html         #The entry point for the admin
        base.html               #The base for all other pages
        courses.html            #List of all course info and resources
        donate.html             #Donation page
        edit_course_form.html   #Allows admin to edit courses
        how_many.html           #Asks how many courses someone wants to
                                 schedule
        index.html              #The home page
        sched.html              #Displays computed schedules
        schedule_entry.html     #Asks what courses someone wants to schedule
    .gitignore                  #Tells git what not to track
    LICENSE                     #The license on the software
    README.md                   #This page
    courses.json                #Stores all course info
    run.py                      #Starts the app
    scheduler.py                #Computes schedules given a list of courses
    secrets.py                  #Passwords for stuff
    settings.py                 #Things to change the behavior of the site
```

###Future development ideas (also see issues)
* Add sorting to show certain schedules before others (e.g. least morning classes, no night classes, fridays off)
