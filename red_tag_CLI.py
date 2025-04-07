from tkinter import E
import red_tag
import red_tag_classes
import red_tag_test_utils

def testing():


    #test data
    p_start = red_tag_classes.Time(11,00)
    p_end = red_tag_classes.Time(20,00)

    #Create a ride object with 7 positions for Laff Trakk
    ride = red_tag_classes.Ride('Laff Trakk',7)
    ride.add_to_dict('load', [None, True, False])
    ride.add_to_dict('unload', [None, True, False])
    ride.add_to_dict('dispatch', [None, True, False])
    ride.add_to_dict('operate', [None, True, False])
    ride.add_to_dict('grouper', [None, False, False])
    ride.add_to_dict('merger', [None, False, True])
    ride.add_to_dict('frontline', [None, False,True])
    number_positions = 9
    ride.set_current_time(p_start)

    #Create an employee_list with 7 people who can legally work laff trakk
    employee_list = []
    employee_list.append(red_tag_classes.Employee('Lead','18',red_tag_classes.Time(10,00), red_tag_classes.Time(20,30)))
    employee_list.append(red_tag_classes.Employee('Minor1','17',red_tag_classes.Time(11,00), red_tag_classes.Time(19,30)))
    employee_list.append(red_tag_classes.Employee('Minor2','16',red_tag_classes.Time(11,00), red_tag_classes.Time(19,30)))
    employee_list.append(red_tag_classes.Employee('OnlyClerk','15',red_tag_classes.Time(11,00), red_tag_classes.Time(16,0)))
    employee_list.append(red_tag_classes.Employee('Adult1','18',red_tag_classes.Time(10,15), red_tag_classes.Time(20,30)))
    employee_list.append(red_tag_classes.Employee('Adult2','18',red_tag_classes.Time(10,15), red_tag_classes.Time(20,30)))
    employee_list.append(red_tag_classes.Employee('Adult3','18',red_tag_classes.Time(10,15), red_tag_classes.Time(20,30)))

    #Add the optional position and person to simulate breaks
    ride.add_to_opt_dict("ADA", [None, True, False])
    employee_list.append(red_tag_classes.Employee('Adult4','18',red_tag_classes.Time(10,15), red_tag_classes.Time(20,30)))

    # #For testing multiple optional positions
    # ride.add_to_opt_dict("Exit gate", [None, True, False])
    # employee_list.append(red_tag_classes.Employee("Adult5", '18', red_tag_classes.Time(10, 15) , red_tag_classes.Time(20, 30)))
    

    #Create the ordered break list
    break_list = red_tag.make_break_list(employee_list, number_positions)


    return [True, ride, number_positions, p_start, p_end, employee_list, break_list]


    # return [False]





def main():
    data = [False]
    startup = input("Welcome user. Please type 'test' to run current testing configuration or press enter to begin full run ")

    #Allows us to run the testing configuration if needed
    if startup == 'test' or startup == 'Test':
        data = testing()
    #Otherwise, run the full program
    if startup != "test" or startup != "Test" or data[0]:
        #Setup
        if (not data[0]):
            #Call all of the functions to get the data
            ride, number_positions = red_tag.gather_ride_data()
            p_start, p_end = red_tag.gather_park_data()
            ride.set_current_time(p_start) #Set thet time to the start of the park
            employee_list = red_tag.gather_employee_data(number_positions, p_start, p_end, ride)
            break_list = red_tag.make_break_list(employee_list, number_positions)
            position_availability = red_tag.calculate_position_availability(employee_list, ride)

        if (data[0]):
            #Take all data from the testing configuration
            ride, number_positions, p_start, p_end, employee_list, break_list= data[1], data[2], data[3], data[4], data[5], data[6]
            position_availability = red_tag.calculate_position_availability(employee_list, ride)


        #Get started and print the first rotation
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
                #Print out te full detailed employee list
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