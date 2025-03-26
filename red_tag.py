import red_tag_classes
import red_tag_CLI
import red_tag_test_utils
import csv

import ast
"""
This is red_tag. It will simulate the job of a red tag by creating a rotation at a specified ride
It will take into account minor breaks, violations, and a relatively fair rotation
"""
ROTATION_LENGTH = 45
def gather_ride_data():
    #map the presets to their setting function. If a recognised name is entered, the appropriate function is mapped
    presets = {'laff trakk' : set_laff_trakk, 'ferris wheel' : set_ferris_wheel, 'wheel' : set_ferris_wheel, 'lightning racer' : set_racer, 'racer' : set_racer, 'wildcat': set_wild_cat, 'cat' : set_wild_cat, 'wild mouse' : set_wild_mouse,
    'mouse': set_wild_mouse, 'tidal force' : set_tidal_force, 'breakers edge' : set_breakers_edge, "breaker's edge" : set_breakers_edge, 'fahrenheit' : set_fahrenheit}
    print ('Welcome to Red Tag! We are going to gather some info about your ride.')
    
    name = input('Please enter the name of your ride:')

    #Check for presets 
    for preset in presets:
        if name.lower() == preset:

            use = ''
            while use.lower() != 'y' and use.lower() != 'n':
                use = input('We have found a preset option for ' + preset +  ' Would you like to use this option? Press y to use or n to enter data manually')
            if use.lower() == 'n':
                break
            else:
                #Call the preset and return ride and count
                ride, count = presets[preset]()
                return ride, count

    #Get a value for mins
    while True:
        try:
            mins = int(input('Please enter the minimum number of people required to operate this ride:'))
            break
        except ValueError:
            print ("Please enter a number")
    ride = red_tag_classes.Ride(name, mins) #Create a ride object

    count = mins #Only used to determine if any additional positions are added besides mins
    print('You will now add the positions for this ride. You must add at least the minimum number of position you specified earlier')
    for _ in range(mins):
        ride.add_pos() #Adding a position belongs to the ride class.
    while True:
        cout = ''
        while cout.lower() != 'y' and cout.lower() != 'n':
            cout = input('You have now achieved mins. Would you like to add an additional position? This can be changed later. Please enter Y or N.')
        if cout == 'Y' or cout == 'y':
            ride.add_optional_pos() #Adding an optional position belongs to the ride class
            count +=1
        else:
            break
        
    return ride, count

"""
Each of the set functions will first create a ride object with the correct name and mins
It will then add the positions specific for that ride. Only mandatory positions are added
The ride and its min value are then returned
Only one of these is called on a run (or zero if a ride is entered manually)
"""
def set_ferris_wheel():
    ride = red_tag_classes.Ride('Wheel',3)
    ride.add_to_dict('Load', [None, False, False])
    ride.add_to_dict('Unload', [None, True, False])
    ride.add_to_dict('Operate', [None, True, False])
    return ride, 3
def set_laff_trakk():
    ride = red_tag_classes.Ride('Laff Trakk', 7)
    ride.add_to_dict('Load', [None, True, False])
    ride.add_to_dict('Unload', [None, True, False])
    ride.add_to_dict('Dispatch', [None, True, False])
    ride.add_to_dict('Operate', [None, True, False])
    ride.add_to_dict('Grouper', [None, False, False])
    ride.add_to_dict('Merger', [None, False, True])
    ride.add_to_dict('Frontline', [None, False,True])
    return ride, 7
def set_racer():
    ride = red_tag_classes.Ride("Lightning Racer" , 6)
    ride.add_to_dict("Merger", [None, False, False])
    ride.add_to_dict("Operate" , [None, True, False])
    ride.add_to_dict("Lightning Attend",[None, True, False] )
    ride.add_to_dict('Lightning Dispatch', [None, True, False])
    ride.add_to_dict("Thunder Attend",[None, True, False] )
    ride.add_to_dict('Thunder Dispatch', [None, True, False])
    return ride, 6
def set_tidal_force():
    ride = red_tag_classes.Ride("Tidal Force" , 3)
    ride.add_to_dict('Dispatch' , [None, False, False])
    ride.add_to_dict("Attend", [None, True, False])
    ride.add_to_dict('Operate', [None, True, False])
    return ride, 3
def set_breakers_edge():
    ride = red_tag_classes.Ride("Breaker's Edge", 12)
    ride.add_to_dict('Zone 1', [None, False, False])
    ride.add_to_dict('Zone 2', [None, False, False])
    ride.add_to_dict('Zone 3', [None, False, False])
    ride.add_to_dict('Zone 4', [None, False, False])
    ride.add_to_dict('Zone 5', [None, False, False])
    ride.add_to_dict("Frontline", [None, False, False])
    ride.add_to_dict('Merger', [None, False, False])
    ride.add_to_dict('Weigh Station', [None, False, False])
    ride.add_to_dict('Load', [None, True, False])
    ride.add_to_dict('Unload', [None, True, False])
    ride.add_to_dict('Operate', [None, True, False])
    ride.add_to_dict("Crow's Nest", [None, False,  False])
    return ride, 12
def set_wild_mouse():
    ride = red_tag_classes.Ride("Wild Mouse" , 4)
    ride.add_to_dict('Merger', [None, False, True])
    ride.add_to_dict('Load', [None, True, False])
    ride.add_to_dict('Operate', [None, True, False])
    ride.add_to_dict('Unload', [None, False, False])
    return ride, 4
