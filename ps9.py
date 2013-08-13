# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    subject={}
    inputFile = open(filename)
    for line in inputFile:
        
        split_line=line.split(',')
        subject[split_line[0]]=(int(split_line[1]),int(split_line[2].replace("\n","")))

    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).
    return subject

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    # TODO...
    if subInfo1[0]>subInfo2[0]:
        return True
    else:
        return False

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    # TODO...
    if subInfo1[1]<subInfo2[1]:
        return True
    else:
        return False

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    # TODO...
    ##print str(subInfo1)
    ##print str(subInfo2)
    m1=float(float(subInfo1[0])/float(subInfo1[1]))
    m2=float(float(subInfo2[0])/float(subInfo2[1]))
    if m1 > m2:
        return True
    else:
        return False

def calTotalWork(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        totalVal += val
        totalWork += work
    return totalWork

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    done=0
    subNames = subjects.keys()
    subNames.sort()
    max_index=''
    schedule={}
    
    ##main loop
    while done!=1:
        max_val_work=subjects[subNames[0]]
        max_index=subNames[0]
        for s in subNames:
            val_work = subjects[s]
            ##print str(val_work)
            ##print str(max_val_work)
            if comparator(val_work,max_val_work):
                ##print 'found new max value'
                max_val_work=val_work
                max_index=s
        ##check if schedule appended with new work is less then maxwork
        ##if so append schedule and remove subject from list of possible keys
        ##print str(max_val_work[1])
        ##print str(schedule)
        if schedule=={} and (max_val_work[1] <= maxWork):
            schedule[max_index]=subjects[max_index]
        if schedule=={} and (max_val_work[1] > maxWork):
            pass
        elif (calTotalWork(schedule)+max_val_work[1]) <= maxWork:
            schedule[max_index]=subjects[max_index]
        subNames.remove(max_index)
        if len(subNames)==0:
            done=1
    return schedule

#
# Problem 3: Subject Selection By Brute Force
#
def Denary2Binary(n,padding):
    '''convert denary integer n to binary string bStr'''
    bStr = ''
    if n < 0:  raise ValueError, "must be a positive integer"
    if n == 0:
        bStr='0'
        return (padding-len(bStr))*'0'+bStr
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    
    return (padding-len(bStr))*'0'+bStr
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    allSolutions=[]
    tempKeys=[]
    eList=[]
    subNames = subjects.keys()
    subNames.sort()
    totalVal, totalWork = 0,0
    totals=[]
    result={}
    ##create enumerated list of all possible solutions
    for i in xrange(0,2**len(subjects)):
        eList.append(Denary2Binary(i,len(subjects)))
        tempKeys=[]
        for j in xrange(0,len(eList[i])):
            if eList[i][j]=='1':
                tempKeys.append(subNames[j])
        allSolutions.append(tempKeys)

    ##sum up work & value from enumerated list
    for i in xrange(0,len(allSolutions)):
        totalVal, totalWork = 0,0
        for j in xrange(0,len(allSolutions[i])):
            (val,work)=subjects[allSolutions[i][j]]
            totalVal+=val
            totalWork+=work
        totals.append([totalVal,totalWork])
    ##find max value under threshold
    maxVal=totals[0][0]
    iMaxVal=0
    for i in xrange(0,len(totals)):
        ##print totals[i]
        if totals[i][1]<=maxWork and totals[i][0]>maxVal:
            maxVal=totals[i][0]
            iMaxVal=i
    ##print 'max Val ' + str(maxVal)
    ##print 'index '+ str(iMaxVal)
    ##print 'courses ' +str(allSolutions[iMaxVal])
    for i in xrange(0,len(allSolutions[iMaxVal])):
        result[allSolutions[iMaxVal][i]]=subjects[allSolutions[iMaxVal][i]]
    return result
                    
                    
        
    
                        
                        


