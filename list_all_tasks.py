def listCASATasks():
    """
    Return a list of all the CASA tasks.

    This function requires casapy modlue tasks.
    """
    from tasks import allcat
    all_tasks=[]
    for key in allcat.keys():
        for taskname in allcat[key]:
            if (taskname[0] == '(') or (taskname[0]=='{'):            
                length = len(taskname)
                taskname = taskname[1:length-2]
            if (taskname in all_tasks) == False:            
                all_tasks.append(taskname)
    all_tasks.sort()
    return all_tasks
