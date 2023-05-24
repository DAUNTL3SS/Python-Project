# Course Project CS340 - PART A - Vaggelis Chasiotis - SPRING I 2023
# This project is about statistical information regarding the 2022 football world cup, Enjoy!
# BONUS QUESTION PLACED IN OPTION 4 - Creates a new column of the number of each player's chances and
#                                     implements it with the rest of the columns.

# Libraries
import pandas as pd  # Library for framing the data
import matplotlib.pyplot as plt  # Library for forming the graph

# Initializing the data and the data frame
df = pd.read_csv("top_scorers_Qatar2022.csv")  # Opening the file using the pandas library with the name df as dataframe
# GFP -> Goals From Penalty, SOT -> Shots on Target, AVG_SD -> Average Shot Distance
header_names = ["PLAYERS", "TEAM", "AGE", "GOALS", "GFP", "SHOTS", "SOT", "AVG_SD"]  # Changing the column names
df.columns = header_names  # Replacing the new column names with the previous ones
df['PLAYERS'] = df['PLAYERS'].str.split('_').str[0]  # Removing the second part of the Players' names
option3 = False
option4 = False

# THE PROGRAM STARTS HERE!
while True:  # Creating an infinite loop in order to display the menu after the completion of all options
    try:  # Creating an error handling condition to run the program as long as an exception is thrown

        # Creating the frame of the menu
        print()
        print("Welcome to the World Cup 2022 Top Scorers program")
        print("Please enter one of the following\n")
        print("\t1. Read & display stats from the top goal scorers")
        print("\t2. Display player shooting distance avg past a threshold")
        print("\t3. Calculate the goal/shot and non-penalty-goal/shot ratio metadata")
        print("\t4. Display menu with additional stats")
        print("\t5. Sort by a field")
        print("\t6. Visualize the processed metadata")
        print("\t7. Exit")
        print()

        option = int(input("Enter your option:"))  # Asking for users input

        # Option 1 code
        if option == 1:
            print("You've entered option 1...")
            print("This option shows a table with the statistics of some significant \n"
                  "football players of the 2022 World Cup")
            print()
            print(df)  # Refers to the dataframe created above and just displays it
            print()
            enter = input("Press anything to continue...")
            continue
        # Option 2 code
        elif option == 2:
            print()
            print("You've entered Option 2...")
            print("This option asks the user for an average shooting distance threshold,\n"
                  "and displays the stats from that distance and higher.")
            print()
            df2 = df  # Creating a new table called df2 (dataframe2) with the data of the beginning table

            # Asking the user for a threshold input
            threshold = float(input("Enter a threshold for the shooting distance:"))
            # Command that refers to the column named "AVG_DD" of the df2 table and displays data above the threshold
            df2 = df2[df2["AVG_SD"] > threshold]
            print(df2)
            print()
            enter = input("Press anything to continue...")
            continue

        # Option 3 code
        elif option == 3:
            print()
            print("You've entered option 3...")
            print("This option Calculates the goals/shot and non-penalty-goals/shot ratios")
            print()
            df3 = df  # Creating a new table called df3 (dataframe3) with the data of the beginning table
            df3["GOALS_PER_SHOT"] = round(df3["GOALS"] / df3["SHOTS"], 2)  # Creating a new column which result comes
            # up from dividing data from columns "goals" and "shots"
            df3["NON_PENALTY_GOALS_PER_SHOT"] = round((df3["GOALS"] - df3["GFP"]) / df3["SHOTS"], 2)  # Creating a
            # new column which result comes up from subtracting data from columns "goals" and "gfp" divided by "shots"
            with open('Chasiotis_qatar2022_stats.txt',
                      'w') as file:  # Creating a new txt file and begins the writing mode
                df3 = df3.rename(columns={"GOALS_PER_SHOT": 'G/S'})  # Renaming the column
                df3 = df3.rename(columns={"NON_PENALTY_GOALS_PER_SHOT": 'NPG/S'})  # Renaming the column
                file.write(df3.to_string(index=False))  # Adding the new data with the initial data

            f = open('Chasiotis_qatar2022_stats.txt', 'r')  # Opening the new file and e
            data = f.read()  # read the data of the new table
            print(data)  # prints the table including the 2 new columns
            f.close()  # closing the file

            print()
            option3 = True  # Enables the boolean variable since option 3 was chosen
            enter = input("Press anything to continue...")
            continue

        # Option 4 code
        elif option == 4:
            # Creating a condition in case option 3 chosen prior to choosing option 6
            if not option3:  # if option 3 was not chosen, display the result to go and choose it first
                print("Unfortunately you are required to have chosen option 3 before proceeding with this option. "
                      "Please come back after doing option 3")
                continue  # if option 3 was chosen, proceed...
            print("You've entered option 4...")
            print("This option is going to display the manu, plus the chances that each player created")
            print()
            df4 = df3  # Creating a new table
            chances = [2, 5, 2, 11, 17, 2, 2, 0, 6, 5, 3]  # Creating a list with the # of chances of each player
            df4.insert(loc=7, column='CHANCES', value=chances)  # Inserting the column specifically at the index 7
            # with the values of the list 'chances'
            with open('Chasiotis_qatar2022_stats_bonus.txt',
                      'w') as file:  # Creating a new txt file and begins the writing mode
                file.write(df4.to_string(index=False))  # Adding the new data with the initial data

            print(df4)
            option4 = True  # Creating this boolean in order to include the chances in the sorting option too
            print()
            enter = input("Press anything to continue...")
            continue

        # Option 5 code
        elif option == 5:
            # Creating a condition in case option 3 chosen prior to choosing option 4
            if not option3:  # if option 3 was not chosen, display the result to go and choose it first
                print("Unfortunately you need to complete option 3 before proceeding with this option...")
            if not option4:
                print("Sorry but you need to complete option 4 also...")
                continue  # if option 3 and 4 were chosen, proceed...
            print()
            print("You've entered option 5...")
            print("This option allows you to choose a field of your liking and the program will sort it")

            df5 = df4  # Creating a new table called df5 (dataframe5) with the data of the option 3 table

            # Creating a variable that assigns a number to each column
            fields = {1: 'PLAYERS', 2: 'TEAM', 3: 'AGE', 4: 'GOALS', 5: 'GFP', 6: 'SHOTS', 7: 'SOT', 8: 'CHANCES',
                      9: 'AVG_SD', 10: 'G/S', 11: 'NPG/S'}
            while True:  # Condition to run for as long as the user inputs the number for the fields
                try:  # Creating an error handling condition to run the program for as long as an exception is thrown
                    # Asking for users input for choosing a field for sorting
                    field = int(input("Please select one of the following fields for sorting:\n"
                                      "\t1) Players\n"
                                      "\t2) Team\n"
                                      "\t3) Age\n"
                                      "\t4) Goals\n"
                                      "\t5) Goals from Penalty\n"
                                      "\t6) Shots\n"
                                      "\t7) Shots on Target\n"
                                      "\t8) Chances\n"
                                      "\t9) Average Shot distance\n"
                                      "\t10) Goals per Shot\n"
                                      "\t11) Non-Penalty Goals per Shot\n"
                                      "Your choice: "))
                    if field not in fields:  # if input is not within the number of fields,
                        raise ValueError  # throw a ValueError
                    break
                except ValueError:  # Error trap message for wrong inputs
                    print("Invalid input. Please enter a number between 1 and 11: ")

            while True:  # Condition to run for as long as the user inputs the number for the sorting order
                try:  # Creating an error handling condition to run the program for as long as an exception is thrown
                    # Asking for users input for choosing a sorting order
                    order_field = int(input("\n\n Please select a sorting order:\n"
                                            "\t1) Ascending\n"
                                            "\t2) Descending\n"
                                            "Your choice: "))
                    if order_field not in [1, 2]:  # if input is not within the number of sorting order
                        raise ValueError  # throw a Value error
                    break
                except ValueError:  # Error trap for wrong inputs
                    print("Invalid input. Please enter 1 or 2: ")

            # Creating a new variable called sort that gets the field from the variable fields
            sort = fields[field]
            # Then run the sort command according to which field is stored in the variable 'sort'
            df5 = df5.sort_values(by=sort, ascending=(order_field == 1))
            # prints the sorted table
            print(df5)
            print()
            enter = input("Press anything to continue...")
            continue

        # Option 6 code
        elif option == 6:
            # Creating a condition in case option 3 chosen prior to choosing option 6
            if not option3:  # if option 3 was not chosen, display the result to go and choose it first
                print("Unfortunately you are required to have chosen option 3 before proceeding with this option. "
                      "Please come back after doing option 3")
                continue  # if option 3 was chosen, proceed...
            print()
            print("You've entered option 6...")
            print("This option displays the new data in a form of graph")

            players = df3['PLAYERS']  # players variable that contains data from the PLAYERS column
            goals = df3['GOALS']  # goals variable that contains data from the GOALS column
            shots = df3['SHOTS']  # shots variable that contains data from the SHOTS column

            plt.bar(players, goals, color='r')  # Making the goals data for the players with color red
            plt.bar(players, shots, align='center', bottom=goals,
                    color='b')  # Making the shots data behind the goals data with color blue
            plt.xticks(players, fontsize=7,
                       rotation=-40)  # Changing the font size and the rotation of the Player's display data
            plt.xlabel('Players')  # Creating a players label on the x_axis
            plt.ylabel('Goals per Shots')  # Creating a Goals per Shots label on the y_axis
            plt.title('Qatar 2022 World Cup Player Stats (Players/Goals Per Shots)')  # Creating a title
            plt.show()  # Displaying the final graph

        # Option 7 code
        elif option == 7:
            print("Thanks for using the program... Bye!")
            break  # Break as long as the user inputs number 7
        else:  # condition in case user inputs a different number than 1-7
            print()
            print("The menu has only 7 options!")

    except ValueError:  # error trap for character inputs
        print()
        print("You need to type the options in numbers!")
