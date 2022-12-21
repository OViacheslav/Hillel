class Course:
    def __init__(self, name, start_date, number_of_lectures, teacher):
        self.name = name
        self.start_date = start_date
        self.number_of_lectures = number_of_lectures
        self.teacher = teacher
        self.lectures = [Lecture('Lecture ' + str(i), i, teacher, self) for i in range(1, number_of_lectures + 1)]
        self.homeworks = {i: Homework('Homework ' + str(i), None) for i in range(1, number_of_lectures + 1)}
        self.enrolled = []
        teacher.all_lectures.append(self.lectures)
        teacher.all_courses.append(self)

    def __str__(self):
        return f"{self.name} ({self.start_date})"

    def enrolled_by(self):
        return self.enrolled

    def get_lecture(self, number):
        if number > self.number_of_lectures:
            raise AssertionError('Invalid lecture number')
        return self.lectures[number-1]

    def get_homeworks(self):
        return_list = []
        for hws in self.homeworks:
            if self.homeworks.get(hws).description is not None:
                return_list.append(self.homeworks.get(hws))
        return return_list


class Lecture:
    def __init__(self, name, number, teacher, course_name):
        self.number = number
        self.teacher = teacher
        self.name = name
        self.course_name = course_name

    def get_homework(self):
        if self.course_name.homeworks.get(self.number).description is not None:
            return self.course_name.homeworks.get(self.number)
        return None

    def set_homework(self, hw):
        self.course_name.homeworks[self.number] = hw
        for stud in self.course_name.enrolled:
            stud.assigned_homeworks.append(hw)

    def new_teacher(self, new_teacher):
        self.teacher = new_teacher
        self.teacher.all_courses.append(self.course_name)
        self.teacher.all_lectures.append(self)
        self.teacher.lectures.append(self)


class Homework:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.homeworks_for_check = {}

    def __str__(self):
        return f"{self.name}: {self.description}"

    def done_by(self):
        return self.homeworks_for_check


class Student:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self._last_name = last_name
        self.assigned_homeworks = []
        self.course = None

    def __str__(self):
        return f"Student: {self.first_name} {self._last_name}"

    def enroll(self, course_name):
        course_name.enrolled.append(self)
        self.course = course_name

    def do_homework(self, home_w):
        for hw in self.assigned_homeworks:
            if hw == home_w:
                home_w.homeworks_for_check.setdefault(self, None)
                self.course.teacher.homeworks_to_check.append(home_w)
                self.assigned_homeworks.remove(hw)

    @property
    def last_name(self):
        return self._last_name


class Teacher:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.all_courses = []
        self.all_lectures = []
        self.lectures = []
        self.homeworks_to_check = []

    def __str__(self):
        return f"Teacher: {self.first_name} {self.last_name}"

    def teaching_lectures(self):
        for elem in self.all_courses:
            index = 0
            while index != elem.number_of_lectures:
                for el in elem.lectures:
                    if el.teacher == self and el not in self.lectures:
                        self.lectures.append(el)

                    if el.teacher != self and el in self.lectures:

                        self.lectures.remove(el)
                    index += 1
        return self.lectures

    def check_homework(self, hw, inc_student, mark):
        if 0 > mark > 100:
            raise AssertionError('Invalid mark')
        if inc_student not in hw.homeworks_for_check:
            raise ValueError('Student never did that homework')
        if hw.homeworks_for_check[inc_student] is not None:
            raise ValueError('You already checked that homework')
        for st in hw.homeworks_for_check:
            if st == inc_student:
                hw.homeworks_for_check[inc_student] = mark
                self.homeworks_to_check.remove(hw)
                return


if __name__ == '__main__':
    main_teacher = Teacher('Thomas', 'Anderson')
    assert str(main_teacher) == f'Teacher: {main_teacher.first_name} {main_teacher.last_name}'

    python_basic = Course('Python basic', '31.10.2022', 16, main_teacher)
    assert len(python_basic.lectures) == python_basic.number_of_lectures
    assert str(python_basic) == 'Python basic (31.10.2022)'
    assert python_basic.teacher == main_teacher
    assert python_basic.enrolled_by() == []
    assert main_teacher.teaching_lectures() == python_basic.lectures

    students = [Student('John', 'Doe'), Student('Jane', 'Doe')]
    for student in students:
        assert str(student) == f'Student: {student.first_name} {student.last_name}'
        student.enroll(python_basic)

    assert python_basic.enrolled_by() == students
    third_lecture = python_basic.get_lecture(3)
    assert third_lecture.name == 'Lecture 3'
    assert third_lecture.number == 3
    assert third_lecture.teacher == main_teacher
    try:
        python_basic.get_lecture(17)
    except AssertionError as error:
        assert error.args == ('Invalid lecture number',)

    third_lecture.name = 'Logic separation. Functions'
    assert third_lecture.name == 'Logic separation. Functions'
    assert python_basic.get_homeworks() == []
    assert third_lecture.get_homework() is None
    functions_homework = Homework('Functions', 'what to do here')
    assert str(functions_homework) == 'Functions: what to do here'
    third_lecture.set_homework(functions_homework)
    assert python_basic.get_homeworks() == [functions_homework]
    assert third_lecture.get_homework() == functions_homework

    for student in students:
        assert student.assigned_homeworks == [functions_homework]

    assert main_teacher.homeworks_to_check == []
    students[0].do_homework(functions_homework)
    assert students[0].assigned_homeworks == []
    assert students[1].assigned_homeworks == [functions_homework]

    assert functions_homework.done_by() == {students[0]: None}
    assert main_teacher.homeworks_to_check == [functions_homework]
    # for mark in (-1, 101):
    #     try:
    #         main_teacher.check_homework(functions_homework, students[0], mark)
    #     except AssertionError as error:
    #         assert error.args == ('Invalid mark',)
    main_teacher.check_homework(functions_homework, students[0], 100)
    assert main_teacher.homeworks_to_check == []
    assert functions_homework.done_by() == {students[0]: 100}
    try:
        main_teacher.check_homework(functions_homework, students[0], 100)
    except ValueError as error:
        assert error.args == ('You already checked that homework',)

    try:
        main_teacher.check_homework(functions_homework, students[1], 100)
    except ValueError as error:
        assert error.args == ('Student never did that homework',)

    substitute_teacher = Teacher('Agent', 'Smith')
    fourth_lecture = python_basic.get_lecture(4)
    assert fourth_lecture.teacher == main_teacher

    fourth_lecture.new_teacher(substitute_teacher)
    assert fourth_lecture.teacher == substitute_teacher
    assert len(main_teacher.teaching_lectures()) == python_basic.number_of_lectures - 1
    assert substitute_teacher.teaching_lectures() == [fourth_lecture]
    assert substitute_teacher.homeworks_to_check == []
