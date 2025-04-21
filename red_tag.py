import red_tag_classes
import red_tag_CLI
import red_tag_test_utils
import csv
import copy
import ast
"""
This is red_tag. It will simulate the job of a red tag by creating a rotation at a specified ride
It will take into account minor breaks, violations, and a relatively fair rotation
"""
ROTATION_LENGTH = 45






def training_check (position_availability, person = None):
    # If we aren't looking at a specific person, just check the whole thing
    if person == None:
        for position in position_availability:
            if len(position_availability[position]) == 0:
                return False
        return True
    
    # Otherwise, let's check what will happen if we get rid of "person"
    result = {1: [], 2: [], 'other': []}
    for position in position_availability:
        availability = position_availability[position]

        if person in availability:
            if len(availability) == 1:
                result[1].append(position)
            elif len(availability) == 2:
                result[2].append(position)
            else:
                result['other'].append(position)
    return result
    

def rotate(ride, first):
    #Grab some variables we will need throughout the function
    employee_list = ride.get_employee_list()
    position_availability = ride.get_position_availability()
    pos_dict = ride.get_pos_dict()
    optional_pos_dict = ride.get_optional_pos_dict()
    all_positions_list = list(pos_dict.keys()) + list (optional_pos_dict.keys())

    temp_position_availability = copy.deepcopy(position_availability)

    for _ in range(len(all_positions_list)): # This is how many positions we have to assign, no matter what
        for tightness in range(1, len(all_positions_list) +1):
            current_position = None
            for position in all_positions_list:
                if len(temp_position_availability[position.lower()]) == tightness:
                    # We have found our psosition to work on, break out of all loops except main one
                    current_position = position.lower()
                    break
            if current_position != None:
                break
        # Having found the position, lets deal with it
        for candidate in employee_list:
            if ((candidate.get_pos()  == None and first) or (candidate.get_pos() != current_position and not first )) and candidate.get_name() in temp_position_availability[current_position.lower()]:
                # Set them
                change_position(ride,candidate.get_name(), None, current_position)

                # Remove this employee from everywhere else in the temp availability - they are no longer available
                for position , people in temp_position_availability.items():
                    if candidate.get_name() in people:
                        temp_position_availability[position].remove(candidate.get_name())
                
                # Remove the position from all_positions_list - it cannot be set twice
                all_positions_list.remove(current_position)
                break # Move on 


def do_breaks(break_occuring, ride):
    # Grab/compute all the variables
    pos_dict = ride.get_pos_dict()
    optional_pos_dict = ride.get_optional_pos_dict()
    break_list = ride.get_break_list()
    employee_list = ride.get_employee_list()

    optional_positions_list = list(optional_pos_dict)
    for i in range(break_occuring): 

        # Grab/compute all the variables
        pos_dict = ride.get_pos_dict()
        optional_pos_dict = ride.get_optional_pos_dict()
        break_list = ride.get_break_list()

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
        person_to_fill = optional_pos_dict[position_to_vacate][0] #A name - don't matter if they are trained, they are about to rotate

        change_position(employee_list, pos_dict, optional_pos_dict, person_to_break.get_name(), None, "Break") #Send the person to break
        change_position(employee_list, pos_dict, optional_pos_dict, person_to_fill, None, position_to_fill ) #Have the person filling fill the spot

        # Make local changes
        break_list.pop(index) #Get them off the break list
        optional_pos_dict[position_to_vacate][0] = None #Empty the old position
        person_to_break.set_break_status(True) #Update the person's status

        # Save them to ride object
        ride.set_optional_pos_dict(optional_pos_dict)
        ride.set_break_list(break_list)
        ride.set_pos_dict(pos_dict)


        print('\033[33m',person_to_break.get_name() + " is going on break now\033[0m") #Notify the user

        # Return that which you changed
        return pos_dict, optional_pos_dict, break_list

def next_rotation(ride, p_start, p_end):
    # Get variables
    employee_list = ride.get_employee_list()
    break_list - ride.get_break_list()
    position_availability = ride.get_position_availability()
    optional_pos_dict = ride.get_optional_pos_dict()
    pos_dict = ride.get_pos_dict()

    #Increase time for next rotation
    ride.set_current_time(ride.get_current_time().add(red_tag_classes.Time(0,ROTATION_LENGTH)))

    #If the time for starting this rotation is after the park closing time, exit
    if ride.get_current_time() > p_end:
        return False
    


    #If anyone is on break, take them off break and assign them a random position in optional.
    #They may possibly be pulled before the rotation is printed to accomodate the next break
    #It doesn't matter if they are trained there, they are about to get pulled or rotated anyways
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
    #TODO: Add training check logic to this function
    send_people_home_result = send_people_home(employee_list, ride, break_list, p_start, p_end, position_availability)
    if send_people_home_result[0]:
        break_list = send_people_home_result[1] #Update the break list if needed from the send_people_home function
    
    #Perform feasibility check - determines if there are any violations
    #TODO: Add logic to feasibility check to make sure you aren't sending home/on break the one person who is trained at a position
    feasibility_result = feasibility_check(employee_list, break_list, pos_dict, optional_pos_dict, ride, p_start, p_end) # Does not change anything, no need to get/set thinga within the function
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
       pos_dict, optional_pos_dict, break_list = do_breaks(break_occuring, ride)


    rotate(ride, False)

    return send_people_home_result #Return this so the CLI knows if the breaks_list has changed and some employees have gone home

