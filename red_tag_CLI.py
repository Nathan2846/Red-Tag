from tkinter import E
import red_tag
import red_tag_classes
import red_tag_test_utils
import yaml

import os

def main():
    config_name = input('Welcome! Please enter the name of a configuration file, or press enter for default:')
    if len(config_name) == 0:
        config_name = os.path.join(os.getcwd(),'Red-Tag/config.yaml')
    
    with open(config_name, 'r') as f:
        config = yaml.safe_load(f)

    ride = red_tag_classes.Ride(config['ride']['name'], config['ride']['mins'])
    for i, p in enumerate(config['ride']['positions']):
        ride.add_pos(p['name'], p['lead'], p['clerk'], p['mandatory'])
    number_positions = i+1 
    
    # Get time strings
    p_start = config['park_open']
    p_end = config['park_close']

    # Make them time objects
    p_start = p_start.split(':')
    p_start = red_tag_classes.Time(int(p_start[0]),int(p_start[1]))
    p_end = p_end.split(':')
    p_end = red_tag_classes.Time(int(p_end[0]),int(p_end[1]))

    ride.set_current_time(p_start)

    # Make the employee list
    employee_list = []
    for i, e in enumerate(config['employees']):
        # Gather stringt time data
        start = e['shift_start']
        end = e['shift_end']

        # Make time objects
        start = start.split(':')
        end = end.split(':')
        start = red_tag_classes.Time(int(start[0]), int(start[1]))
        end = red_tag_classes.Time(int(end[0]), int(end[1]))


        current = red_tag_classes.Employee(e['name'], e['age'], start, end, e['is_lead'])
        current.set_untrained_positions(e['untrained_positions'])

        employee_list.append(current)
    
    break_list = red_tag.make_break_list(employee_list, number_positions)
    position_availability = red_tag.calculate_position_availability(employee_list, ride)

    red_tag.rotate(employee_list, ride, position_availability, True)
    red_tag.print_ride(ride)

    #Prepare to enter main loop
    print("Ride has been successfully created. You may now enter the following commands. \n Press e to get a full readout of employee data. \n"
    " Press n to get the next rotation. \n Press q to quit. \n Press + to add another employee. \n Press - <name> to remove an employee. \n Press r to fully reset and start over again. \n Press h to get this list of commands again."
    "\n Press f <employee name> to locate an employee and print out their current status. \n Press t <employee> <position> to train an employee on a position")

    command = input("Please enter your first command: ")
    command = command.lower()
    #Enter the main loop
    while(command != 'q'): #As long as the user doesn't ask to quit, keep going
        command_tokens = command.split() #Tokenize the command
            
        if not command_tokens:
            command = 'h' #If no command is entered, display help
        else:
            command = command_tokens[0] #The first thing entered will always be the command



        if ride.get_current_time() == p_end or ride.get_current_time() > p_end: #If the day is over, end the program
            print ("The day is over, thank you for being here, have a great night!")
            break
        elif command == 'h':
            #Print the help menu
            print("\n Press e to get a full readout of employee data. \n",
            " Press n to get the next rotation. \n Press q to quit. \n Press + to add another employee. \n Press - <name> to remove an employee. \n Press r to fully reset and start over again. \n Press h to get this list of commands again."
            "\n Press f <employee name> to locate an employee and print out their current status. \n Press t <employee> <position> to train an employee on a position")
        elif command == 't':
            # Train an employee
            if len(command_tokens) != 3:
                print ('Please enter the command in the form t <employee> <position>')
            else:
                employee_name, position = command_tokens[1], command_tokens[2]


                
                # Find the employee object 
                employee_object = red_tag.find_employee_in_list(employee_list,  employee_name)
                if employee_object == None:
                    print ('Employee not found')
                    continue

                # Train them
                before = len(employee_object.get_untrained_positions())
                employee_object.train_on_position(position.lower())
                after = len(employee_object.get_untrained_positions())

                # Confirm
                if before == after:
                    print ('Position not found or employee is already trained at this position')
                else:
                    print (f'{employee_name} has been succesfully trained at {position}')
        elif command == 'e':
            #Print out the full detailed employee list
            red_tag.print_employee_list(employee_list)
        elif command == 'n':
            print_rotation_result = red_tag.next_rotation(employee_list, ride, break_list, p_start, p_end, position_availability)
            try:
                if print_rotation_result[0]:
                    break_list = print_rotation_result[1]
                red_tag.print_ride(ride)
            except:
                continue
        elif command == 'r':
            confirm = input("Are you sure you want to proceed? This will delete all data. Type 'yes' to restart or press any key to continue this run")
            if confirm.lower() == "yes":
                print ("\n" *10)
                main()
        elif command == "+":
            #Create a new guy and add him to the break list
            new_guy = red_tag.add_an_employee(employee_list, p_start, p_end)
            break_list.append(new_guy)
            break_list = red_tag.make_break_list(break_list, len(break_list))

            print(new_guy.get_name() , "has been added, but we need a position for them to occupy.")
            #Create a new optional position and set this fellas position to the new position
            name = ride.add_optional_pos()
            ride.get_optional_pos_dict()[name][0] = new_guy.get_name()
            new_guy.set_pos(name)

            #If the new guy has already had break, adjust
            break_answer = ''
            if break_answer.lower() != 'y' and break_answer.lower() != 'n':
                break_answer = input("Has " + new_guy.get_name() + " had a break yet? Please enter y or n: ")
            if break_answer.lower() == 'y':
                time_answer = ''
                while (len(time_answer.split()))!= 2:
                    time_answer = input("What time did the break end? Enter in the form HH:MM")
                time_tokens = time_answer.split(':') 
                new_guy.set_break_status(True)
                new_guy.set_break_end(red_tag_classes.Time(time_tokens[0], time_tokens[1]))
            elif break_answer.lower() == 'n':
                print("Employee has been added successfully")
            else:
                print ("Inavalid input - continuing under the assumption that the break has not occured.")

        elif command == "-":
            if (len(employee_list) == ride.get_mins()):
                print ("You are at mins and cannot remove an employee")
            else:
                #You can remove an employee
                if len(command_tokens) != 2:
                    print ("Improper usage. Please use - <employee name>")
                else:
                    remove_employee = red_tag.find_employee_in_list(employee_list, command_tokens[1])
                    remove_employees_position = remove_employee.get_pos()
                    for pos in ride.get_pos_dict():
                        if pos == remove_employees_position:
                            red_tag.obliterate_employee(employee_list, break_list, ride.get_pos_dict(), remove_employee.get_name())
                            cont = True
                            break
                    for optional_pos in ride.get_optional_pos_dict():
                        if optional_pos == remove_employees_position:
                            red_tag.obliterate_employee(employee_list, break_list, ride.get_optional_pos_dict(), remove_employee.get_name())
                            del ride.get_optional_pos_dict()[optional_pos]
                            cont = False
                            break

                    #At this point the employee has been obliterated - lets fill the position with someone from optional
                    if cont:
                        print ("Please select the option you would like removed by entering the number in brackets after it is listed")
                        i = 0
                        optional_position_list = []
                        for optional_position in ride.get_optional_pos_dict():
                            print (optional_position, '[', i, ']', end=" --- ")
                            i += 1
                            optional_position_list.append(optional_position)

                        while True:
                            try:
                                choice = int(input("Please enter your choice now:"))
                                if choice >= len(optional_position_list):
                                    print('Please enter an index within range')
                                    continue
                                break
                            except ValueError:
                                print ("Please enter a number")
                        

                        position =  optional_position_list[choice]
                        employee_name_covering = ride.get_optional_pos_dict()[position][0]

                        if employee_name_covering != None:
                            employee_covering = red_tag.find_employee_in_list(employee_list, employee_name_covering)
                            employee_covering.set_pos(remove_employees_position)
                        ride.get_pos_dict()[remove_employees_position][0] = employee_name_covering
                        del ride.get_optional_pos_dict()[position]
        elif command == 'f':
            if len(command_tokens) != 2:
                print ("Improper usage. Please use the format 'f <employee name>")
            else:
                located = red_tag.find_employee_in_list(employee_list, command_tokens[1])
                if located == None:
                    print ("Employee not found, please try again")
                else:
                    print(repr(located))
        elif command == 't':
            print (red_tag_test_utils.test_dict_list_match(employee_list, ride.get_pos_dict(), ride.get_optional_pos_dict()))
        elif command == 'br':
            print (break_list)
        else:
            print ("Command not recognised - please enter h for options")
        

        

        command = input("Please enter the next command: ")

        




if __name__ == "__main__":
    main()