'''
Class to represent courses for the course info page on sitstuff
'''
import os
import pickle


def remove_spaces(my_str):
    """Remove the spaces from the end of a string"""
    if(my_str == ""):
        return ""
    if(my_str[-1] == " "):
        return remove_spaces(my_str[:-1])
    else:
        return my_str


def load_data():
    """Loads the data from .dat file... get it? dat file? No? Okay..."""
    my_dir = os.path.dirname(__file__)
    file_path = os.path.join(my_dir, 'courses.dat')
    try:
        with open(file_path) as f:
            data = pickle.load(f)
    except:
        data = []
    return data


def save_data(data):
    """Saves the data to the .dat file"""
    my_dir = os.path.dirname(__file__)
    file_path = os.path.join(my_dir, 'courses.dat')
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


class Course:

    # constructor
    def __init__(self, dept, num, name):
        self.__dept = remove_spaces(dept.upper())
        self.__num = remove_spaces(num)
        self.__name = remove_spaces(name)
        self.__lecture = None
        self.__recitation = None
        self.__lab = None
        self.__homework = None
        self.__exams = None
        self.__final = None
        self.__books = {}

    # department setter/getter
    @property
    def dept(self):
        return self.__dept

    @dept.setter
    def dept(self, local_dept):
        '''Used to let the value be set/updated later'''
        if len(local_dept) not in range(1, 5):  # department should be between 1 and 4 characters
            raise ValueError(
                'Department should be between 1 and 4 characters. Ex: CS, HHS, E')
        self.__dept = remove_spaces(local_dept.upper())
    # course number setter/getter

    @property
    def num(self):
        return self.__num

    @num.setter
    def num(seld, local_num):
        if len(local_num) == 2:
            self.__num = remove_spaces(local_num)
        else:
            raise ValueError(
                'Number should be three digits. Ex: 115, 221, 468')
    # course name setter/getter

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, local_name):
        self.__name = remove_spaces(local_name)

    # course lecture setter/getter
    @property
    def lecture(self):
        return self.__lecture

    @lecture.setter
    def lecture(self, local_lecture):
        self.__lecture = local_lecture

    # course recitation setter/getter
    @property
    def recitation(self):
        return self.__recitation

    @recitation.setter
    def recitation(self, local_recitation):
        self.__recitation = local_recitation
    # course lab setter/getter

    @property
    def lab(self):
        return self.__lab

    @lab.setter
    def lab(self, local_lab):
        self.__lab = local_lab
    # course homework setter/getter

    @property
    def homework(self):
        return self.__homework

    @homework.setter
    def homework(self, local_homework):
        self.__homework = local_homework
    # course exams setter/getter

    @property
    def exams(self):
        return self.__exams

    @exams.setter
    def exams(self, local_exams):
        self.__exams = local_exams
    # course final setter/getter

    @property
    def final(self):
        return self.__final

    @final.setter
    def final(self, local_final):
        self.__final = local_final
    # course books setter/getter

    @property
    def books(self):
        return self.__books

    @books.setter
    def books(self, pdf, name):
        self.__books[pdf] = name

    # output stuff
    def __str__(self):
        return str(self.__dept) + str(self.__num) + ': ' + str(self.__name)

    def __repr__(self):
        return "<Course {'dept':'" + str(self.__dept) + "', 'num':" + str(self.__num) + ", 'name':" + str(self.__name) + "}>"

    def getHTML(self):
        title = '<h3 id="' + self.__dept + '">' + self.__dept + \
            self.__num + " - " + self.__name + '</h3>'
        info = ''
        if (self.lecture != None):
            info = info + '<b>Lecture:</b>' + self.lecture + '<br>'
        if (self.recitation != None):
            info = info + '<b>Recitation:</b>' + self.recitation + '<br>'
        if (self.lab != None):
            info = info + '<b>Lab:</b>' + self.lab + '<br>'
        if (self.homework != None):
            info = info + '<b>Homework:</b>' + self.homework + '<br>'
        if (self.exams != None):
            info = info + '<b>Exams:</b>' + self.exams + '<br>'
        if (self.final != None):
            info = info + '<b>Final:</b>' + self.final + '<br>'
        if (self.books != {}):
            other_stuff = '<fieldset><legend> Books and required stuff </legend>'
            for book in self.books:
                other_stuff = other_stuff + '<a href="http://sitstuff.com/book/' + \
                    book + '" target="_blank">' + self.books[book] + '</a><br>'
            other_stuff = other_stuff + '</fieldset>'
        else:
            other_stuff = ""
        return title + info + other_stuff

    def getFormData(self):
        """Returns everything that has value in a dictionary"""
        result = {}
        result['dept'] = self.__dept
        result['num'] = self.__num
        result['name'] = self.__name
        if self.lecture != None:
            result['lecture'] = self.lecture
        if self.recitation != None:
            result['recitation'] = self.recitation
        if self.lab != None:
            result['lab'] = self.lab
        if self.homework != None:
            result['homework'] = self.homework
        if self.exams != None:
            result['exams'] = self.exams
        if self.final != None:
            result['final'] = self.final
        if self.books != None:
            result['books'] = self.books
        return result


'''
    myC = Course('cs', '115', 'Intro to Computer Science')
    myC.lecture = 'lecture info'
    myC.recitation = 'recitation info'
    myC.lab = 'lab info'
    myC.homework = 'homework info'
    myC.exams = 'exams info'
    myC.final = 'final info'
    myC.books['file.pdf'] = 'Test file'
    print myC.getHTML()
'''
'''
    <h3 id="C"> CH115 - Chemistry 1 </h3>
    <b>Lecture:</b>2 1-hour lectures per week. Most people stop going after 3 weeks or so, obviously people that go more generally do better<br>
    <b>Recitation:</b>1 recitation per week - go over topics from lecture, 10 minute quiz<br>
    <b>Exams:</b>3 1-hour exams<br>
    <b>Homework:</b>MasteringPhysics - 1 online assignment/week<br>
    <b>Final:</b>4 hour allotted time, generally takes 1-2.5 hour<br>
    <fieldset><legend> Books and required stuff </legend>
        OWLv2 Online Course - Not actually used for most recitations<br>
        <a href="http://sitstuff.com/books/First_Semester/ZumdahlChem9.pdf" target="_blank">Zumdahl Chemistry 9th Edition</a><br>
    </fieldset>
'''
