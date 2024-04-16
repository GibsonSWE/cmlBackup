from src import constants as c
from src import utils
from src import cml_api as cml

import sys
import time


def backup_labs():
    token = cml.get_token()
    labs = cml.get_labs(token)

    for lab in labs:
        lab_details = cml.get_lab_details(token, lab)
        name = lab_details['lab_title']

        state = cml.get_state(token, lab)
        if state != 'STARTED':
            response = cml.start_lab(token, lab, name)

        if cml.check_converged(token, lab) is False:
            print('Waiting for the lab to converge...')
            while True:
                converged = cml.check_converged(token, lab)
                if converged is True:
                    print('The lab has fully converged')
                    break

        response = cml.extract_config(token, lab)
        time.sleep(1)

        response = cml.download_lab(token, lab)
        with open(c.BACKUP_PATH+utils.snake(lab_details['lab_title'])+'.yaml', 'w') as file:
            file.write(response.text)

        response = cml.stop_lab(token, lab, name)
        while True:
            state = cml.get_state(token, lab)
            if state == 'STOPPED':
                print('Lab stopped')
                print()
                break


def main():
    if '--version' in sys.argv or '-v' in sys.argv:
        print(utils.show_version())

    elif '--help' in sys.argv or '-h' in sys.argv:
        print(utils.show_help())
    else:
        backup_labs()
        print('Backup complete')



if __name__ == "__main__":
    main()
    print()
