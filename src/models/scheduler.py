import urllib
import os
import xml.etree.ElementTree as etree
import re
import itertools

def get_sem_list():
    import requests
    import re
    url = 'http://web.stevens.edu/scheduler/core/'
    order  = {'W':0, 'S':1, 'A':2, 'B':3, 'F':4}#custom alphabetic order
    r = requests.get(url)
    myre = re.compile(r'[0-9]{4}[A-Z]')#get things like '####A'
    re_list =  myre.findall(r.text)
    sem_list = sorted(
        list(set(re_list)), #gets only unique values
        #sort by year then term in custom alphabetic order
        key=lambda semester: (semester[:4], order.get(semester[-1])),
        reverse=True)#most recent first
    return sem_list

SEMESTER = get_sem_list()[0]

def cleanupCourses(this_root, this_course_list):  # called from schedule()
    """Given the root of the xml tree and the course list, this will go through the XML and remove any course not in the list from the tree, then returns the revised root"""
    for course in this_root.findall('Course'):
        name = course.get('Section')
        while re.match("([A-Za-z-])", name[-1]) or re.match("([A-Za-z-])", name[-2]):
            name = name[:(len(name) - 1)]
        if name not in this_course_list:
            this_root.remove(course)
    return this_root

def cleanupElements(this_root):  # called from schedule()
    """Given the root of the xml tree, this goes through the courses and removes any elements that don't have info about meeting times, then returns the revised root"""
    for course in this_root.findall('Course'):
        for element in course:
            if element.tag == 'Meeting':
                pass
            else:
                course.remove(element)
    return this_root

def fixSpacing(this_root):  # called from schedule()
    """Given the root of the xml tree, this will go through and fix the spacing between the letters and numbers so it can be compared better later on, then returns the revised root"""
    for course in this_root:
        attribs = course.attrib
        section = attribs['Section']
        index_count = 0
        new_section = ""
        for letter in section:
            if letter == " ":
                letter = (4 - index_count) * " "
            new_section = new_section + letter
            index_count += 1
        attribs['Section'] = new_section
    return this_root

def fixTime(time):  # called from schedule()
    """Given a time from the "StartTime" or "EndTime" attribute in the xml tree, this will change teh format to HHMM and return the revised time. This also corrects a 4 hour offset present in the time formats"""
    time = time[:(len(time) - 4)]
    if len(time) == 4:  # add a 0 to the front of early times
        time = '0' + time
    time = time[:2] + time[3:]  # remove the colon
    hours = int(time[:2]) + 4  # correct 4 hour offset
    hours = str(hours)
    if len(hours) == 1:
        # add the 0 in fron of early times if it needs it now
        hours = "0" + hours
    time = hours + time[2:]
    return time

def fixTimeFormat(this_root):  # called from schedule()
    """Given the root of the xml tree, this will go through and fix the time formatting, making it standard 24hr as 4 digits in the form of HHMM, then returns the revised root"""
    for course in this_root:
        for meeting in course:
            attribs = meeting.attrib
            try:
                start_time = attribs['StartTime']  # get values
                end_time = attribs['EndTime']
                start_time = fixTime(start_time)  # fix values
                end_time = fixTime(end_time)
                attribs['StartTime'] = start_time  # reassign
                attribs['EndTime'] = end_time
            except KeyError:
                # somehow something that wasn't a meeting slipped through
                course.remove(meeting)
    return this_root

def getCallNums(this_root):  # called from schedule()
    """Given the root of the xml tree, this will parse the xml and return a dictionary of course sections and call numbers"""
    call_numbers = {}
    for course in this_root:
        section_name = course.attrib['Section']
        call_num = int(course.attrib['CallNumber'])
        call_numbers[section_name] = call_num
    return call_numbers

def getBigDict(this_root):  # called from schedule()
    """Given the root of the xml tree, this will parse the xml and return a nested dictionary of courses, sections, and meeting times"""
    big_dict = {}
    prev_course = ""
    for course in this_root:  # add classes and section lists
        attribs = course.attrib
        this_course = attribs['Section']
        if len(this_course) == 9:  # recitation course
            course_big = this_course[:8]
            course_section = this_course[8:]
            if course_big == prev_course[:8]:  # same course
                # add the new section with a list
                big_dict[course_big][course_section] = []
            else:  # new course
                big_dict[course_big] = {}  # add the new class
                # add the new section with a list
                big_dict[course_big][course_section] = []
        else:  # normal course(lecture)
            course_big = this_course[:7]
            course_section = this_course[7:]
            if this_course[:7] == prev_course[:7]:  # same course
                # add the new section with a list
                big_dict[course_big][course_section] = []
            else:  # new course
                big_dict[course_big] = {}  # add the new class
                # add the new section with a list
                big_dict[course_big][course_section] = []
        prev_course = this_course

        for meeting in course:  # write the meetings to the section lists
            info = meeting.attrib
            try:
                day = info['Day']
                startTime = info['StartTime']
                endTime = info['EndTime']
                # if the exact same meeting is already in the list
                if [day, startTime, endTime] in big_dict[course_big][course_section]:
                    break  # then dont add another!
                if len(day) == 1:  # if this meeting describes one day
                    big_dict[course_big][course_section].append(
                        [day, startTime, endTime])  # add the meeting time
                else:  # if multiple days happen at the same time
                    for letter in day:  # add one list for each meeting
                        big_dict[course_big][course_section].append(
                            [letter, startTime, endTime])
            except KeyError:
                pass
                #TOGGLE below for list of courses that cause errors
                #global global_class_error_list
                #global_class_error_list.append(str(course.get('Section')))
    return big_dict

