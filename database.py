from datetime import datetime
import sqlite3
import mysql.connector # the mysql connector was installed using pip install mysql-connector-python

# All functions to use for the program
def get_rating(cursor):
        cursor.execute("SELECT ratingName FROM rating")
        ratings = cursor.fetchall()
        for index in range(len(ratings)):
            print(f"{index+1}. {ratings[index][0]}")
        select = int(input("Select > "))
        return select
    
def get_title(cursor):
    cursor.execute("SELECT gameTitle FROM game")
    titles = cursor.fetchall()
    for index in range(len(titles)):
        print(f"{index+1}. {titles[index][0]}")
    choice = int(input("Select > "))
    return titles[choice-1][0]

def get_sqlrating(mycursor):
    mycursor.execute("SELECT ratingName FROM rating")
    ratings = mycursor.fetchall()
    for index in range(len(ratings)):
        print(f"{index+1}. {ratings[index][0]}")
    select = int(input("Select > "))
    return select

def get_sqlid(mycursor):
    mycursor.execute("SELECT gameId FROM game")
    ids = mycursor.fetchall()
    print("These ids are already in use. Please choose one that doesn't exist yet:")
    print("{:>10}  {:<10}".format("Selector", "Id"))
    for index in range(len(ids)):
        print(f"{index+1}. {ids[index][0]}")
    sel = int(input("Select > "))
    return sel

