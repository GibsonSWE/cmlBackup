from src import constants as c
from src import utils
from src import cml_api as cml

import sys
import time

def list_labs(token):
    print()
    labs = cml.get_labs(token)
    for n, lab_id in enumerate(labs):
        details = cml.get_lab_details(token, lab_id)
        state = cml.get_state(token, lab_id)
        print(f"[{n}] ({state}) | {details['lab_title']} ")
    print()
    return labs



def backup_lab(token, lab_id):
    lab_details = cml.get_lab_details(token, lab_id)
    name = lab_details['lab_title']

    state = cml.get_state(token, lab_id)
    initial_state = state
    if state != 'STARTED':
        response = cml.start_lab(token, lab_id, name)

    if cml.check_converged(token, lab_id) is False:
        print('Waiting for the lab to converge...')
        while True:
            converged = cml.check_converged(token, lab_id)
            if converged is True:
                print('The lab has fully converged')
                break

    response = cml.extract_config(token, lab_id)
    time.sleep(1)

    response = cml.download_lab(token, lab_id)
    with open(c.BACKUP_PATH+utils.snake(lab_details['lab_title'])+'.yaml', 'w') as file:
        file.write(response.text)

    if initial_state == "STARTED":
        return
    elif initial_state == "STOPPED":
        response = cml.stop_lab(token, lab_id, name)
        while True:
            state = cml.get_state(token, lab_id)
            if state == 'STOPPED':
                print('Lab stopped')
                break
    else:
        print(f"Initial state unknown: {initial_state}")
        print("Exiting")
        exit()


def iterate_through_labs(token):
    labs = cml.get_labs(token)

    for lab in labs:
        backup_lab(token, lab)


def main():
    if '--version' in sys.argv or '-v' in sys.argv:
        print(utils.show_version())

    elif '--help' in sys.argv or '-h' in sys.argv:
        print(utils.show_help())
    else:
        token = cml.get_token()
        labs = list_labs(token)
        user_choice = input('ID/all: ').lower()
        
        if user_choice == 'all':
            iterate_through_labs(token)
        elif user_choice == 'exit':
            exit()
        elif user_choice.isnumeric() is True:
            lab_list_id = int(user_choice)
            backup_lab(token, labs[lab_list_id])
        print('\nBackup complete')
        


if __name__ == "__main__":
    main()
    print()