# In progress
def new_send_people_home (employee_list, ride, break_list, p_start, p_end, position_availability):
    pos_dict = ride.get_pos_dict()
    opt_pos_dict = ride.get_optional_pos_dict()
    current_time = ride.get_current_time()

        #Let us now determine if any employees shift are going to end on this rotation
    people_leaving = []
    for employee in employee_list:
        if employee.get_shift_end() < current_time or employee.get_shift_end() == current_time:
            people_leaving.append(employee)

    # If there's no one leaving, we are done here
    if (len(people_leaving) == 0):
        return [False]
    
    for i, employee in enumerate(people_leaving):
        # Get the training report
        training = training_check(position_availability, employee.get_name())

        # Review training violations of sending this employee home
        while len(training[0]) != 0 :
            position = training[0]
            # At least one critical training violation will occur because of this
            # Determine if the position is critical
            if position in opt_pos_dict:
                training[0].pop(0) # Don't care - clear them out 
            else:
                #This is a problem - employee MUST be replaced
                training[0] = swap(position_availability, ride, employee, training[0])

#In progress
def swap(position_availability, ride, employee, violations):
    print (f'It is time for {employee.get_name()} to go home for the day, but if they leave there will be no one left who is trained at the following positions:')
    for p in violations:
        print ('\t\t',p)
    
    print ('Because these positions are not optional, you will need to add someone (or multiple people) to the ride who is/are trained at this time')

    # Continue adding people 
    

"""
This function will determine if people will need to go home in the next ROTATION_LENGTH minutes. If they do, it will prompt
the user to either remove the position (if possible), add a new employee, or continue with this employee in, while ackowledging
that this may result in a violation
"""
def send_people_home(employee_list, ride, break_list, p_start, p_end, position_availability):
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

            # Inform them about violation time or its lack of relevance
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

            # Get information about training
            training_check_result = training_check(position_availability, True, employee_leaving.get_name())

            # TODO: Rewrite the logic for this entire function. See blue sheet (hah!)



            #Present the user with the options for what they can do about this problem

            #Idiot check to make sure the command given is one of the permitted options
            command = ''

            # Depending on the result of the training check and the nature of the position, the next action may be predetermined
            if training_check_result == 1:
                print (f' Fatal error - you have no employees trained at this position')
                exit(0)
            elif training_check_result == 2: #This should never happen, because it would mean there is no one trained at the position at all
                print (f' You are about to lose your only employee trained at this position')
                if employee_leaving.get_pos().lower() in pos_dict.keys():
                    print (f'This is a mandatory position - you cannot get rid of it. Your must add an employee to replace them with or ackowledge that you are keeping this employee beyond their scheduled end-of-shift ')


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
                pos_dict, optional_pos_dict, break_list, employee_list = obliterate_employee(ride, employee_leaving.get_name())
                
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


def add_an_employee(ride, p_start, p_end):
    # Get variables
    employee_list = ride.get_employee_list()
    break_list = ride.get_break_list()
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

    # Determine if they already had a break
    break_answer = ''
    if break_answer.lower() != 'y' and break_answer.lower() != 'n':
        break_answer = input("Has " + name + " had a break yet? Please enter y or n: ")
    if break_answer.lower() == 'y':
        time_answer = ''
        while (len(time_answer.split()))!= 2:
            time_answer = input("What time did the break end? Enter in the form HH:MM")
        time_tokens = time_answer.split(':') 
        break_status = True
        break_end = (red_tag_classes.Time(time_tokens[0], time_tokens[1]))
    else:
        break_status = False
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

    # If they al;ready had abreak, they don't need a break
    if break_status:
        current.set_break_status(True)
        current.set_break_end(break_end)

    # Set variables
    ride.set_employee_list(employee_list)
    ride.set_break_list(break_list)
    ride.make_break_list()
    return current
"""
Completely removes all traces of an employee in the program. Takes them out of pos dict, off the break list, 
and out of the employee list. NOTE: pos dict in this context is whatever dictionary the employee is in
"""
def obliterate_employee(ride, employee_name):
    # Get variables
    employee_list = ride.get_employee_list()
    pos_dict = ride.get_pos_dict()
    break_list = ride.get_break_list()
    opt_pos_dict = ride.get_optional_pos_dict()

    employee_object = find_employee_in_list(employee_list, employee_name) #Locate the employee
    employee_position = employee_object.get_pos()
    try:
        pos_dict[employee_position][0] = None #Set the position to none in the dictionary
        location = 'pos_dict'
    except:
        opt_pos_dict[employee_position][0] = None
        location = 'opt_pos_dict'
    employee_list.remove(employee_object) #Get the object out of the list
    
    try:
        break_list.remove(employee_object) #Remove the employee from the break list if they needed one
    except ValueError:
        pass #The employee is not in the break list to begin with

    # Set variables
    ride.set_break_list(break_list)
    ride.set_pos_dict(pos_dict)
    ride.set_employee_list(employee_list)
    ride.set_optional_pos_dict(opt_pos_dict)

    return break_list, pos_dict, opt_pos_dict, employee_list, location

"""
This is a helper function to complete an entire swap or position change
If you want to set, use two name as None and the position you want to set as position_to_set
If you want to swap, use position_to_set as None
"""
def change_position(ride, one_name, two_name, position_to_set):
    # Get everything we need
    employee_list = ride.get_employee_list()
    pos_dict = ride.get_pos_dict()
    optional_pos_dict = ride.get_optional_pos_dict()

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
    # Set everything we changed
    ride.set_employee_list(employee_list)
    ride.set_optional_pos_dict(optional_pos_dict)
    ride.set_pos_dict(pos_dict)

"""
This is a helper function to print the employee info 
Everything yuou need to know about people is in here
"""
def print_employee_list(ride):
    employee_list = ride.get_employee_list()
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
        if employee.get_name().lower() == name.                                                                                                                                                                                                                                            lower():
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

                


