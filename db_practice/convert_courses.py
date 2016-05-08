import json

with open('courses.json') as f:
    data = json.load(f)

courses = []
courses.append(['CAL', 103, 'Writing and Communications', None, None, None, None, None])
courses.append(['CAL', 105, 'Knowledge, Nature, and Culture', None, None, None, None, None])
courses.append(['CH', 115, 'Chemistry 1', None, None, None, None, None])
courses.append(['CH', 117, 'Chemistry Lab', None, None, None, None, None])
courses.append(['CH', 281, 'Biology', None, None, None, None, None])
courses.append(['CS', 135, 'Discrete Structures', None, None, None, None, None])
courses.append(['CS', 188, 'Seminar in COmputer Science', None, None, None, None, None])
courses.append(['CS', 284, 'Data Structures', None, None, None, None, None])
courses.append(['CS', 334, 'Computation and Automata', None, None, None, None, None])
courses.append(['CS', 383, 'Computer Organization and Programming', None, None, None, None, None])
courses.append(['CS', 503, 'Discrete Math for Cryptography', None, None, None, None, None])
courses.append(['E', 101, 'Engineering Experiences', None, None, None, None, None])
courses.append(['E', 115, 'Introduction to Programming', None, None, None, None, None])
courses.append(['E', 120, 'Graphics', None, None, None, None, None])
courses.append(['E', 121, 'Engineering Design 1', None, None, None, None, None])
courses.append(['E', 122, 'Engineering Design 1', None, None, None, None, None])
courses.append(['E', 126, 'Mechanics of Solids', None, None, None, None, None])
courses.append(['E', 245, 'Circuits and Systems', None, None, None, None, None])
courses.append(['H', 183, 'Research Seminar 1', None, None, None, None, None])
courses.append(['H', 184, 'Research Seminar 2', None, None, None, None, None])
courses.append(['MA', 121, 'Calc 1', None, None, None, None, None])
courses.append(['MA', 123, 'Calc 2', None, None, None, None, None])
courses.append(['MA', 188, 'Seminar in Math Sciences', None, None, None, None, None])
courses.append(['MA', 221, 'Differential Equations', None, None, None, None, None])
courses.append(['MA', 222, 'Probability and Statistics', None, None, None, None, None])
courses.append(['MA', 227, 'Multivariable Calculus', None, None, None, None, None])
courses.append(['MGT', 103, 'Introduction to Entrepreneurial Thinking', None, None, None, None, None])
courses.append(['PEP', 111, 'Mechanics', None, None, None, None, None])
courses.append(['PEP', 201, 'Physics 2 for Engineering Students', None, None, None, None, None])
courses.append(['QF', 101, None, None, None, None, None, None])

for course in sorted(data):
    print data[course]
