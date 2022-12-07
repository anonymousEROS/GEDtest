"""
GEDCOM parser design

Create empty dictionaries of individuals and families
Ask user for a file name and open the gedcom file
Read a line
Skip lines until a FAM or INDI tag is found
    Call functions to process those two types

Processing an Individual
Get pointer string
Make dictionary entry for pointer with ref to Person object
Find name tag and identify parts (surname, given names, suffix)
Find FAMS and FAMC tags; store FAM references for later linkage
Skip other lines

Processing a family
Get pointer string
Make dictionary entry for pointer with ref to Family object
Find HUSB WIFE and CHIL tags
    Add included pointers to Family object
Skip other lines

Testing to show the data structures:
    Print descendant chart after all lines are processed
    Print info from the collections of Person and Family objects
    
Jaidan Dovala/
c3400
16 April 2022
FamilyTree.py
Family Tree that lets user perform miltiple operations on a .GED file

    All of the code you turn in must have been written by you without immediate 
reference to another solution to the problem you are solving.  That means that you can look at 
other programs to see how someone solved a similar problem, but you shouldn't have any code 
written by someone else visible when you write yours (and you shouldn't have looked at a 
solution just a few seconds before you type!).  You should compose the code you write based on 
your understanding of how the features of the language you are using can be used to implement 
the algorithm you have chosen to solve the problem you are addressing.  Doing it this way is 
"real programming" - in contrast to just trying to get something to work by cutting and pasting 
stuff you don't actually understand.  It is the only way to achieve the learning objectives of the 
course. 

"""

#-----------------------------------------------------------------------



from collections import namedtuple


