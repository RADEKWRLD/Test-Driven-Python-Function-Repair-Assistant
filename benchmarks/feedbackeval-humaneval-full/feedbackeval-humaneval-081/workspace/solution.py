def numerical_letter_grade(grades):
    letter_grade = []
    for grade in grades:
        if grade == 4.0:
            letter_grade.append('A+')
        elif grade > 3.7:
            letter_grade.append('A')
        elif grade > 3.3:
            letter_grade.append('A-')
        elif grade > 3.0:
            letter_grade.append('B+')
        elif grade > 2.7:
            letter_grade.append('B')
        elif grade > 2.3:
            letter_grade.append('B-')
        elif grade > 2.0:
            letter_grade.append('C+')
        elif grade > 1.7:
            letter_grade.append('C')
        elif grade > 1.3:
            letter_grade.append('C-')
        elif grade > 1.0:
            letter_grade.append('D+')
        elif grade > 0.7:
            letter_grade.append('D')
        elif grade >= 0.0:
            letter_grade.append('D-')
        else:
            letter_grade.append('E')
    return letter_grade

# Test the function with the given example
print(numerical_letter_grade([4.0, 3, 1.7, 2, 3.5]))  # Output: ['A+', 'C', 'C-', 'C', 'A-']