def set_wild_cat():
    ride = red_tag_classes.Ride('Wildcat',  4)
    ride.add_to_dict('Merger' , [None, False, True])
    ride.add_to_dict('Attend',[None, False, False])
    ride.add_to_dict('Dispatch', [None, True, False])
    ride.add_to_dict('Operate' , [None, True, False])
    return ride, 4
def set_fahrenheit():
    ride = red_tag_classes.Ride('Fahrenheit', 5)
    ride.add_to_dict('Frontline', [None, False, True])
    ride.add_to_dict('Merger', [None, False, False])
    ride.add_to_dict('Load Side Attend', [None, False, False])
    ride.add_to_dict("Exit Side Attend" , [None, True, False])
    ride.add_to_dict('Operate', [None, True, False])
    return ride, 5

def gather_park_data():
    print("\033[32mJust a few quick questions about the park hours!\033[0m")
    
    #Idiot-check loop to ensure they input a valid time format for park start
    p_start = ''
    while (len(p_start.split(':')) != 2):
        p_start = input('What time does the park open? Please enter in military time in the form HH:MM')
    p_start = p_start.split(':')
    p_start = red_tag_classes.Time(int(p_start[0]),int(p_start[1])) #Put it into a Time object

    #same thing as above for ending time
    p_end = ''
    while (len(p_end.split(':')) != 2):
        p_end = input('And what time does the park end? Please enter in the same format')
    p_end = p_end.split(':')
    p_end = red_tag_classes.Time(int(p_end[0]),int(p_end[1]))

    return p_start, p_end
def gather_employee_data(number_positions, p_start, p_end, ride):
    print ("\033[32mGreat! Let's gather some info about your operators! Don't forget to include yourself in this list (you're important too!)\033[0m")
    
    employee_list = [] #An empty list to startw with
    iterations = number_positions #Copying the variable to do arithmetic with later in the process

    #Idiot check loop for the csv option
    csv_option = ''
    while csv_option.lower() != 'y' and csv_option.lower() != 'n':
        csv_option = input('\033[33mWould you like to input employee data from a csv file? Please enter y or n\033[0m')
    
    #If they are reading from CSV, get the name of the file
    if csv_option.lower() == 'y':
        file_name = input('Please enter the name of the CSV file you would like to read data from')
        try:
            with open(file_name) as csv_file:
                csv_reader = csv.reader(csv_file)
                switchover = False
                for line in csv_reader:
                    if not switchover:
                        #Split the shift start and end times into tokens 
                        e_start = line[2].split(':')
                        e_end = line[3].split(':')
                        #Create a new employee object using the data in the line. Create a new Time object for shift start/end 
                        current = red_tag_classes.Employee(line[0],line[1], red_tag_classes.Time(int(e_start[0]),int(e_start[1])), red_tag_classes.Time(int(e_end[0]), int(e_end[1])))

                        #Reassemble the untrained positions
                        line[4] = line[4:]
                        current.set_untrained_positions(line[4]) # Add the untrained positions
                        employee_list.append(current)
                        #If we have more employees than positions, break out
                        if len(employee_list) > len(ride.get_pos_dict()) + len(ride.get_optional_pos_dict()):
                            print('\033[31mThere are more employees than positions in this file. Additional employees will be ignored\033[0m')
                            break
                    else:
                        #The switchover has not occured yet. This is a position we need to add
                        if line[0] == '-':
                            switchover = True
                            continue
                        ride.add_pos_csv(line[0], line[1], line[2])

        except FileNotFoundError:
            print ('\033[31mFile not found! Please enter data manually\033[0m')

    #Determine if we need to add more employees manually
    iterations = number_positions - len(employee_list)
    if iterations <0: 
        iterations = 0
    if iterations != number_positions and iterations != 0:
        print('\033[31mThere were not enough employees listed in the CSV file to fill all positions. You need an additional ', iterations, 'people. Please enter their info manually\033[0m')

    #If we need more employees, proceed to enter them manually
    #If the csv option is not used iterations will equal number of positions
    for _ in range(iterations):
        name = input("Please enter the employee's name. If they are the lead, please name them 'Lead'")
        
        #Idiot check loop to ensure they enter a numerical value for age
        while True:
            age = input ('How old is ' + name + '?')
            try:
                int(age)
                break
            except ValueError:
                print('\033[31mPlease enter a value\033[0m')

        # Add any positions they should avoid
        avoid_list = []
        avoid_pos = input('Are there any positions that this person is not trained on? Please enter one position per line or press enter to continue: ')
        while avoid_pos != '':
            avoid_list.append(avoid_pos)
            avoid_pos = input('Are there any positions that this person is not trained on? Please enter one position per line or press enter to continue: ')
        
 
        #Idiot check loop to make sure they enter y or n for entire day question
        shift_start_q = ''
        while shift_start_q.lower() != 'y' and shift_start_q.lower() != 'n':
            shift_start_q = input('Are they working the entire day? Please enter Y or N.')
        if shift_start_q == 'Y' or shift_start_q == 'y':
            #Creates an employee object with shift time half hour before open to half hour past close
            current = red_tag_classes.Employee(name, age, p_start.subtract(red_tag_classes.Time(0,30)), p_end.add(red_tag_classes.Time(0,30)))
        else:

            #Idiot check loop to ensure they enter a valid time format for start
            e_start = ''
            while (len(e_start.split(':')) != 2):
                e_start = input('What time does this employee start their shift?')
            e_start = e_start.split(':')
            e_start = red_tag_classes.Time(int(e_start[0]), int(e_start[1])) #Put the input into a time object

            #Idiot check loop for shift end 
            e_end = ''
            while (len(e_end.split(':')) != 2):
                e_end = input('What time does this employee end their shift?')
            e_end = e_end.split(':')
            e_end = red_tag_classes.Time(int(e_end[0]), int(e_end[1])) #Put the impout into a time object
            current = red_tag_classes.Employee(name, age, e_start, e_end) #Create an employee object with all the info we just collected
        
        current.set_untrained_positions(avoid_list) # Set the untrained positions
        employee_list.append(current) #Add the new employee to the list


    #TODO: Get ride of this code
    calculate_position_availability(employee_list, ride)

        

    #Find the lead and make sure they are marked as not needing a break. 
    # TODO: Create lead break logic - if 2 leads are present they can break themselves, but gotta make sure at least 1 is present at all times
    lead = find_employee_in_list(employee_list, 'Lead')
    lead.set_break_status(True)
    return employee_list