class Person():
    # Stores info about a single person
    # Created when an Individual (INDI) GEDCOM record is processed.
    #-------------------------------------------------------------------

    def __init__(self, ref):
        # Initializes a new Person object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._asSpouse = []  # use a list to handle multiple families
        self._asChild = None
        self._birth = None
        self._death = None
       
    def addName(self, names):
        # Extracts name parts from a list of name and stores them
        self._given = names[0]
        self._surname = names[1]
        self._suffix = names[2]
    
    def addIsSpouse(self, famRef):
        # Adds the string (famRef) indicating family in which this person
        # is a spouse, to list of any other such families
        self._asSpouse += [famRef]

    def addIsChild(self, famRef):
        # Stores the string (famRef) indicating family in which this person
        # is a child
        self._asChild = famRef

    def printDescendants(self, prefix=''):
        # print info for this person and then call method in Family
        print(prefix,end='')
        print(self)
        # recursion stops when self is not a spouse
        for fam in self._asSpouse:
            families[fam].printFamily(self._id,prefix)

    def name (self):
        # returns a simple name string 
        return self._given + ' ' + self._surname.upper() \
               + ' ' + self._suffix

    def isDescendant(self, descendant):
        # check if the identified person is an descendant of self
        if self._id == descendant:
            return True
        else:
            if self.helper1(descendant):
                return True
            else:
                return False

    def helper1(self, descendant):
        # helper function for isDescendant 
        for fam in self._asSpouse:
            for child in families[fam]._children:
                if persons[child]._id == descendant:
                    return True
                else:
                    if persons[child].helper1(descendant):
                        return True

    def printAncestors(self, space):
        #prints every ancestor of self
        if not self._asChild:
            print("0", self)
        else:
            self.helper2(space, 0)

    def helper2(self, space, num):
        # helper function for printAncestors, post order
        if num != 0:
            space += '   '
        if self._asChild:
            persons[families[self._asChild]._spouse1].helper2(space, num + 1)
            persons[families[self._asChild]._spouse2].helper2(space, num + 1)
            print(space + str(num), persons[self._id])
        else:
            print(space + str(num), persons[self._id])
            
    def addBirth(self, birth):
        #Stores the Event birth indicating the birth of this person 
        self._birth = birth
    
    def addDeath(self, death):
        #Stores the Event death indicating the death of this person
        self._death = death

    def printCousins(self, n = 1):
        # print nth cousins
        parentList = list()
        toExcludeList = list()
        siblingList = list()
        cousinList = list()

        parentList = self.getParent(parentList, toExcludeList, n)
        siblingList = self.getSibling(parentList, toExcludeList, siblingList)
        for child in siblingList:
            persons[child].getCousin(cousinList, n)
        self.printCousinResult(cousinList, n)

    def getParent(self, parentList, toExcludeList, n):
        # get parents 
        if self._asChild is not None:
            if n > 0:
                if n == 1:
                    toExcludeList.append(families[self._asChild]._spouse1)
                    toExcludeList.append(families[self._asChild]._spouse2)
                persons[families[self._asChild]._spouse1].getParent(parentList, toExcludeList, n - 1)
                persons[families[self._asChild]._spouse2].getParent(parentList, toExcludeList, n - 1)
                return parentList
            elif n == 0:
                return parentList.append(self._asChild)
        else:
            return []

    def getSibling(self, parentList, toExcludeList, siblingList):
        # get sibling of the parent
        for child in parentList:
            for sibling in families[child]._children:
                if sibling not in toExcludeList:
                    siblingList.append(sibling)
        return siblingList

    def getCousin(self, cousinList, n):
        # get cousins
        if self._asSpouse:
            for child in self._asSpouse:
                for cousin in families[child]._children:
                    if n > 1:
                        persons[cousin].getCousin(cousinList, n - 1)
                    else:
                        cousinList.append(cousin)

    def printCousinResult(self, cousinList, n):
        # print the cousins found
        if str(n)[-1] == '1':
            print(str(n) + 'st cousins for ' + self.name())
        elif str(n)[-1] == '2':
            print(str(n) + 'nd cousins for ' + self.name())
        elif str(n)[-1] == '3':
            print(str(n) + 'rd cousins for ' + self.name())
        else:
            print(str(n) + 'th cousins for ' + self.name())

        if cousinList:
            for cousin in cousinList:
                print(" ", persons[cousin])
        else:
            print('No cousins')
            
    def __str__(self):
        #return a string of person info including full name and suffix
        #birth and death info, children and spouse id
        if self._asChild: # make sure value is not None
            childString = ' asChild: ' + self._asChild
        else: childString = ''
        if self._asSpouse != []: # make sure _asSpouse list is not empty
            spouseString = ' asSpouse: ' + str(self._asSpouse)
        else: spouseString = ''

        if self._birth: #make sure birth info is available
            birthString = ' n: ' + self._birth._str_()
        else: birthString = ''
        if self._death: #make sure death info is available
            deathString = ' d: ' + self._death._str_()
        else: deathString = ''

        return self._given + ' ' + self._surname.upper()\
               + ' ' + self._suffix +birthString + deathString + childString + spouseString

    def treeInfo (self):
        # returns a string representing the structure references included in self
        if self._asChild: # make sure value is not None
            childString = ' | asChild: ' + self._asChild
        else: childString = ''
        if self._asSpouse != []: # make sure _asSpouse list is not empty
            # Use join() to put commas between identifiers for multiple families
            spouseString = ' | asSpouse: ' + ','.join(self._asSpouse)
        else: spouseString = ''
        return childString + spouseString
    
    def eventInfo(self):
        ## add code here to show information from events once they are recognized
        return ''

    def __str__(self):
        # Returns a string representing all info in a Person instance
        # When treeInfo is no longer needed for debugging it can 
        return self.name() \
                + self.eventInfo()  \
                + self.treeInfo()  ## Comment out when not needed for debugging


# end of class Person
# ---------------------------------------------------------
# stores events for date and location

