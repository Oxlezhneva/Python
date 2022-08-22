

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress and grade <= 10:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _average(self):
        list2 = []
        for i in self.grades.values():
            for k in i:
                list2.append(k)
        average_mean = round(sum(list2)/len(list2), 1)         
        return average_mean      

    def __str__(self):
        res = f'Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за домашние задания: {self._average()}\
        \nКурсы в процессе изучения: {", ".join(self.courses_in_progress)}\
        \nЗавершенные курсы: {", ".join(self.finished_courses)}'
        return res        

    def __lt__(self, other):
        if not  isinstance(other, Student):
            print('Сравнение невозможно')
            return
        return self._average()<other._average()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
   
    def _average(self):
        list1 = []
        for i in self.grades.values():
            for k in i:
                list1.append(k)
        average_mean = round(sum(list1)/len(list1), 1)         
        return average_mean    

    def __str__(self):
        res = f'Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за лекции: {self._average()}'
        return res

    def __lt__(self, other):
        if not  isinstance(other, Lecturer):
            print('Сравнение невозможно')
            return
        return self._average()<other._average()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress  and grade <= 10:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'Имя: {self.name} \nФамилия: {self.surname}'
        return res



stud_ivan_petrov = Student('Иван', 'Петров', 'your_gender')
stud_ivan_petrov.courses_in_progress += ['Python', 'Git']
stud_ivan_petrov.finished_courses+= ['C++', 'JavaScript']

stud_denis_dmitrienko = Student('Денис', 'Дмитриенко', 'your_gender')
stud_denis_dmitrienko.courses_in_progress += ['Python', 'Git']
stud_denis_dmitrienko.finished_courses+= ['Программирование', 'Java']

lec_maxim_arov = Lecturer('Максим', 'Аров')
lec_maxim_arov.courses_attached += ['Python', 'Git']

lec_artem_durov = Lecturer('Артем', 'Дуров')
lec_artem_durov.courses_attached += ['Python', 'Git', 'C++', 'JavaScript']

rev_anna_tipina = Reviewer('Анна', 'Типина')
rev_anna_tipina.courses_attached += ['Python','Git', 'C++']

rev_irina_rodnina = Reviewer('Ирина', 'Роднина')
rev_irina_rodnina.courses_attached += ['Python', 'JavaScript']

stud_ivan_petrov.rate_hw(lec_maxim_arov, 'Python', 10)
stud_ivan_petrov.rate_hw(lec_maxim_arov, 'Python', 9)
stud_ivan_petrov.rate_hw(lec_maxim_arov, 'Python', 9)
stud_ivan_petrov.rate_hw(lec_maxim_arov, 'Git', 9)
stud_ivan_petrov.rate_hw(lec_maxim_arov, 'Git', 10)
stud_ivan_petrov.rate_hw(lec_maxim_arov, 'Git', 8)

stud_denis_dmitrienko.rate_hw(lec_artem_durov, 'Python', 9)
stud_denis_dmitrienko.rate_hw(lec_artem_durov, 'Python', 9)
stud_denis_dmitrienko.rate_hw(lec_artem_durov, 'Python', 10)
stud_denis_dmitrienko.rate_hw(lec_artem_durov, 'Git', 9)
stud_denis_dmitrienko.rate_hw(lec_artem_durov, 'Git', 9)
stud_denis_dmitrienko.rate_hw(lec_artem_durov, 'Git', 10)


rev_anna_tipina.rate_hw(stud_ivan_petrov, 'Python', 10)
rev_anna_tipina.rate_hw(stud_ivan_petrov, 'Python', 10)
rev_anna_tipina.rate_hw(stud_ivan_petrov, 'Python', 10)
rev_anna_tipina.rate_hw(stud_ivan_petrov, 'Git', 9)
rev_anna_tipina.rate_hw(stud_ivan_petrov, 'Git', 9)
rev_anna_tipina.rate_hw(stud_ivan_petrov, 'Git', 10)

rev_irina_rodnina.rate_hw(stud_denis_dmitrienko, 'Python', 9)
rev_irina_rodnina.rate_hw(stud_denis_dmitrienko, 'Python', 9)
rev_irina_rodnina.rate_hw(stud_denis_dmitrienko, 'Python', 9)
rev_irina_rodnina.rate_hw(stud_denis_dmitrienko, 'Git', 9)
rev_irina_rodnina.rate_hw(stud_denis_dmitrienko, 'Git', 9)
rev_irina_rodnina.rate_hw(stud_denis_dmitrienko, 'Git', 9)


print(rev_anna_tipina)
print()
print(rev_irina_rodnina)
print()
print(lec_maxim_arov)
print()
print(lec_artem_durov)
print()
print(stud_ivan_petrov)
print()
print(stud_denis_dmitrienko)
print()

print(f'Средняя оценка за лекции {lec_maxim_arov.name} {lec_maxim_arov.surname} > cредняя оценка за лекции {lec_artem_durov.name} {lec_artem_durov.surname} - {lec_maxim_arov>lec_artem_durov}')
print(f'Средняя оценка за домашнее задание {stud_ivan_petrov.name} {stud_ivan_petrov.surname} > cредняя оценка за домашнее задание {stud_denis_dmitrienko.name} {stud_denis_dmitrienko.surname} - {stud_ivan_petrov>stud_denis_dmitrienko}')


student = [stud_ivan_petrov, stud_denis_dmitrienko]
lector = [lec_artem_durov, lec_maxim_arov]

def stud_average_grade(stud, cource):
    list3 =[]
    for i in stud:
        if cource in i.grades:
            for k in i.grades[cource]:
                list3.append(k)
    average_m = round(sum(list3)/len(list3), 1)             
    return average_m
    

def lec_average_grade(lect, cource):
    list4 =[]
    for i in lect:
        if cource in i.grades:
            for k in i.grades[cource]:
                list4.append(k)
    average_m = round(sum(list4)/len(list4), 1)             
    return average_m


print(f'Средняя оценка за домашние задания по всем студентам курса Python {stud_average_grade(student, "Python")}')
print(f'Средняя оценка за домашние задания по всем студентам курса Git {stud_average_grade(student, "Git")}')
print(f'Средняя оценка за за лекции всех лекторов курса Git {lec_average_grade(lector, "Git")}')
print(f'Средняя оценка за за лекции всех лекторов курса Python {lec_average_grade(lector, "Python")}')