def calculate_position_availability(employee_list, ride):
    #Begin by getting all positions in one list
    all_positions = list(ride.get_pos_dict().keys()) + list(ride.get_optional_pos_dict().keys())

    position_availability = {}
    # Determine List of employees for each positions. Create a dictionary where the key is the position
    # and the value is the list of employees that can do it

    for position in all_positions:
        position_availability[position.lower()] = []
        for employee in employee_list:
            if position.lower() not in employee.get_untrained_positions():
                position_availability[position.lower()].append(employee.get_name())

    
    return position_availability



"""
This function returns a list of all the breaks that need completed in order
"""
def make_break_list(employee_list, number_positions):
    duplicate = employee_list.copy() #Create a duplicate of the employee list to work with
    return_list = []
    for _ in range(len(employee_list)):
        max_time = red_tag_classes.Time(24,00) #A maximum time value
        current_lowest_employee = 1 #This variable will hold the employee object with the first brak time
        lowest_index = 0 #This will be the index of the lowest employee
        for i in range(len(duplicate)):
            potential_employee = duplicate[i] #The current employee
            current_break_start = potential_employee.get_break_window()[0]
            if current_break_start < max_time and current_break_start != red_tag_classes.Time(0,0):
                #They need a break, and it is earlier than any other found thus far. Set all variables
                max_time = current_break_start
                current_lowest_employee = potential_employee
                lowest_index = i
        if current_lowest_employee.get_name().lower() == 'lead':
            duplicate.pop(lowest_index) #Remove the lead, we don't need to deal with them
            continue #Continue on without adding them to the return_list
        return_list.append(current_lowest_employee) #Add the employee onto the end of the list
        if (len(duplicate))!= 0 :
            #Remove the employee from the duplicate
            duplicate.pop(lowest_index)

    return return_list

def begin_rotation(employee_list, ride, position_availability):
    #Grab some variables we will need throughout the function
    pos_dict = ride.get_pos_dict()
    optional_pos_dict = ride.get_optional_pos_dict()
    all_positions_list = list(pos_dict.keys()) + list (optional_pos_dict.keys())
    all_positions_dict = {**pos_dict, **optional_pos_dict}

    # Iterate through the position availability
    for tightness in range(1,len(all_positions_list)):
        for position in all_positions_list: # We can do all positions now b/c we know we have enough to cover mandatory and optional
            if len(all_positions_dict[position]) == tightness: # It is currently time to work on this position
                    for candidate in employee_list:
                        if candidate.get_pos() is None and candidate.get_name() in position_availability[position.lower()]:
                            # Time to set them here 
                            change_position(employee_list, pos_dict, optional_pos_dict, candidate.get_name(), None, position)


