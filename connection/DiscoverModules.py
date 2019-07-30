def DiscoverModules( numModules = 24 ):
    """Look for SUPERball v2 Hebi modules in the network and return their Hebi Group."""

    from hebi import Lookup
    from hebi import GroupCommand
    from time import sleep

    # Module Names on SUPERball V2 [M01 M02 ... M24]
    SBModuleNames = (['M' + str(i + 1).zfill(2) for i in xrange(numModules)])

    # Get table of all Hebi motors
    lookup = Lookup()
    sleep(2)  # gives the Lookup process time to discover modules

    # Count how many modules were found
    num_modules_found = 0
    # The following command does not work anymore on Python2 using hebi-pi > 0.99.2
    for entry in lookup.entrylist:
        num_modules_found = num_modules_found + 1

    if num_modules_found == 0:
        # No modules were found!
        raise Exception('No modules found!')
    elif num_modules_found != numModules:
        # Module number mismatch
        raise Exception('Could not find all the modules!')

    # Get the modules using the correct name order 
    GroupSB = lookup.get_group_from_names('*', SBModuleNames)

    try:
        if GroupSB.size == 0:
            # Empty group!
            raise Exception('GroupSB is empty!')
        elif GroupSB.size != numModules:
            # Module number mismatch
            raise Exception('GroupSB size mismatch!')
    except AttributeError:
        raise Exception('Attribute Error while accessing GroupSB.size')

    try:
        infoTableSB = GroupSB.request_info()
    except AttributeError:
        raise Exception('Attribute Error in GroupSB')
    
    if infoTableSB is None:
        raise Exception('infoTableSB is None!')

    try:
        print('{} module(s) found!'.format(len(infoTableSB.name)))
    except AttributeError:
        raise Exception('Attribute Error in infoTableSB')

    if len(infoTableSB.name) != numModules:
        raise Exception('Number of modules mismatch')
    
    print('SUPERball Motors Found:')
    for module in xrange(len(infoTableSB.name)):
        print(infoTableSB.name[module])

    return GroupSB