data = None
# program start. Asks user which method they want to use
while data != 3:
    print("Which database do you want to use?")
    print("1) SQL (Sqlite)") # use this option if you don't have Workbench installed.
    print("2) MySQL (Workbench)")
    print("3) Quit")
    data = int(input("Select > "))

    if data == 1: # if user chose '1' it takes them to the sqlite3 database
        db = sqlite3.connect('games.db')
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS rating ("
                            "ratingId INT UNSIGNED AUTO_INCREMENT NOT NULL,"
                            "ratingName VARCHAR(3) NOT NULL,"
                            "PRIMARY_KEY ratingId"
                            ")")
        cursor.execute("CREATE TABLE IF NOT EXISTS game ("
                                    "gameTitle VARCHAR(45) NOT NULL,"
                                    "gameDateReleased DATE,"
                                    "ratingId INT UNSIGNED NOT NULL,"
                                    "FOREIGN_KEY ratingId REFERENCES rating(ratingId),"
                                    "PRIMARY_KEY gameId"
                                    ")")

        mgames = [("Halo", '2001-11-15',1),
                ("The Legend of Zelda: Ocarina of Time", '1998-11-21',2),
                ("Assassin's Creed Black Flag", '2013-10-19',1)]

        # Initial inserts for testing. 
        #   MySQL INSERT QUERY (Parent table)
        cursor.execute("INSERT INTO rating (ratingId, ratingName) VALUES (1, 'M')") # Use this for ENUM values
        cursor.execute("INSERT INTO rating (ratingId, ratingName) VALUES (2,'E')") # Use this for ENUM values
        cursor.execute("INSERT INTO rating (ratingId, ratingName) VALUES (3,'T')") # Use this for ENUM values

        #   MySQL INSERT QUERY (Child Table)
        sqlInsertgame = "INSERT INTO game (gameTitle, gameDateReleased, ratingId) VALUES (?, ?, ?)"
        cursor.executemany(sqlInsertgame, mgames) # this works for multiple values in tuples
        print("Inserts complete")
        db.commit()

       
        choice = None
        while choice != 5:
            print("1) View games")
            print("2) Add game")
            print("3) Update game rating")
            print("4) Delete game")
            print("5) Return to previous menu")
            choice = int(input("Select > "))
            print()

            if choice == 1:
                cursor.execute("SELECT gameTitle, ratingName FROM game AS g JOIN rating AS r ON g.ratingId = r.ratingId")

                print("{:<45}          {:>10}".format("Title", "Rating"))

                for record in cursor.fetchall():
                    print("{:<45}     {:>10}".format(record[0],record[1]))
                print("\n")
            elif choice == 2:
                print("Enter a game title")
                title = input("Title: ")
                print("Date must be in YYYY-MM-DD format")
                day = input("Day(DD): ")
                if day == "today":
                    date = datetime.today().strftime('%Y-%m-%d')
                else:
                    month = input("Month(MM): ")
                    year = input("Year(YYYY): ")
                    date = (f"{year}-{month}-{day}")
                print("Enter the rating")
                rating = (get_rating(cursor))
                values = (title, date, rating)
                cursor.execute("INSERT INTO game (gameTitle, gameDateReleased, ratingId) VALUES (?,?,?)", values)
                db.commit()
                print("Game added to database.")
                print("\n")
            
            elif choice == 3:
                title = [input("Title: ")]
                print("Change rating to one of the following options")
                rating = get_rating(cursor)
                if rating == 1:
                    cursor.execute("UPDATE game SET ratingId = 1 WHERE gameTitle = ?", title)
                    print("Game rating updated to 'M'.")
                if rating == 2:
                    cursor.execute("UPDATE game SET ratingId = 2 WHERE gameTitle = ?", title)
                    print("Game rating updated to 'E'.")
                db.commit()
                
            elif choice == 4:
                title = get_title(cursor)
                values = (title,)
                cursor.execute("DELETE FROM game WHERE gameTitle = ?",values)
                db.commit()
                print("Game deleted from database.")
                print("\n")
                
    elif data == 2: # if user chose '2' it takes them to the Workbench database

        connection = mysql.connector.connect(host='localhost',user='root',password='password')
        print("Connected to Workbench.")
        print("\n")
        mycursor = connection.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS games")
        connection = mysql.connector.connect(host='localhost',user='root',password='password',database='games')
        mycursor = connection.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS rating ("
                            "ratingId INT UNSIGNED AUTO_INCREMENT NOT NULL,"
                            "ratingName VARCHAR(3) NOT NULL,"
                            "PRIMARY KEY (ratingId)"
                            ")ENGINE=INNODB")
        mycursor.execute("CREATE TABLE IF NOT EXISTS game ("
                                    "gameId INT UNSIGNED AUTO_INCREMENT,"
                                    "gameTitle VARCHAR(45) NOT NULL,"
                                    "gameDateReleased DATE,"
                                    "ratingId INT UNSIGNED NOT NULL,"
                                    "FOREIGN KEY (ratingId) REFERENCES rating (ratingId),"
                                    "PRIMARY KEY (gameId)"
                                    ")ENGINE=INNODB")
        
        mgames = [(1,"Halo", '2001-11-15',1),
                (2,"The Legend of Zelda: Ocarina of Time", '1998-11-21',2),
                (3,"Assassin's Creed Black Flag", '2013-10-19',1)]

        # Initial inserts for testing. 
        #   MySQL INSERT QUERY (Parent tabl e)
        # mycursor.execute("INSERT INTO rating (ratingId, ratingName) VALUES (1, 'M')") # Use this for ENUM values
        # mycursor.execute("INSERT INTO rating (ratingId, ratingName) VALUES (2,'E')") # Use this for ENUM values
        # mycursor.execute("INSERT INTO rating (ratingId, ratingName) VALUES (3,'T')") # Use this for ENUM values

        #   MySQL INSERT QUERY (Child Table)
        # sqlInsertgame = "INSERT INTO game (gameId, gameTitle, gameDateReleased, ratingId) VALUES (%s, %s, %s, %s)"
        # mycursor.executemany(sqlInsertgame, mgames) # this works for multiple values in tuples
        # print("Inserts complete")
        connection.commit()
        

        choice = None
        while choice != 5: # gives user options in the database
            print("1) View games")
            print("2) Add game")
            print("3) Update game rating")
            print("4) Delete game")
            print("5) Return to previous menu")
            choice = int(input("Select > "))
            print()

            if choice == 1: # Display's the game's information
                mycursor.execute("SELECT gameId, gameTitle, ratingName FROM game AS g JOIN rating AS r ON g.ratingId = r.ratingId ORDER BY gameId")

                print("{:>10}  {:>45}    {:>10}".format("GameId","Title", "Rating"))

                for record in mycursor.fetchall():

                    print("{:>10}  {:>45}   {:>10}".format(record[0],record[1],record[2]))
                print("\n")

            elif choice == 2: # Adds a game to the database
                print("Enter a game title")
                title = input("Title: ")
                print("Enter the rating")
                rating = get_sqlrating(mycursor)
                print("\n")
                id = get_sqlid(mycursor)
                print("Date must be in YYYY-MM-DD format (Type 'today' for today's date)")
                day = input("Day(DD): ")
                if day == "today":
                    date = datetime.today().strftime('%Y-%m-%d')
                else:
                    month = input("Month(MM): ")
                    year = input("Year(YYYY): ")
                    date = (f"{year}-{month}-{day}")
                values = (id,title,date,rating)
                mycursor.executemany("INSERT INTO game (gameId, gameTitle, gameDateReleased, ratingId) VALUES (%s,%s,%s,%s)", (values,))
                connection.commit()
                print("Game added to database.")
                print("\n")

            elif choice == 3: # Updates the rating of a game
                title = [input("Title: ")]
                print("Change rating to one of the following options")
                rating = get_sqlrating(mycursor)
                if rating == 1:
                    mycursor.execute("UPDATE game SET ratingId = 1 WHERE gameTitle = %s", title)
                    connection.commit()
                    print("Game rating updated to 'M'.")
                    print("\n")
                if rating == 2:
                    mycursor.execute("UPDATE game SET ratingId = 2 WHERE gameTitle = %s", title)
                    connection.commit()
                    print("Game rating updated to 'E'.")
                    print("\n")

            elif choice == 4: # Deletes a game
                title = get_title(mycursor)
                values = (title,)
                mycursor.execute("DELETE FROM game WHERE gameTitle = %s",values)
                connection.commit()
                print("Game deleted from database.")
                print("\n")
  
    elif data == 3:
        print("Program ended")
        quit()


