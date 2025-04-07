import sys
import src.extraction as exp
import src.transformation as trs
import src.visualization as vis

def answer(file):
    while True:
        try:
            trs.coord_file(file)
            break
        except:
            sys.exit()

while True:
    try:
        ans = input('Do you have Gaia DR3 data? [y/n]: ').strip().lower()
        if ans == 'n':
            while True:
                try:
                    ans1 = input("A million random sources? [y/n]: ").strip().lower()
                    if ans1 == 'n':
                        file = exp.gaia_query(False)
                        answer(file)
                        break
                    if ans1 == 'y':
                        file = exp.gaia_query(True)
                        answer(file)
                        break
                    if ans1 == 'exit':
                        print('Going back!')
                        sys.exit()
                    else:
                        print("Something happened! PD: Write 'exit' to leave")
                except:
                    break
        if ans == 'y':
            while True:
                try:
                    file_name = input('Write file name of Gaia DR3 data (e.g. gaia_raw.csv): ').strip().lower()
                    try:
                        answer(file_name)
                        break
                    except:
                        print("Wrong path or path not found! (Write 'Ctrl + C' to leave)")
                except:
                    break
        if ans == 'exit':
            print('See you later!')
            sys.exit()
        else:
            print("\nPD: Write 'exit' to leave")
    except SystemExit:
        sys.exit()
            