def next_rotation(employee_list, ride, break_list, p_start, p_end):
    #Increase time for next rotation
    ride.set_current_time(ride.get_current_time().add(red_tag_classes.Time(0,ROTATION_LENGTH)))

    #If the time for starting this rotation is after the park closing time, exit
    if ride.get_current_time() > p_end:
        return False
    


    #Making life easier
    optional_pos_dict = ride.get_optional_pos_dict()
    pos_dict = ride.get_pos_dict()

    #If anyone is on break, take them off break and assign them a random position in optional.
    #They may possibly be pulled before the rotation is printed to accomodate the next break
    print("\n\n\n")
    for employee in employee_list:
        if employee.get_pos() == "Break":
            print ("\033[32mWelcome back from break " + employee.get_name() + '\033[0m')
            employee.set_break_end(ride.get_current_time()) #End their break in the object
            for key in optional_pos_dict:
                #Find a position in the optional_pos_dict that doesn't have anyone and assign them there
                if optional_pos_dict[key][0] == None:
                    optional_pos_dict[key][0] = employee.get_name()
                    employee.set_pos(key)
                    break

    #First priority is to send people home if needed
    send_people_home_result = send_people_home(employee_list, ride, break_list, p_start, p_end)
    if send_people_home_result[0]:
        break_list = send_people_home_result[1] #Update the break list if needed from the send_people_home function
    
    #Perform feasibility check - determines if there are any violations
    feasibility_result = feasibility_check(employee_list, break_list, pos_dict, optional_pos_dict, ride, p_start, p_end)
    if not feasibility_result[0]:
        #There will be some violations at some point
        print ('\033[31m' , 'WARNING:', '\033[0m', 'violation expected at', feasibility_result[3])
        print ('Breaks needed: ', feasibility_result[1], '/ extras present', feasibility_result[2])
    else:
        print ('\033[32m', 'No violations found!', '\033[0m')

    #Second priority is to send people on break if it is possible to do so. This will determine if it is possible
    pop_lead = [0, False]
    break_occuring = 0 #We start with no breaks occuring
    for i in range(len(break_list)):
        if (ride.get_current_time() > break_list[i].get_break_window()[0]  or ride.get_current_time() == break_list[i].get_break_window()[0]) and break_list[i].get_name() != "Lead":
            #The time is equal to or later than someones break window, and that person is not the lead. They may be able to brak
            if len(optional_pos_dict) > break_occuring:
                #We can do a break
                break_occuring+=1
        elif ride.get_current_time() > break_list[i].get_break_window()[0] and break_list[i].get_name() == "Lead":
            pop_lead = [True, i] #It is time for the leads break, but the program doesn't worry about that
        else:
            if pop_lead[0]:
                break_list.pop(pop_lead[1]) #We can pop the lead out of the break list
            break

    #If it is possible, send the person on break and remove the from the break list
    if break_occuring >0:
        optional_positions_list = list(optional_pos_dict)
        for i in range(break_occuring):
            #Lets determine who gets to go on break
            index = 0
            time = break_list[index].get_break_window()[0]
            if (int(break_list[index].get_age()) >= 18):
                #If the first perosn in the brak list is not a minor, make sure there is not a minor that should be going at this time
                for j in range(len(break_list)):

                    if int(break_list[j].get_age()) < 18 and break_list[j].get_break_window()[0] < ride.get_current_time():
                        #A minor should go instead - they always have the highest priority
                        index = j
                        break

            #Get all the info
            position_to_fill = break_list[index].get_pos() #The position of the person who is aboyut to go on break that will need filled
            position_to_vacate = optional_positions_list[i] #The position that will be pulled to cover break
            person_to_break = break_list[index] #An employee object
            person_to_fill = optional_pos_dict[position_to_vacate][0] #A name 

            change_position(employee_list, pos_dict, optional_pos_dict, person_to_break.get_name(), None, "Break") #Send the person to break
            change_position(employee_list, pos_dict, optional_pos_dict, person_to_fill, None, position_to_fill ) #Have the person filling fill the spot

            optional_pos_dict[position_to_vacate][0] = None #Empty the old position
            person_to_break.set_break_status(True) #Update the person's status
            break_list.pop(index) #Get them off the break list
            print('\033[33m',person_to_break.get_name() + " is going on break now\033[0m") #Notify the user

    #Third priority is rotating all remaing employees
    first_pos = employee_list[0]
    for i in range(len(employee_list)):
        current_pos = employee_list[i].get_pos()
        if current_pos == "Break": #Don't rotate people on break
            continue
        try:
            next_employee = employee_list[i+1] #Try to move them one down the list
        except:
            next_employee = first_pos #Unless you are at the end of the list, in that case, go back to the start
        if next_employee.get_pos() == "Break":
            continue

        change_position(employee_list, pos_dict, optional_pos_dict, employee_list[i].get_name(), next_employee.get_name(), None) #Perform the swap

    clean_rotation(employee_list, ride) #Make sure clerks aren't operating, leads aren't clerking, etc.

    return send_people_home_result #Return this so the CLI knows if the breaks_list has changed and some employees have gone home


