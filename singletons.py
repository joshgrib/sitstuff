import course_class
import os
import json

def add_course(dept, number, name):
    """Add a new course to the list of courses"""
    courses = course_class.load_data()
    #add new course
    new = course_class.Course(dept, number, name)
    courses = courses + [new]
    course_class.save_data(courses)

def add_book(course_n, url, title):
    """Usage: add_book("MA222", "ma222_8e.pdf", "Book Name, 3rd edition")"""
    courses = course_class.load_data()
    for course in courses:
        print course, "\n", course.books, "\n"
        if str(course)[:len(course_n)] == course_n:
            print "Found it!!!!!!!!!!!!!!!!"
            course.books[url] = title
            print "added book"
            print "---\n"
    course_class.save_data(courses)

def rem_course(course_n):
    courses = course_class.load_data()
    count = 0
    for course in courses:
        if str(course)[:len(course_n)] == course_n:
            if(count<2):
                print "Found one!"
                courses.remove(course)
                count += 1
    course_class.save_data(courses)

if __name__ == "__main__":
    print "------------------Starting------------------"
    #add_course("PEP", "201", "Physics II for Engineering Students")
    #add_book("PEP201", "pep111_3e.pdf", "Physics for Scientists and Engineers, Knight 3rd Edition")
    #rem_course("PEP201")
    print "--------------------Done--------------------"




    '''
    #get sorted course list
    sorted_courses = sorted(courses, key=lambda x: x.dept+x.num)

    for course in sorted_courses:
        print "---"
        print "Course:" + course.dept + course.num
        for book in course.books:
            print book
#            new_u = raw_input("Enter new url:")
#            course.books
#            name = course.books[book]
#            del course.books[book]
#            course.books[new_u] = name
#    course_class.save_data(courses)

    this_list = course_class.load_data()
    clist = []
    for course in this_list:
        clist = clist + [course.dept + "   " + course.num]
    for i in sorted(clist):
        print i


    my_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(my_dir, 'courses.json')
    with open(json_file_path, 'r') as f:
        these_courses = json.load(f)

    c_list = []

    for course in these_courses:
        #print course
        dept = course[0:3]
        num = course[3:7]
        name = course[9:]
        myC = course_class.Course(dept, num, name)
        #print repr(myC)
        for category in these_courses[course]:
            if category == 'info':
                #print "  " + category
                for thing in these_courses[course]['info']:
                    if thing == 'Lecture':
                        print "    Lecture"
                        myC.lecture = these_courses[course]['info']['Lecture']
                    if thing == 'Recitation':
                        #print "    Reciation"
                        myC.recitation = these_courses[course]['info']['Recitation']
                    if thing == 'Homework':
                        #print "    Homework"
                        myC.homework = these_courses[course]['info']['Homework']
                    if thing == 'Exams':
                        #print "    Exams"
                        myC.exams = these_courses[course]['info']['Exams']
                    if thing == 'Final':
                        #print "    Final"
                        myC.final = these_courses[course]['info']['Final']
            if category == 'books':
                #print "  " + category
                for book in these_courses[course]['books']:
                    #print "    " + book
                    name = these_courses[course]['books'][book]['name']
                    url = these_courses[course]['books'][book]['url']
                    #print name
                    #print url
                    myC.books[url] = name
            print myC.lecture
            print myC.recitation
            print "---"
        c_list = c_list + [myC]

    course_class.save_data(c_list)
    '''