def isAllowed(classList1, classList2):  # called from checkCombination()
    '''Given two meeting lists, check to see if there is a conflict, and return True if there is not'''
    # if class 2 ends before class 1 starts, or class 1 ends before class 2
    # starts, then it's fine
    if (classList2[2] < classList1[1]) or (classList1[2] < classList2[1]):
        return True
    else:
        return False

def checkCombination(courseDict, inputList):  # called from findAllCombos()
    '''This will go through a combination list and see if it all works. If it does it will return a true value'''
    conflicts = 0  # initialize counters
    # find all combinations of size 2 from the inputList
    for thisCombo in itertools.combinations(inputList, 2):
        # comparison one in the item in the list we are on now
        comp1 = thisCombo[0]
        # seperate the section and the course, different if its a lecture
        if len(comp1) == 9:
            course1 = comp1[0:8]
            section1 = comp1[8:]
        else:
            course1 = comp1[0:7]
            section1 = comp1[7:]

        comp2 = thisCombo[1]  # comparison two is the next item in the list
        # seperate the section and the course, different if its a letter
        if len(comp2) == 9:
            course2 = comp2[0:8]
            section2 = comp2[8:]
        else:
            course2 = comp2[0:7]
            section2 = comp2[7:]
        # check one is the list of meetings for course1 section1
        check1 = courseDict[course1][section1]
        # check two is the list of meetings for course2 section2
        check2 = courseDict[course2][section2]
        for meeting1 in check1:
            for meeting2 in check2:
                # if the meetings are on the same day...
                if meeting1[0] == meeting2[0]:
                    # if there is no conflicts do nothing
                    if (isAllowed(meeting1, meeting2) == True):
                        pass
                    # if there is a conflict, add to the conflict counter
                    else:
                        conflicts = conflicts + 1
    if conflicts == 0:  # if there were no conflicts, return true
        return True
    #return False #maybe this should be here?

def findAllCombos(courseDict, callNumbers):  # called from schedule()
    '''This function goes through the nested courses, stores lists of all possible combinations of courses, and prints them'''
    bigList = []  # list of lists of courses and sections
    goodCombos = []  # store all the good combinations
    badCombos = []  # store the bad combinations
    possibilities = ""
    # make a list of lists with the small lists being lists of possible
    # sections for one course
    for course in courseDict:
        courseList = []
        for section in courseDict[course]:
            courseList.append(str(course + section))
        bigList.append(courseList)
    combos = 0  # initialize the counter
    # find all combinations of one section of each class
    allCombos = list(itertools.product(*bigList))
    for combo in allCombos:
        combos = combos + 1
        # see if the combo works and add to apppropriate list
        checkCombination(courseDict, combo)
        if checkCombination(courseDict, combo) == True:
            goodCombos.append(combo)
        else:
            badCombos.append(combo)

    possibilities = {}
    # possibilities['totalCombos']=str(combos)
    # possibilities['goodCombos']=str(goodCombos)
    comboCounter = 1
    for x in goodCombos:
        urlPart = []
        possibilities[comboCounter] = {}
        for course in x:
            urlPart.append(callNumbers[str(course)])
        # format url
        url = 'https://web.stevens.edu/scheduler/#' + SEMESTER + '='
        for callNumber in urlPart:
            url = url + str(callNumber) + ","
        url = url[:-1]

        possibilities[comboCounter]['url'] = str(url)
        possibilities[comboCounter]['list'] = str(x)
        comboCounter = comboCounter + 1
    return possibilities

def schedule(course_list):
    """
    Given a list of courses, return a dictionary of the possible schedules
    ['BT 353','CS 135','HHS 468','BT 181','CS 146','CS 284'] -->
    {1:
        {'url': 'https://web.stevens.edu/scheduler/#2015F=10063,10486,10479,11840,12011,11995,10482,10487',
        'list': "('BT 181A', 'CS 284A', 'CS 135A', 'CS 135LB', 'BT 353C', 'HHS 468EV', 'CS 146B', 'CS 284RA')"},
     2: {'url': 'https://web.stevens.edu/scheduler/#2015F=10063,10486,10479,11840,12011,11995,10482,12166',
        'list': "('BT 181A', 'CS 284A', 'CS 135A', 'CS 135LB', 'BT 353C', 'HHS 468EV', 'CS 146B', 'CS 284RB')"},
     3: {'url': 'https://web.stevens.edu/scheduler/#2015F=10063,10486,10479,11840,12012,11995,10482,10487',
         'list': "('BT 181A', 'CS 284A', 'CS 135A', 'CS 135LB', 'BT 353D', 'HHS 468EV', 'CS 146B', 'CS 284RA')"},
     4: {'url': 'https://web.stevens.edu/scheduler/#2015F=10063,10486,10479,11840,12012,11995,10482,12166',
          'list': "('BT 181A', 'CS 284A', 'CS 135A', 'CS 135LB', 'BT 353D', 'HHS 468EV', 'CS 146B', 'CS 284RB')"}}
    """
    url = 'https://web.stevens.edu/scheduler/core/' + SEMESTER + '/' + SEMESTER + '.xml'
    urllib.urlretrieve(url, 'courses.xml')
    tree = etree.parse('courses.xml')
    os.remove('courses.xml')
    root = tree.getroot()

    root = cleanupCourses(root, course_list)
    root = cleanupElements(root)
    root = fixSpacing(root)
    root = fixTimeFormat(root)

    call_numbers = getCallNums(root)
    big_dict = getBigDict(root)

    all_combos = findAllCombos(big_dict, call_numbers)

    return all_combos


if __name__ == '__main__':
    print schedule(['CS 442', 'CS 392', 'CS 519', 'MA 331'])
