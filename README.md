# Overview
By undertaking the challenge of learning how to connect python to a sql database, I hope to gain more understanding of how SQL language works behind the scenes of a GUI editor for the SQL language such as Workbench.


I have written software that connects to either a sqlite database or to Workbench, a tool that connects to a MySQL server. This program allows the user to add data into the database and then they can see the changes they have made.


I decided to write this program to help students learning about databases see what possibilities there are when it comes to creating a database; they can create one using a tool like Workbench or just by using python and the sqlite3 software. I also made this program to help me further understand how a database is created. 

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of how created the Relational Database.}

[Software Demo Video](http://youtube.link.goes.here)

# Relational Database

The database I am using is both a sqlite database and MySQL Workbench.

The structure of the database is as follows:

1. I have a parent table and a child table.
2. The parent table is called rating.
4. The child table is called game which relies on having a rating to be called a game.

# Development Environment

Visual Studio Code


Workbench


Python, sqlite3, and sql.connector


# Useful Websites

* [Youtube](https://www.youtube.com/watch?v=3vsC05rxZ8c&list=PLzMcBGfZo4-l5kVSNVKGO60V6RkXAVtp-&index=1)
* [Replit](https://replit.com/@NicholasBoss1/CSE310SQLDBWorkshop#main.py)
* [SQLDocumentation](https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html)

# Future Work

* Creating functionality for user to create their own database.
* Creating a prebuilt database as an option.
* Adding ability to edit dates.