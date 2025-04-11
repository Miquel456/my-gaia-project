import sys
import src.extraction as ext

# MAIN PROGRAM
while True:
    try:
        ans = input('Do you have Gaia DR3 data? [y/n]: ').strip().lower()
        # ANSWER WITH 'n' TO GENERATE A NEW DATASET
        if ans == 'n':
            while True:
                try:
                    ans1 = input("A 500k random sources? [y/n]: ").strip().lower()
                    # ANSWER WITH 'n' TO GENERATE FIXED SOURCES (WILL ALWAYS BE THE SAME)
                    if ans1 == 'n':
                        file = ext.gaia_query(False)
                        ext.answer(file)
                        break
                    # ANSWER WITH 'y' TO GENERATE RANDOM SOURCES (EVERYTIME WILL BE DIFFERENT SOURCES)
                    if ans1 == 'y':
                        file = ext.gaia_query(True)
                        ext.answer(file)
                        break
                    # ANSWER 'exit' TO GO BACK
                    if ans1 == 'exit':
                        print('Going back!')
                        sys.exit()
                    # WHEN THE ANSWER DOES NOT MEET THE PREVIOUS CONDITIONS
                    else:
                        print("Something happened! PD: Write 'exit' to leave")
                except:
                    break
        # ANSWER WITH 'y' TO NOT GENERATE A NEW DATASET
        if ans == 'y':
            while True:
                try:
                    # INTRODUCE THE NAME OF THE FILE (BY DEFAULT ARE 'gaia_raw_fixed.csv' AND 'gaia_raw_random.csv')
                    file_name = input('Write file name of Gaia DR3 data (e.g. gaia_raw.csv): ').strip().lower()
                    try:
                        ext.answer(file_name)
                        break
                    # IF FILE CANNOT BE READ. PRESS 'Ctrl' AND 'C' TO EXIT
                    except:
                        print("Wrong path or path not found! (Write 'Ctrl + C' to leave)")
                except:
                    break
        # ANSWER WITH 'exit' TO EXIT
        if ans == 'exit':
            print('See you later!')
            sys.exit()
        # ANSWER WITH 'exit' TO EXIT
        else:
            print("\nPD: Write 'exit' to leave")
    except SystemExit:
        sys.exit()
            