"""
This is a helper function that will ensure the lead stays on the ride and clerks stay where they belong
"""
def clean_rotation(employee_list, ride):
    #First, let us find the lead and ensure they are on the ride
    pos_dict = ride.get_pos_dict()
    optional_pos_dict = ride.get_optional_pos_dict()
    lead_position = None #The lead employee list
    clerk_position_list = [] #The list of potential clerk positions
    clerk_position_info_list = [] #The list of position objects to check and see if the clerk can be where they are

    swapped = [] #A list of employee objects that have already been swapped

    for position in pos_dict:
        if pos_dict[position][0] == "Lead":
            lead_position = pos_dict[position] #We found the lead, and there is only ever one. Break out
            break
    if lead_position == None: #We still haven't found them, they must be doing an optional position
        for position in optional_pos_dict:
            if optional_pos_dict[position][0] == "Lead":
                lead_position = optional_pos_dict[position]
    for employee in employee_list:
        if int(employee.get_age()) < 16 and employee.get_pos() != "Break":
            clerk_position_list.append(employee.get_pos()) #The positions that clerks are occupying
    for position in clerk_position_list:
        #Put the info list for that position into the clerk_position_info_list
        try:
            clerk_position_info_list.append(pos_dict[position])
        except:
            clerk_position_info_list.append(optional_pos_dict[position])
    
    #Great, we found the lead. Lets determine if it is valid and change it if it isnt
    if not lead_position[1]:
        #No good, pick another position
        for i in range(len(employee_list)):
            potential_swap = employee_list[i]
            potential_swap_position = potential_swap.get_pos()
            if potential_swap_position == "Break":
                continue
            try:
                if pos_dict[potential_swap_position][1] and (int(find_employee_in_list(employee_list, pos_dict[potential_swap_position][0]).get_age()) >= 16):
                    #The swap is valid because it can accept leads and the person there is not a clerk
                    lead = find_employee_in_list(employee_list, lead_position[0]) #The lead employee object
                    change_position(employee_list, pos_dict, optional_pos_dict, employee_list[i].get_name(), lead.get_name(), None )
                    swapped.append(lead) #Make sure the person is not swapped again
                    swapped.append(employee_list[i])
                    break
            except KeyError:
                #The person we are swapping is in the optional pos dict. This changes nothing
                if optional_pos_dict[potential_swap_position][1] and (int(find_employee_in_list(employee_list, pos_dict[potential_swap_position][0]).get_age()) >= 16):
                    #The swap is valid because it can accept leads and the person there is not a clerk
                    lead = find_employee_in_list(employee_list, lead_position[0]) #The lead employee object
                    change_position(employee_list, pos_dict, optional_pos_dict, employee_list[i].get_name(), lead.get_name(), None )
                    swapped.append(lead) #Make sure the person is not swapped again
                    swapped.append(employee_list[i])
                    break
    
    #Time to do the same for the clerks
    for clerk in clerk_position_info_list:
        #Perform the swap function, but make sure you dont swap a clerk that has already been swapped or the person that is going on break
        if not clerk[2]:
            #A swap is needed
            for i in range(len(employee_list)):
                potential_swap = employee_list[i]
                potential_swap_position = potential_swap.get_pos()
                if potential_swap_position == "Break":
                    continue #Don't swap people on breaks
                #WARNING unsure if this is actually functioning. People who have already been swapped may be swapped again
                for swap in swapped:
                    cont = False 
                    if swap.get_name() == potential_swap.get_name():
                        #This person has already been swapped out of a position
                        cont = True
                        break

                try:
                    if pos_dict[potential_swap_position][2]:
                        #The swap is valid, make it happen
                        clerk_object = find_employee_in_list(employee_list, clerk[0])
                        change_position(employee_list, pos_dict, optional_pos_dict, employee_list[i].get_name(), clerk_object.get_name(), None )
                        swapped.append(clerk_object) #Make sure they are not swapped again
                        swapped.append(employee_list[i])
                        break
                except KeyError: #They are swapping for an optional position instead
                        if optional_pos_dict[potential_swap_position][2]:
                            #The swap is valid, make it happen
                            clerk_object = find_employee_in_list(employee_list, clerk[0])
                            change_position(employee_list, pos_dict, optional_pos_dict, employee_list[i].get_name(), clerk_object.get_name(), None )
                            swapped.append(clerk_object)
                            swapped.append(employee_list[i])
                            break

