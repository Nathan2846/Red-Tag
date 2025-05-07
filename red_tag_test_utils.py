import red_tag
import red_tag_classes

def test_dict_list_match(employee_list, positions_dict, optional_positions_dict):
    for employee in employee_list:
        list_value = employee.get_pos() #The position of the meployee object
        if list_value.lower() == "break":
            continue
        try:
            dict_value = positions_dict[list_value][0] #The name of the employee at that dict key
        except:
            try: 
                dict_value = optional_positions_dict[list_value][0]
            except:
                print(list_value , " not found in either dict")
                return False
        
        if employee.get_name() != dict_value:
            print(employee, ' is out of compliance')
            return False
    return True


# Provides a full readout of all ride attributes
def full_readout(ride):
    print (f'Ride mins: {ride.get_mins()}')
    print (f'Mandatory positions: {ride.get_pos_dict().keys()}' )
    print (f'Optional positions: {ride.get_optional_pos_dict().keys()}')
    print (f'Current break order:', end= '')
    for e in ride.get_break_list():
        print (e.get_name())
    print (f'Current position_availability {ride.get_position_availability()}')
    print (f'*' * 30)

    for e in ride.get_employee_list():
        print (f'Name: {e.get_name()} |Position: {e.get_pos()}|Untrained positions: {e.get_untrained_positions()}')