import csv
from os import path
from PasswordHash import *

"""
Future improvements

Use a database instead of csv
Ask user to enter old password before changing
Include a GUI like Tkinter / Flask
"""

def createUser():

    # Create a csv file if none exists already
    if not path.exists("Users.csv"):
        file = open("Users.csv", "w")
        file.close()

    # Set variables and open csv to convert to list
    file = list(csv.reader(open("Users.csv")))
    tmp = []
    userExists = True
    userID = ""
    password = ""

    # Username must be unique, error handling if not
    while userExists:
        userID = input("Please enter a user ID: ")
        for row in file:
            tmp.append(row[0])  # Create a list of usernames to check against
        if userID in tmp:
            print("User already exists")
        else:
            password = createPassword()  # If username doesn't exist, ask user to create password
            password = hashPassword(password)  # md5 hash the password before saving
            print("Password saved")
            userExists = False

    # Add the new username and password to the csv file
    file = open("Users.csv", "a")
    newUser = userID + "," + password + "\n"
    file.write(newUser)
    file.close()



def createPassword():

    # As per book exercise, password scored on a points system
    points = 0
    specialChar = ["!", "£", "$", "%", "&", "<", "*", "@"]

    passwordCreate = str(input("Please enter a new password for this user:"))

    if len(passwordCreate) >= 8:  # 1 point for 8 characters or longer
        points += 1
    for char in passwordCreate:  # 1 Point if there is an uppercase letter
        if char.isupper():
            points += 1
            break
    for char in passwordCreate:  # 1 Point if there is an lowercase letter
        if char.islower():
            points += 1
            break
    for char in passwordCreate:  # 1 point if it contains a number
        if char.isnumeric():
            points += 1
            break
    for char in passwordCreate:  # 1 point if there is a special character from the list above
        if char in specialChar:
            points += 1
            break

    passwordCheck = passwordStrength(points, passwordCreate)  # Check password strength

    return passwordCheck


def passwordStrength(score, passwordStrength):

    # Checks the strength of a password and returns a suitable message
    passwordNew = ""
    if score < 3:  # If password is too weak, user must create a stronger password
        print("Password too weak")
        passwordNew = createPassword()
    elif 2 < score < 5:  # If password doesn't meet all conditions, user informed and given opportunity to create new
        check = False
        while not check:
            change = input("Password could be improved, would you like to change it? (y/n)")
            if change.lower() == "y":
                passwordNew = createPassword()
                check = True
            elif change.lower() == "n":
                passwordNew = passwordStrength
                check = True
            else:
                print("Please enter a valid selection")
    else:
        print("You have selected a strong password")
        passwordNew = passwordStrength  # Setting password to new password if not storing enough or user changes

    return passwordNew


def changePassword():

    # Changes a users password if that user exists
    file = list(csv.reader(open("Users.csv")))
    tmp = []
    userID = input("Please enter a user ID: ")

    # Creates a list of usernames and gets index of username entered
    for row in file:
        tmp.append(row[0])
    if userID in tmp:
        index = tmp.index(userID)
        currentPassword = input("Please enter your current password: ")
        currentPassword = hashPassword(currentPassword)

        # Updates list to include passwords
        tmp = []
        for row in file:
            tmp.append(row)

        # Changes the password for the user (based on index above)
        if currentPassword == tmp[index][1]:
            newPassword = createPassword()
            newPassword = hashPassword(newPassword)
            tmp[index][1] = newPassword
            # Writers the updated list with new password back to csv
            file = open("Users.csv", "w")
            x = 0
            for row in tmp:
                newRec = tmp[x][0] + "," + tmp[x][1] + "\n"
                file.write(newRec)
                x += 1
            file.close()
            print("Password successfully changed")
        else:
            print("Passwords do not match")
    else:
        print("User does not exist")


def displayUsers():

    # Displays a list of all current users
    file = open("Users.csv", "r")
    reader = csv.reader(file)
    rows = list(reader)
    for row in rows:
        print(row[0])
    file.close()


quit = False

while not quit:

    print("""
    1) Create a new user ID
    2) Change a password
    3) Display all user IDs
    4) Quit\n""")

    try:
        choice = int(input("Please select an option: "))

        if choice == 1:
            createUser()
        elif choice == 2:
            changePassword()
        elif choice == 3:
            displayUsers()
        elif choice == 4:
            quit = True
        else:
            print("Please select a valid option")

    except ValueError:
        print("Please select a number")