"""
This function will determine if people will need to go home in the next ROTATION_LENGTH minutes. If they do, it will prompt
the user to either remove the position (if possible), add a new employee, or continue with this employee in, while ackowledging
that this may result in a violation
"""
def send_people_home(employee_list, ride, break_list, p_start, p_end):
    #Let us make life easier
    pos_dict = ride.get_pos_dict()
    optional_pos_dict = ride.get_optional_pos_dict()
    current_time = ride.get_current_time()
    send_people_home_return = [False] #A default value to return if no one needs to be sent home

    #Let us now determine if any employees shift are going to end on this rotation
    people_leaving = []
    for employee in employee_list:
        if employee.get_shift_end() < current_time or employee.get_shift_end() == current_time:
            people_leaving.append(employee)

    #Great, now we can figure out what to do with these people
    if (len(people_leaving) == 0): #If there are no people to send home, we can just return and be done
        return send_people_home_return
    else:
        for i in range(len(people_leaving)):
            employee_leaving = people_leaving[i]
            print("\n")
            print ('\033[33m',employee_leaving.get_name() , " needs to leave at " , employee_leaving.get_shift_end() , '\033[0m')
            if (int(employee_leaving.get_age()) < 18):
                #Determine the violation time

                violation_time = None
                if employee_leaving.get_break_status(): #The employees violation time is 5 hours past the end of break
                    break_end = employee_leaving.get_break_end()
                    violation_time = break_end.add( red_tag_classes.Time(5,0))

                else:
                    #The employee hasn't had a break, their V. time is 5 hours after shift start
                    violation_time = employee.get_shift_start() + red_tag_classes.Time(5,0)

                print ("\033[31mThe employee is a minor and will violate at " , violation_time, '\033[0m')       
            else:  
                print ("\033[32mThis employee is not a minor, you do not need to worry about violations for this employee\033[0m")  


            #Present the user with the options for what they can do about this problem
            while True:
                #Idiot check to make sure the command given is one of the permitted options
                command = ''
                while command != '+' and command != '-' and command != 'acknowledge':
                    command = input("Please identify how you would like to address this issue. Press '-' to remove an optional position, if possible \n Press '+' to add an employee to replace "+
                    employee_leaving.get_name()+ ". \n Type 'acknowledge' to continue with this employee for the next rotation. By doing so, you acknowledge that this could lead to a violation")

                if command == 'acknowledge':
                    #Break out and do nothing for this employee
                    print ('\033[31mRisk acknowledged. The rotation will now continue with this employee in it\033[0m')
                    break
                elif command == '+':
                    #Create a new Employee object. Recalculate break list with existing break list and new employee object.
                    current = add_an_employee(employee_list, p_start, p_end) #Call the helper to return a new employee

                    #Determine if the employee needs a break, and if so, add them to the break list
                    #Idiot check for this input
                    needs_break = ''
                    while needs_break.lower() != 'n' and needs_break.lower() != 'y': 
                        needs_break = input ('Does ' + current.get_name() + ' need a break? Please enter y or n' )
                    if needs_break == 'n':
                        current.set_break_status(True)
                    else:
                        #Remake the break list with the new employee in it
                        break_list.append(current)
                        break_list = make_break_list(break_list, len(break_list))
                    
                    #Perform the swap
                    leaving_position = employee_leaving.get_pos()
                    #Call the obliterate function with the correct dictionary
                    try:
                        obliterate_employee(employee_list, break_list, pos_dict, employee_leaving.get_name())
                    except KeyError:
                         obliterate_employee(employee_list, break_list, optional_pos_dict, employee_leaving.get_name())
                    
                    current.set_pos(leaving_position) #Set the new employees position to the position the employee is leaving

                    #Set the dictionary entry to the new employees name
                    try:
                        pos_dict[leaving_position][0] = current.get_name()
                    except KeyError:
                        optional_pos_dict[leaving_position][0]= current.get_name()
                   
                   #Set the return value to the new break list
                    send_people_home_return = [True, break_list]

                    break
                    

                elif command == '-':
                    #Choose to subtract a position. Let us determine if there is a position to subtract.
                    #If 0, tell them to choose another option, if 1 remove it, if 2 or more give them a choice
                    if (len(optional_pos_dict) == 0):
                        print("\033[31m You are already at mins and cannot remove a position. Please choose another option \033[0m")
                    elif (len(optional_pos_dict) == 1):
                        
                        #Get the info needed
                        leaving_position = employee_leaving.get_pos()
                        dict_keys = list(optional_pos_dict.keys())
                        position = dict_keys[0] #The only optional position - about to be removed
                        employee_name_covering = optional_pos_dict[position][0] #The name of the employee in that position
                        print ("There is only one optional position currently: ", position, " and it will now be deleted. \033[31m You are at mins \033[0m")
                        
                        #remove the employee that is leaving
                        print ('\033[32m',employee_leaving.get_name(), " may now leave. Thank you for being here today! \033[0m")
                        try:
                            obliterate_employee(employee_list, break_list,pos_dict,employee_leaving.get_name()) #Obliterate the employee

                            
                            #Set the position of the employee covering to the position of the person leaving
                            employee_covering = find_employee_in_list(employee_list, employee_name_covering) #The employee object in the optional position
                            employee_covering.set_pos(leaving_position) #Set position in employee object
                            pos_dict[leaving_position][0] = employee_name_covering #Set position in dictionary
                        
                        except KeyError:
                            #The employee we are removing is occupying the position we are removing. 

                            #Obliterate the employee from the optional pos dict
                            obliterate_employee(employee_list, break_list, optional_pos_dict, employee_leaving.get_name())

                            #We don't need to do anything further as no one needs to cover the optional position

                        #remove the position they are vacating
                        del optional_pos_dict[position] #Remove the optional position
                        break
                    else:
                        #Give the employee the option of who they would like to remove
                        print ("\033[33mThere are multiple positions that can be removed. Please select the option you would like removed by entering the number in brackets after it is listed\033[0m")
                        i = 0
                        optional_position_list = []
                        for optional_position in optional_pos_dict: #Print out their options
                            print (optional_position, '[', i, ']', end=" --- ")
                            i += 1
                            optional_position_list.append(optional_position) #Add it to the list so we can pick it using the index the user provides
                        choice = int(input("Please enter your choice now:"))

                        #This now almost the same as above
                        leaving_position = employee_leaving.get_pos() #The position of the employee leaving
                        position = optional_position_list[choice] #The positoion we are going to remove
                        employee_name_covering = optional_pos_dict[position][0] #The name of the person in the position we are about to delete

                        try:
                            obliterate_employee(employee_list, break_list, pos_dict, employee_leaving.get_name()) 

                            employee_covering = find_employee_in_list(employee_list, employee_name_covering) #The object for the name of employee_name_covering
                            employee_covering.set_pos(leaving_position) #Set their position
                            pos_dict[leaving_position][0] = employee_name_covering #Adjust the dictionary
                        except KeyError:
                            #The position is optional and can just be deleted without swapping people
                            obliterate_employee(employee_list, break_list, optional_pos_dict, employee_leaving.get_name())
                        del optional_pos_dict[position] #Remove the old position from the dictionary
                        break
        return send_people_home_return #Return the result as false as we did not need to adjust the breaks list at all


