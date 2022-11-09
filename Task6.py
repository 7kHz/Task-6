class Student:
    student_list = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        Student.student_list.append(self)

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашнии задания: ' \
               f'{Reviewer.grades_average_student(self, self.grades)}\n' \
               f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n' \
               f'Завершенные курсы: {"".join(self.finished_courses)}'

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Not a lecturer')
        else:
            return Reviewer.grades_average_student(self, self.grades) < \
                   Reviewer.grades_average_student(self, other.grades)

    def rate_hw_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached \
                and course in self.courses_in_progress:
            if course in Lecturer.lecturer_grades:
                lecturer.lecturer_grades[course] += [grade]
            else:
                Lecturer.lecturer_grades[course] = [grade]
        else:
            return 'Ошибка'

    def grades_average_lecturer(self, grades_lec, course_lec):
        count = 0
        res = []
        for value in grades_lec.setdefault(''.join(course_lec)):
            count += value
            res.append(value)
        return round(count / len(res), 2)


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    lecturer_grades = {}

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: ' \
               f'{Student.grades_average_lecturer(self, Lecturer.lecturer_grades, self.courses_attached)}'

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a lecturer')
        else:
            return Student.grades_average_lecturer(self, self.lecturer_grades, self.courses_attached) < \
                   Student.grades_average_lecturer(self, other.lecturer_grades, other.courses_attached)


class Reviewer(Mentor):
    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def rate_hw_student(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def grades_average_student(self, grades_student):
        count = 0
        res = []
        for key, values in grades_student.items():
            for value in values:
                count += value
                res.append(value)
        return round(count / len(res), 2)


dark_knight = Student('Dark', 'Knight', 'your_gender')
dark_knight.courses_in_progress += ['C++', 'Python']
dark_knight.finished_courses += ['Введение в программирование']

dan_braun = Student('Dan', 'Braun', 'your_gender')
dan_braun.courses_in_progress += ['C++', 'Python']
dan_braun.finished_courses += ['GIT']

bruce_banner = Reviewer('Bruce', 'Banner')
bruce_banner.courses_attached += ['C++', 'Python']
bruce_banner.rate_hw_student(dark_knight, 'C++', 3)
bruce_banner.rate_hw_student(dark_knight, 'Python', 4)

tony_stark = Reviewer('Tony', 'Stark')
tony_stark.courses_attached += ['Python', 'C++']
tony_stark.rate_hw_student(dan_braun, 'Python', 5)
tony_stark.rate_hw_student(dan_braun, 'C++', 4)

paul_walker = Lecturer('Paul', 'Walker')
paul_walker.courses_attached += ['C++']
dark_knight.rate_hw_lecturer(paul_walker, 'Python', 5)
dark_knight.rate_hw_lecturer(paul_walker, 'C++', 2)

darth_vader = Lecturer('Darth', 'Vader')
darth_vader.courses_attached += ['Python']
dan_braun.rate_hw_lecturer(darth_vader, 'C++', 5)
dan_braun.rate_hw_lecturer(darth_vader, 'Python', 3)

print(bruce_banner.__str__())
print(paul_walker.__str__())
print(dan_braun.__str__())

print(dark_knight < dan_braun)
print(darth_vader < paul_walker)


def student_course_grade_average(student_list, student_course):
    count = 0
    res = []
    for student in student_list:
        for value in student.grades.get(student_course):
            count += value
            res.append(value)
    return f'Средняя оценка студентов за курс {student_course} = {round(count / len(res), 2)}'


print(student_course_grade_average(Student.student_list, 'C++'))


def lecturer_course_grade_average(lecturer_list, lecturer_course):
    count = 0
    res = []
    for lecturer in lecturer_list:
        for value in lecturer.lecturer_grades.get(lecturer_course):
            count += value
            res.append(value)
    return f'Средняя оценка лекторов за курс {lecturer_course} = {round(count / len(res), 2)}'


print(lecturer_course_grade_average([paul_walker, darth_vader], 'Python'))