class Event():
    def __init__(self):
        self._date = None
        self._place = None
        
    def addDate(self, date):
        # Stores the string (date) indicating the date of the event
        self._date = date

    def addPlace(self, place):
        # Stores the string (place) indicating the place of the event
        self._place = place


    def _str_(self):
        #return a string of the date and location of an event
        if self._date: #Date is available
            dateString = self._date.rstrip('\n')
        else:
            dateString = ''
        if self._place: #Place is available
            placeString = self._place.rstrip('\n')
        else:
            placeString = ''
    
        if dateString == '' and placeString == '':
             #Return message "No record of date and location" if there's nothing
            return 'No record of date and place'
        else:
            return dateString + ' ' + placeString

#---------------------------------------------------------
# End of Event class

#-----------------------------------------------------------------------
Spouse = namedtuple('Spouse',['personRef','tag'])

class Family():
    # Stores info about a family
    # Created when an Family (FAM) GEDCOM record is processed.
    #-------------------------------------------------------------------

    def __init__(self, ref):
        # Initializes a new Family object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._spouse1 = None
        self._spouse2 = None
        self._children = []
        self._marriagedate = ''
        self._marriageplace = ''

    def addHusband(self, personRef):
        # Stores the string (personRef) indicating the husband in this family
        self._spouse1 = personRef

    def addWife(self, personRef):
        # Stores the string (personRef) indicating the wife in this family
        self._spouse2 = personRef

    def addChild(self, personRef):
        # Adds the string (personRef) indicating a new child to the list
        self._children += [personRef]

    def addMarriageDate(self, MarriageDate):
        # Add marriage date
        self._marriagedate = MarriageDate[0:len(MarriageDate)-1]

    def addMarriagePlace(self, MarriagePlace):
        # Add marriage place
        self._marriageplace = MarriagePlace[0:len(MarriagePlace)-1]

    def printFamily(self, firstSpouse, prefix):
        # Used by printDecendants in Person to print spouse
        # and recursively invole printDescendants on children
        if prefix != '': prefix = prefix[:-2]+'  '
        if self._spouse1 == firstSpouse:
            if self._spouse2:  # make sure value is not None
                print(prefix + '+', end='')
                print(persons[self._spouse2], end='')
                if self._marriagedate:
                    print(', m: ', end='')
                    print(self._marriagedate, end=' ')
                    print(self._marriageplace)
                    
        else:
            if self._spouse1:  # make sure value is not None
                print(prefix + '+', end='')
                print(persons[self._spouse1])
        for child in self._children:
             persons[child].printDescendants(prefix+'|--')

    def __str__(self):
        # toString method
        if self._spouse1: # make sure value is not None
            husbString = ' Husband: ' + self._spouse1
        else: husbString = ''
        if self._spouse2: # make sure value is not None
            wifeString = ' Wife: ' + self._spouse2
        else: wifeString = ''
        if self._children != []: childrenString = ' Children: ' + ','.join(self._children)
        else: childrenString = ''
        return husbString + wifeString + childrenString

# end of class Family

#-----------------------------------------------------------------------
# Global dictionaries used by Person and Family to map INDI and FAM identifier
# strings to corresponding object instances

persons = dict()  # saves references to all of the Person objects
families = dict() # saves references to all of the Family objects

#-----------------------------------------------------------------------

def getPerson (personID):
    return persons[personID]

def getFamily (familyID):
    return families[familyID]

## Print functions that print the info in all Person and Family objects 
## Meant to be used in a module that tests this one
def printAllPersonInfo():
    # Print out all information stored about individuals
    for ref in sorted(persons.keys()):
        print(ref + ':' + str(persons[ref]))
    print()

def printAllFamilyInfo():
    # Print out all information stored about families
    for ref in sorted(families.keys()):
        print(ref + ':' + str(families[ref]))
    print()