def add_an_employee(employee_list, p_start, p_end, ):
    #Create a new Employee object. This function does NOT add them to the break list or recalculate it if necessary

    #Idiot loop to make sutre the name has no spaces
    name = 'bad input'
    while (len(name.split()) > 1):
        name = input("Please enter the employee's name")
    
    #Idiot loop to make sure age is a number
    while True:
        age = input ('How old is ' + name + '?')
        try:
            int(age)
            break
        except ValueError:
            print('\033[31m Please enter a value \033[0m')
    shift_start_q = ''
    while shift_start_q.lower() != 'y' and shift_start_q.lower() != 'n':
        shift_start_q = input('Are they working the entire day? Please enter Y or N.')
    if shift_start_q == 'Y' or shift_start_q == 'y':
        #Creates an employee object with shift time half hour before open to half hour past close
        current = red_tag_classes.Employee(name, age, p_start.subtract(red_tag_classes.Time(0,30)), p_end.add(red_tag_classes.Time(0,30)))
        employee_list.append(current)
    else:
        #Idiot check loop to make sure they enter times in the form HH:MM
        e_start, e_end = '', ''
        while len(e_start.split(':')) != 2 or len(e_end.split(":")) != 2:
            e_start = input('What time does this employee start their shift? Enter in the form HH:MM')
            e_end = input('What time does this employee end their shift? Enter in the form HH:MM')
           
        e_start = e_start.split(':')
        e_end = e_end.split(':')
        #Create the time objects
        e_start = red_tag_classes.Time(int(e_start[0]), int(e_start[1])) 
        e_end = red_tag_classes.Time(int(e_end[0]), int(e_end[1]))

        #Create the employee object and add them to the employee list
        current = red_tag_classes.Employee(name, age, e_start, e_end) 
        employee_list.append(current) 
    if current.get_name() == "Lead": #Leads don't get breaks in this program
        current.set_break_status(True)
    return current
"""
Completely removes all traces of an employee in the program. Takes them out of pos dict, off the break list, 
and out of the employee list. NOTE: pos dict in this context is whatever dictionary the employee is in
"""
def obliterate_employee(employee_list, break_list, pos_dict, employee_name):
    employee_object = find_employee_in_list(employee_list, employee_name) #Locate the employee
    employee_position = employee_object.get_pos()
    pos_dict[employee_position][0] = None #Set the position to none in the dictionary
    employee_list.remove(employee_object) #Get the object out of the list
    
    try:
        break_list.remove(employee_object) #Remove the employee from the break list if they needed one
    except ValueError:
        pass #The employee is not in the break list to begin with

"""
This is a helper function to complete an entire swap or position change
If you want to set, use two name as None and the position you want to set as position_to_set
If you want to swap, use position_to_set as None
"""
def change_position(employee_list, pos_dict, optional_pos_dict, one_name, two_name, position_to_set):
    if two_name == None:
        #This isnt a swap, it is a set
        employee_one = find_employee_in_list(employee_list, one_name) #Get the employee object
        employee_one.set_pos(position_to_set) #Set their position
        if position_to_set == "Break": #We dont have to update it in the dict if it is a break
            pass
        elif position_to_set in pos_dict.keys():
            pos_dict[position_to_set][0] = one_name
        else:
            optional_pos_dict[position_to_set][0] = one_name
    else:
        #This is a swap

        #Locate the employees
        employee_one = find_employee_in_list(employee_list, one_name)
        employee_two = find_employee_in_list(employee_list, two_name)
        #Find their positions
        employee_one_position = employee_one.get_pos()
        employee_two_position = employee_two.get_pos()
        #Set the positions in the employee object
        employee_two.set_pos(employee_one_position)
        employee_one.set_pos(employee_two_position)
        #Adjust employee one in the dict
        if employee_one_position == "Break":
            pass
        elif employee_one_position in pos_dict.keys():
            pos_dict[employee_one_position][0] = two_name
        else:
            optional_pos_dict[employee_one_position][0] = two_name
        #Adjust employee two in the dict
        if employee_two_position == "Break":
            pass
        elif employee_two_position in pos_dict.keys():
            pos_dict[employee_two_position][0] = one_name
        else:
            optional_pos_dict[employee_two_position][0] = one_name

"""
This is a helper function to print the employee info 
Everything yuou need to know about people is in here
"""
def print_employee_list(employee_list):
    print ("name - break - wStart - wEnd - position")
    for employee in employee_list:
        return_string = employee.get_name() + "-"
        return_string += str(employee.get_break_status()) + "-"
        return_string += str(employee.get_break_window()[0]) + "-"
        return_string += str(employee.get_break_window()[1]) + "-"
        return_string += employee.get_pos()
        print(return_string)

"""
This is a helper function to print a ride with just positions and employee names
"""
def print_ride(ride):
    print ('\033[36m' ,ride.get_name() + "     "  + str(ride.get_current_time()), '\033[0m') #Ride name and current time
    print ('-' * 50)
    pos_dict = ride.get_pos_dict()
    opt_dict = ride.get_optional_pos_dict()
    print ("\033[33mHere are the mandataory positions\033[0m")
    for position in pos_dict: #Loop through all mandatory positions and print them out
        if pos_dict[position][0] != None:
            print(position + " : " + pos_dict[position][0])
    print("-" * 50)
    if (len(opt_dict) > 0 ):
        print("\033[33mAnd here are the optional positions:\033[0m")
        for position in opt_dict: #Print through all occupired optional posiitions
            if opt_dict[position][0] != None:
                print (position + " : " + opt_dict[position][0])
    print ('-' * 50)

"""
This is a helper function to find an employee in the given employee list - a linear search
"""
def find_employee_in_list(employee_list, name):
    for employee in employee_list:
        if employee.get_name().lower() == name.lower():
            return employee
    return None

