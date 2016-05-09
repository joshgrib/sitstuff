#############################################
#   A module for accessing a database to:   #
#   -Add courses                            #
#   -Edit course info                       #
#   -Other cool stuff                       #
#############################################
import sqlite3

#DATABASE = 'course_info.db'
#TABLE = 'courses'

class CourseDB:
    """
    A class for accessing a database name 'courses'
    With the following schema:
    dept|number|name|lecture|recitation|homework|exams|final
    with each value of type 'text',
    except 'number' which is integer
    """
    def __init__(self, database, table):
        self.__database = database
        self.__table = table
        self.__conn = self.get_conn()
        self.__cursor = self.get_cursor()
    def get_conn(self):
        return sqlite3.connect(self.__database)
    def get_cursor(self):
        return self.__conn.cursor()
    def ex_and_comm(self, query):
        self.__cursor.execute(query)
        self.__conn.commit()
    def ex_and_return(self, query):
        return self.__cursor.execute(query)
    def open_db(self):
        self.__conn = self.get_conn()
        self.__cursor = self.get_cursor()
    def close_db(self):
        self__conn.commit()
        self.__conn.close()
    def create_table(self):
        """
        Creates the initial table in the db and schema
        This could be improved to take in a tuple of tuples of
        values and types or something, but I'm making it for a
        pretty specific use right now, ideas for the future though
        """
        query = "CREATE TABLE {0}(".format(self.__table)
        query += "dept       text,"
        query += "number     integer,"
        query += "name       text,"
        query += "lecture    text,"
        query += "recitation text,"
        query += "homework   text,"
        query += "exams      text,"
        query += "final      text)"
        self.ex_and_comm(query)
    def delete_table(self):
        query = "DROP TABLE {0}".format(self.__table)
        self.ex_and_comm(query)
    def get_table(self):
        query = "SELECT * FROM {0} ".format(self.__table)
        query += "ORDER BY dept ASC, number ASC"
        return self.ex_and_return(query)
    def print_table(self):
        table = self.get_table()
        for row in table:
            print row

    def add_course(self, dept, num, name):
        query = "INSERT INTO {0} ".format(self.__table)
        query += "VALUES ('{0}', '{1}', '{2}', '{3}', '{3}', '{3}', '{3}', '{3}')".format(dept, num, name, None)
        self.ex_and_comm(query)
    def del_course(self, dept, num):
        query = "DELETE FROM {0} ".format(self.__table)
        query += "WHERE dept='{0}' AND number='{1}'".format(dept, num)
        self.ex_and_comm(query)
    def get_course(self, dept, num):
        query = "SELECT * from {0} ".format(self.__table)
        query += "WHERE dept='{0}' AND number='{1}'".format(dept, num)
        #query gets an array of items, I just want the first
        for result in self.ex_and_return(query):
            return result
    def print_course(self, dept, num):
        for row in self.get_course(dept, num):
            print row

    def update_value(self, dept, num, col, info):
        query = "UPDATE {0} ".format(self.__table)
        query += "SET {0}='{1}' ".format(col, info)
        query += "WHERE dept='{0}' AND number='{1}'".format(dept, num)
        self.ex_and_comm(query)
    def update_lecture(self, dept, num, info):
        self.update_value(dept, num, 'lecture', info)
    def update_recitation(self, dept, num, info):
        self.update_value(dept, num, 'recitation', info)
    def update_homework(self, dept, num, info):
        self.update_value(dept, num, 'homework', info)
    def update_exams(self, dept, num, info):
        self.update_value(dept, num, 'exams', info)
    def update_final(self, dept, num, info):
        self.update_value(dept, num, 'final', info)

    def get_value(self, dept, num, col):
        query = "SELECT {0} FROM {1} ".format(col, self.__table)
        query += "WHERE dept='{0}' AND number='{1}'".format(dept, num)
        #the following nonsense to to make sure I only get the text
        #of the first result
        for result in self.ex_and_return(query):
            return result[0]
    def get_lecture(self, dept, num):
        return self.get_value(dept, num, 'lecture')
    def get_recitation(self, dept, num):
        return self.get_value(dept, num, 'recitation')
    def get_homework(self, dept, num):
        return self.get_value(dept, num, 'homework')
    def get_exams(self, dept, num):
        return self.get_value(dept, num, 'exams')
    def get_final(self, dept, num):
        return self.get_value(dept, num, 'final')

    def __str__(self):
        return "Table {0} in file {1}".format(self.__table, self.__database)

    def get_course_HTML_helper(self, dept, num, name, lecture, recitation, homework, exams, final):
        title = '<h3 id="{0}">{0}{1} - {2}</h3>'.format(dept, num, name)
        info = ''
        if (lecture != 'None'):
            info += "<b>Lecture:</b>{0}<br>".format(lecture)
        if (recitation != 'None'):
            info += "<b>Recitation:</b>{0}<br>".format(recitation)
        if (homework != 'None'):
            info += "<b>Homework:</b>{0}<br>".format(homework)
        if (exams != 'None'):
            info += "<b>Exams:</b>{0}<br>".format(exams)
        if (final != 'None'):
            info += "<b>Final:</b>{0}<br>".format(final)
        return title + info
    def get_course_HTML(self, c):
        return self.get_course_HTML_helper(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7])
    def get_HTML(self):
        table = self.get_table()
        html = ''
        for row in table:
            html += self.get_course_HTML(row)
        return html
    def get_depts(self):
        query = "SELECT dept FROM {0}".format(self.__table)
        resp = []
        for result in self.ex_and_return(query):
            resp += result
        return resp


if __name__ == '__main__':
    #print "Sorry no tests active right now"
    """Below: feature testing"""
    db = CourseDB('test.db', 'test')
    try:
        db.create_table()
    except sqlite3.OperationalError:
        db.delete_table()
        db.create_table()
    db.add_course('AA', '101', 'Intro to db class')
    db.add_course('BB', '202', 'Databases class 2')
    db.add_course('CC', '303', 'Advanced DB class')
    dept = ['AA', 'BB', 'CC']
    num = ['101', '202', '303']
    for i in range(2):
        db.update_lecture(dept[i], num[i], 'Lecture info')
        db.update_recitation(dept[i], num[i], 'Rec info')
        db.update_homework(dept[i], num[i], 'HW info')
        db.update_exams(dept[i], num[i], 'Exam info')
        db.update_final(dept[i], num[i], 'Final info')
    print db.get_HTML()
    print db.get_depts()
    #db.print_course(dept, num)
    #print "    Lecture:    {0}".format(db.get_lecture(dept, num))
    #print "    Recitation: {0}".format(db.get_recitation(dept, num))
    #print "    Homework:   {0}".format(db.get_homework(dept, num))
    #print "    Exams:      {0}".format(db.get_exams(dept, num))
    #print "    Final:      {0}".format(db.get_final(dept, num))
    #db.del_course('BB', '202')
    db.print_table()
    db.delete_table()
    #db.print_table()
    db.close_db()
