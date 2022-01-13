"""Functions to parse a file containing student data."""


from calendar import c


def all_houses(filename):
    """Return a set of all house names in the given file.

    For example:
      >>> unique_houses('cohort_data.txt')
      {"Dumbledore's Army", 'Gryffindor', ..., 'Slytherin'}

    Arguments:
      - filename (str): the path to a data file

    Return:
      - set[str]: a set of strings
    """

    houses = set()

    character_data = open(filename)
    for line in character_data:
        house = line.rstrip().split('|')[2]
        if house:
            houses.add(house)

    return houses


def students_by_cohort(filename, cohort='All'):
    """Return a list of students' full names by cohort.

    Names are sorted in alphabetical order. If a cohort isn't
    given, return a list of all students. For example:
      >>> students_by_cohort('cohort_data.txt')
      ['Adrian Pucey', 'Alicia Spinnet', ..., 'Zacharias Smith']

      >>> students_by_cohort('cohort_data.txt', cohort='Fall 2015')
      ['Angelina Johnson', 'Cho Chang', ..., 'Terence Higgs', 'Theodore Nott']

      >>> students_by_cohort('cohort_data.txt', cohort='Winter 2016')
      ['Adrian Pucey', 'Andrew Kirke', ..., 'Roger Davies', 'Susan Bones']

      >>> students_by_cohort('cohort_data.txt', cohort='Spring 2016')
      ['Cormac McLaggen', 'Demelza Robins', ..., 'Zacharias Smith']

      >>> students_by_cohort('cohort_data.txt', cohort='Summer 2016')
      ['Alicia Spinnet', 'Dean Thomas', ..., 'Terry Boot', 'Vincent Crabbe']

    Arguments:
      - filename (str): the path to a data file
      - cohort (str): optional, the name of a cohort

    Return:
      - list[list]: a list of lists
    """

    students = []

    character_data = open(filename)
    for line in character_data:
        firstname, lastname, _, _, cohort_name = line.rstrip().split('|')

        if cohort_name not in ("I", "G") and cohort in ("All", cohort_name):
            students.append(f'{firstname} {lastname}')
    return sorted(students)


def all_names_by_house(filename):
    """Return a list that contains rosters for all houses, ghosts, instructors.

    Rosters appear in this order:
    - Dumbledore's Army
    - Gryffindor
    - Hufflepuff
    - Ravenclaw
    - Slytherin
    - Ghosts
    - Instructors

    Each roster is a list of names sorted in alphabetical order.

    For example:
      >>> rosters = hogwarts_by_house('cohort_data.txt')
      >>> len(rosters)
      7

      >>> rosters[0]
      ['Alicia Spinnet', ..., 'Theodore Nott']
      >>> rosters[-1]
      ['Filius Flitwick', ..., 'Severus Snape']

    Arguments:
      - filename (str): the path to a data file

    Return:
      - list[list]: a list of lists
    """

    dumbledores_army = []
    gryffindor = []
    hufflepuff = []
    ravenclaw = []
    slytherin = []
    ghosts = []
    instructors = []

    character_data = open(filename)
    for line in character_data:
        firstname, lastname, house, _, cohort_name = line.rstrip().split('|')

        if house:
            if house == "Dumbledore's Army":
                dumbledores_army.append(f'{firstname} {lastname}')
            elif house == 'Gryffindor':
                gryffindor.append(f'{firstname} {lastname}')
            elif house == 'Hufflepuff':
                hufflepuff.append(f'{firstname} {lastname}')
            elif house == 'Ravenclaw':
                ravenclaw.append(f'{firstname} {lastname}')
            elif house == 'Slytherin':
                slytherin.append(f'{firstname} {lastname}')
        else:
            if cohort_name == "G":
                ghosts.append(f'{firstname} {lastname}')
            elif cohort_name == 'I':
                instructors.append(f'{firstname} {lastname}')
    return [sorted(dumbledores_army), sorted(gryffindor), sorted(hufflepuff), sorted(ravenclaw), sorted(slytherin), sorted(ghosts), sorted(instructors)]


def all_data(filename):
    """Return all the data in a file.

    Each line in the file is a tuple of (full_name, house, advisor, cohort)

    Iterate over the data to create a big list of tuples that individually
    hold all the data for each person. (full_name, house, advisor, cohort)

    For example:
      >>> all_student_data('cohort_data.txt')
      [('Harry Potter', 'Gryffindor', 'McGonagall', 'Fall 2015'), ..., ]

    Arguments:
      - filename (str): the path to a data file

    Return:
      - list[tuple]: a list of tuples
    """

    all_data = []

    character_data = open(filename)
    for line in character_data:
        firstname, lastname, house, advisor, cohort = line.rstrip().split('|')
        full_name = f'{firstname} {lastname}'

        all_data.append(full_name, house, advisor, cohort)

    return all_data


def get_cohort_for(filename, name):
    """Given someone's name, return the cohort they belong to.

    Return None if the person doesn't exist. For example:
      >>> get_cohort_for('cohort_data.txt', 'Harry Potter')
      'Fall 2015'

      >>> get_cohort_for('cohort_data.txt', 'Hannah Abbott')
      'Winter 2016'

      >>> get_cohort_for('cohort_data.txt', 'Someone else')
      None

    Arguments:
      - filename (str): the path to a data file
      - name (str): a person's full name

    Return:
      - str: the person's cohort or None
    """

    character_data = open(filename)
    for line in character_data:
        firstname, lastname, house, advisor, cohort = line.rstrip().split('|')
        full_name = f'{firstname} {lastname}'

        all_data.append(full_name, house, advisor, cohort)
        for full_name, _, _, cohort in all_data:
            if full_name == name:
                return cohort
            else:
                return None


def find_duped_last_names(filename):
    """Return a set of duplicated last names that exist in the data.

    For example:
      >>> find_name_duplicates('cohort_data.txt')
      {'Creevey', 'Weasley', 'Patil'}

    Arguments:
      - filename (str): the path to a data file

    Return:
      - set[str]: a set of strings
    """

    duplicates = set()
    appeared = set()

    for full_name, _, _, _ in all_data(filename):
        last = full_name.split(' ')[-1]

        if last in appeared:
            duplicates.add(last)

        appeared.add(last)

    return duplicates


def get_housemates_for(filename, name):
    """Return a set of housemates for the given student.

    Given a student's name, return a list of their housemates. Housemates are
    students who belong to the same house and were in the same cohort as the
    given student.

    For example:
    >>> get_housemates_for('cohort_data.txt', 'Hermione Granger')
    {'Angelina Johnson', ..., 'Seamus Finnigan'}
    """

    housemates = set()

    target = None
    for person in all_data(filename):
        full_name, house, advisor, cohort = person

        if full_name == name:
            target = person
            break

    if target:
        target_name, target_house, _, target_cohort = target

        for full_name, house, _, cohort_name in all_data(filename):
            if ((house, cohort_name) == (target_house, target_cohort) and
                    full_name != name):
                housemates.add(full_name)

    return housemates


##############################################################################
# END OF MAIN EXERCISE.  Yay!  You did it! You Rock!
#

if __name__ == '__main__':
    import doctest

    result = doctest.testfile('doctests.py',
                              report=False,
                              optionflags=(
                                  doctest.REPORT_ONLY_FIRST_FAILURE
                              ))
    doctest.master.summarize(1)
    if result.failed == 0:
        print('ALL TESTS PASSED')