"""
Ultimately, this function will return true or false based off of the amount of minor break time is coverable within the set window
May also note if this will require squtching positions within a rotation
Returns in the form [True/False, number of breaks, number of extras, time of earliest violation ]
"""
def feasibility_check(employee_list, break_list, pos_dict, optional_pos_dict, ride, p_start, p_end):

    
    minor_breaks = [] #A list of all the minor breaks - minors are thre only ones who can violate
    for employee in break_list:
        if int(employee.get_age()) < 18 and not employee.get_break_status():
            minor_breaks.append(employee) #Add all minor breaks to the list

    if (len(minor_breaks)) == 0: #If there are no breaks to do, then of course it is possible
        return [True]

    #Determine how many minor breaks will be done on each rotation
    #Figure out if we have enough employees to cover that many breaks on each rotation
    #If not, determine if there are ways we can reduce the number of breaks that are occuring at one time
    time_travel = ride.get_current_time() #A time object used to move throughout the day without adjusting the rides current time
    counter_dict = {} #A dicitionary that maps times to the list of minor breaks on that time

    #NOTE counter_dict assumes that all minors will start their break the instant they can do so, without worrying
    #about the rest of their break windows or if the start of window lines up with a rotation

    for minor in minor_breaks:
        if counter_dict.__contains__(minor.get_break_window()[0]):
            counter_dict[minor.get_break_window()[0]].append(minor) #Add it to the list if it already exists
        else:
            counter_dict[minor.get_break_window()[0]] = [minor] #If it doesnt exist, make a new key



    #Create a list of all the times rotations will begin
    start_times = []
    time_travel = p_start
    while time_travel <p_end:
        start_times.append(time_travel)
        time_travel = time_travel.add(red_tag_classes.Time(0,ROTATION_LENGTH)) #We are assuming that all rotations are ROTATION_LENGTH minutes

    #Determine which rotation the breaks will start on
    rotation_dict = {} #This maps rotations to minors
    for time in counter_dict:
        if start_times.__contains__(time): #If the start of window is on a rotation, just copy it over to the rotation_dict
            rotation_dict[time] = counter_dict[time]
            continue
        else:
            for rotation_time in start_times: #Otherwise, find the first rotation that they would go one break, and add that
                if rotation_time > time:
                    rotation_dict[rotation_time] = counter_dict[time]
                    break
    

    max_possible = len(optional_pos_dict) #This is the maximum number of possible breaks

    if max_possible == 0:
        #You have no extras and can do no breaks. Let's find out what the first time for violation is
        first_key = list(rotation_dict.keys())[0] #This is the number of break we have to do on the earliest rotation

        #Loop through and find the earliest end of a break window for any minor
        earliest_violation = red_tag_classes.Time(24, 0)
        for key in rotation_dict:
            for i in range (len(rotation_dict[key])):
                if rotation_dict[key][i].get_break_window()[1] < earliest_violation:
                    earliest_violation = rotation_dict[key][i].get_break_window()[1]

        #reutrn violation, number of people who will violate, we have 0 extras, when the violation will occur
        return [False, len(rotation_dict[first_key]), 0, earliest_violation]

    #Call the adjustments sub-function
    new_object = adjustments(rotation_dict, max_possible)

    #This new object could be either a list stating when violations could occur, or a dictionary to re-call the function
    while isinstance(new_object, dict):
        new_object = adjustments(new_object, max_possible)
    
    if new_object[0]:
        return [True] #The adjustments worked, and we were able to avoid violations
    else:
        return new_object #The adjustments did not work, and the function will identify when earliest violation occurs


def adjustments(rotation_dict, max_possible):
    for time in rotation_dict:
        number_of_breaks_on_rotation = len(rotation_dict[time]) #Thje number of breaks we are currently doing at this time
        index = 0 #The current break we are looking at on a rotation
        earliest_violation = red_tag_classes.Time(24,0)
        while number_of_breaks_on_rotation > max_possible:
            #Mess around and see if we can make number_of_breaks_on_rotation smaller

            #Check and see if the index is larger than number of people needing a break (this means everyone needs a break at that time)
            if index >= number_of_breaks_on_rotation:
                return [False, number_of_breaks_on_rotation, max_possible, earliest_violation] #No breaks can be adjusted

            #The index is not larger, so lets try moving the break of the person at this index back 1 rotation to see if that helps
            current_start = time
            current_start = current_start.add(red_tag_classes.Time(0,ROTATION_LENGTH)) #The next rotation we are looking at (maybe we can start the breka now)
            
            current_employee = rotation_dict[time][index]

            #Adjust the earliest violation so we can report it if we are unable to adjust the break time
            if current_employee.get_break_window()[1] < earliest_violation:
                earliest_violation = current_employee.get_break_window()[1]
            
            if current_start < current_employee.get_break_window()[1]:
                #We can definitely move the employees break. Adjust the dict. Adjust number_of_breaks_on_rotation

                rotation_dict[time].pop(index) #Remove this from the current time
                
                #Move it to the next rotation
                if rotation_dict.__contains__(current_start):
                    rotation_dict[current_start].append(current_employee)
                else:
                    rotation_dict[current_start] = [current_employee]
                    return rotation_dict
                number_of_breaks_on_rotation = len(rotation_dict[time])
            else:
                #We cannot adjust the employees break - this is the only time they can go. Add 1 to index and try next employee (if there is one)
                index += 1
    return [True] #If we get the breaks down far enough to exit the while loop, we cna return True

def main():
    red_tag_CLI.main()
            
if __name__ == "__main__":
    main()

                