def processGEDCOM(file):

    def getPointer(line):
        # A helper function used in multiple places in the next two functions
        # Depends on the syntax of pointers in certain GEDCOM elements
        # Returns the string of the pointer without surrounding '@'s or trailing
        return line[8:].split('@')[0]

    def processPerson(newPerson):
        nonlocal line
        line = f.readline()
        while line[0] != '0': # process all lines until next 0-level
            tag = line[2:6]  # substring where tags are found in 0-level elements
            if tag == 'NAME':
                names = line[6:].split('/')  #surname is surrounded by slashes
                names[0] = names[0].strip()
                names[2] = names[2].strip()
                newPerson.addName(names)
            elif tag == 'FAMS':
                newPerson.addIsSpouse(getPointer(line))
            elif tag == 'FAMC':
                newPerson.addIsChild(getPointer(line))
            # read to go to next line
            line = f.readline()
            ## add code here to look for other fields
            if tag == 'BIRT' or line[2:6] == 'BIRT':
                birth = Event()# makes Event for birth
                line = f.readline()
                if line[2:6] == 'DATE' :
                    birth.addDate(line[7:])
                    line = f.readline()
                if line[2:6] == 'PLAC' :
                    birth.addPlace(line[7:])
                line = f.readline()
                newPerson.addBirth(birth)
            
            if tag == 'DEAT' or line[2:6] == 'DEAT':
                death = Event()# makes Event for death 
                line = f.readline()
                if line[2:6] == 'DATE' :
                    death.addDate(line[7:])
                    line = f.readline()
                if line[2:6] == 'PLAC':
                    death.addPlace(line[7:])
                line = f.readline()
                newPerson.addDeath(death)

    def processFamily(newFamily):
        nonlocal line
        line = f.readline()
        while line[0] != '0':  # process all lines until next 0-level
            tag = line[2:6]
            if tag == 'HUSB':
                newFamily.addHusband(getPointer(line))
            elif tag == 'WIFE':
                newFamily.addWife(getPointer(line))
            elif tag == 'CHIL':
                newFamily.addChild(getPointer(line))
            # read to go to next line
            line = f.readline()
            ## add code here to look for other fields 
            if tag == 'MARR' or line[2:6] == 'MARR':
                line = f.readline()
                if line[2:6] == 'DATE' :
                    newFamily.addMarriageDate(line[7:])
                    line = f.readline()
                if line[2:6] == 'PLAC':
                    newFamily.addMarriagePlace(line[7:])
                    line = f.readline()

    ## f is the file handle for the GEDCOM file, visible to helper functions
    ## line is the "current line" which may be changed by helper functions

    f = open (file)
    line = f.readline()
    while line != '':  # end loop when file is empty
        fields = line.strip().split(' ')
        # print(fields)
        if line[0] == '0' and len(fields) > 2:
            # print(fields)
            if (fields[2] == "INDI"):
                ref = fields[1].strip('@')
                ## create a new Person and save it in mapping dictionary
                persons[ref] = Person(ref)
                ## process remainder of the INDI record
                processPerson(persons[ref])

            elif (fields[2] == "FAM"):
                ref = fields[1].strip('@')
                ## create a new Family and save it in mapping dictionary
                families[ref] = Family(ref)
                ## process remainder of the FAM record
                processFamily(families[ref])

            else:    # 0-level line, but not of interest -- skip it
                line = f.readline()
        else:    # skip lines until next candidate 0-level line
            line = f.readline()


def _main():
    filename = "Kennedy.ged"  # Set a default name for the file to be processed
##    Uncomment the next line to make the program interactive
    filename = input("Type the name of the GEDCOM file:")

    processGEDCOM(filename)

    printAllPersonInfo()

    printAllFamilyInfo()
    
    
    person = "I46"  # Default selection to work with Kennedy.ged file
##    Uncomment the next line to make the program interactive
    person = input("Enter person ID for descendants chart:")
    

    getPerson(person).printDescendants()
    # getPerson(person).printAncestors()
    # getPerson(person).printCousin()

    
if __name__ == '__main__':
    _main()


