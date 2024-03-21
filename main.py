import sqlite3
import hashlib
import getpass
#imports sqilite3, hashlib and getpass modules

#Connects to the database
connection = sqlite3.connect("Eldritch Library Management Database.db")
#creates a cursor to interact with the database
cursor = connection.cursor()
#This creates a table if it does not exists for users
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, role TEXT)")
#Also creates a table if it does not exists for books
cursor.execute(
    "CREATE TABLE IF NOT EXISTS books (title Text, author TEXT, isbn INT, stock INT)")
#Funtion to register new users
def register ():
  #prompts the users to enter a username
  username = input("Enter your username: ")
  #prompts the user to enter a password while input is hidden
  password = getpass.getpass("Enter your password: ")
  #Assigns the admin or guest role
  role = input("Assign role (admin/guest): ")
  #inputs the above info into the database
  cursor.execute("INSERT INTO users VALUES (?,?,?)", (username, password, role))
  #pushes the changes into the database
  connection.commit()
  #prints the message "regisration successful"
  print("Registration successful!")
#function for login
def login():
  username = input("Enter your username: ")
  password = getpass.getpass("Enter your password: ")
  #An SQL query to see if username and password matches
  cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
  #Checks the database for similar details in database
  user = cursor.fetchone()
  #if statement to check if creditials are correct
  if user:
    print("Login successful!")
    #returns the username of the logged in user
    return user[0]
  #Else statement and error message if incorrect username or password
  else:
    print("Invalid username or password.")
    return None
#function to display all books in database
def display_all_books():
  #connects to the database
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  #connects to the cursor which interacts with the database
  cursor = connection.cursor()
  #SQL query to select all books from the database
  cursor.execute('''
    SELECT * FROM books
    ''')
  #Fetches all the books returned by the query 
  books = cursor.fetchall()
  #checks to see if books are in the database
  if books:
    #if books are in the database, prints the books in columns
    print ("Title\t\tAuthor\t\tISBN\t\tavailable")
    #provides seperations between columns 
    print("-" * 50)
    #loops through each book in the books list
    for book in books:
    #prints the book details in columns using f string
      print (f" {book[0]:<8} | {book[1]:<10} | {book[2]:<10} | {book[3]:<10}")
  #if no books in database, print this message
  else:
    print("No books in library")
  #closes the database
  connection.close()
#function to add a new book to the database
def add_book():
  #prompts or users to enter details of the book
  title = input("Enter the title of the book: ")
  author = input("Enter the author of the book: ")
  isbn = input("Enter the ISBN of the book: ")
  stock = input("Enter the number of copies of the book: ")
  #An SQL query to assign details into "books" table
  cursor.execute("INSERT INTO books VALUES (?,?,?,?)", (title, author, isbn, stock))
  #commits changes to the database
  connection.commit()
  print("Book has been added successfully!")
#function to remove books from the database
def remove_book():
  #prompts the user to enter the isbn of book to remove
  isbn = input("Enter the ISBN of the book to remove: ")
  #An SQL query to remove the book from the database based on isbn
  cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
  #commits changes to the database
  connection.commit()
  print("Book has been removed successfully!")
#Funtion to update stock value 
def update_book_stock():
  #Prompts user to enter isbn number of book to update stock
  isbn = input("Enter the ISBN of the book to update: ")
  new_stock = input("Enter number of stock: ")
  #SQL query to updaye the stock number of the book by isbn
  cursor.execute("UPDATE books SET stock = ? WHERE isbn = ?", (new_stock, isbn))
  #commits changes to the database, prints update has been successful
  connection.commit()
  print("Book stock has been updated successfully!")
#function to search for books in the database
def search_book():
  #prompts the users to enter title of book they wish to search for
  search_term = input("Enter the title of the book you would like to search: ")
  #connections to database
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  #connects the cursor to interact with the database
  cursor = connection.cursor()
  #SQL query to search for books in the database
  cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + search_term + '%',))
  books = cursor.fetchall()
  #check if any of the books matches the search term
  if books:
    #print columns for title, author, isbn and books stock
    print ("Title\t\tAuthor\t\tISBN\t\tAvailable")
    #creates lines for seperation
    print ("-" * 50)
    #loops through each book in the books list
    for book in books:
      print (f" {book[0]:<20} | {book[1]:<20} | {book[2]:<20} | {book[3]:<20}")
  else:
    print ("No books are currantly available in the Libary")
#funtion to borrow books from database
def borrow_book():
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  #execute sql query to select all books from the database
  cursor.execute('''
    SELECT * FROM books
    ''')
  #Fetches all books which are available in the library
  books = cursor.fetchall()
  #checks to see if books are in the database
  if books:
    print ("Title\t\tAuthor\t\tISBN\t\tAvailable")
    print ("-" * 50)
    for book in books:
    #formatsand prints the books details using f strings
      print (f" {book[0]:<8} | {book[1]:<10} | {book[2]:<10} | {book[3]:<10}")
    #prompts user to enter the isbn of the book they want to borrow
    isbn = input("Enter the isbn of the book you wish to borrow: ")
  #SQL query to select the book from the database based on isbn
    cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
  #fetches the first matching record returned by the query
    book = cursor.fetchone()
#checks to see if the books are available from the database
    if book:
      #checks if books are available to borrow
      if book[3] > 0:
        #if the book is available, prompts user to enter isbn number of book to borrow
        cursor.execute("UPDATE books SET available = available - 1 WHERE isbn = ?", (isbn))
        connection.commit()
        print("Book borrowed successfully!")
      #prints the messages based on the booke availability
      else:
        print("Sorry, the book is currently not available.")
    else:
      print("Unable to find book.")
  else:
    print ("No books are available in the Libary")
  #closes the database
  connection.close()
#Function to return book to the database
def return_book():
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  #execute sql query to select all books from the database
  cursor.execute('''
    SELECT * FROM books
    ''')
  books = cursor.fetchall()
  #if statement to check if books are in the database
  if books:
    print ("Title\t\tAuthor\t\tISBN\t\tAvailable")
    print ("-" * 50)
  #Reads for books information and prints it in columns
    for book in books:
      #formats and print book information with use of f strings
      print (f" {book[0]:<8} | {book[1]:<10} | {book[2]:<10} | {book[3]:<10}")
    #prompts user to enter the isbn of the book they want to return
    isbn = input("Enter the isbn of the book to return: ")
    cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
    #fetches the first matching record returned by the query
    book = cursor.fetchone()
    #checks to see if the book is available in the database
    if book:
      if book[3] < book[2]:
        #SQL quest to update book in database
        cursor.execute("UPDATE books SET available = available + 1 WHERE isbn = ?", (isbn,))
        #commits changes to the database
        connection.commit()
        #prints the message book has been returned successfully
        print("Book has been returned successfully!")
      else:
        print("Sorry, the book is unable to be returned.")
    else:
      print("Book not found.")
  else:
    print ("No books are available in the Libary")
  connection.close()
#Creates a function to display all users in the database
def display_all_users():
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  #SQL query to select all users in the database
  cursor.execute('''
    SELECT * FROM users
    ''')
  #Fetches all users from the database
  users = cursor.fetchall()
  #if statement to check if users are in the database
  if users:
    print ("Username\tRole")
    print ("-" * 50)
  #interates through each user and prints their details in columns
    for user in users:
      print (f" {user[0]:<10} | {user[1]:<10}")
  else:
    print ("No users are available in the Libary")
  connection.close()
#Function to update user roles
def update_user_role():
  #prompts user to enter username of user to update role
  username = input("Enter the Username of the user to update: ")
  #prompts user to enter new role of user
  role = input("Enter the new role of the user (admin/user): ")
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  #SQL query to update user role in the database
  cursor.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
  print("User role has been updated successfully!")
  connection.commit() 
#Function to sort books by isbn
def sort_books_by_isbn():
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  cursor.execute( 'SELECT * FROM books ORDER BY isbn')
  books = cursor.fetchall()
  #checks if any books are in the library 
  if books:
    #print a message stating books are sorted by isbn
    print ("Books sorted by isbn")
    #prints books into columns
    print ("Title\t\tAuthor\t\tISBN\t\tAvailable")
    #Prints seperator lines to seperate column headers from data
    print ("-" * 50)
    #iterates through each book, prints the data
    for book in books:
      print (f" {book[0]:<8} | {book[1]:<10} | {book[2]:<10} | {book[3]:<10}")
  else:
    print ("No books are available in the Libary")
  connection.close()
#Function for main 
def main():
  #prints the following message out into terminals
  while True:
    print("Welcome to the Eldritch Library Management System!")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    #users are promted to enter a choice
    choice = input("Enter your choice: ")
    #if statement to check if choice is 1, connects to register function
    if choice == "1":
      register()
    #elif statement to check if choice is 2, connects to login function
    elif choice == "2":
      user = login()
      #Checks to see if users is a guest
      if user == 'guest':
        while True:
          print("Welcome, " + user + "!")
          #Calls the functions to display/borrow/return books
          print("1. Display books")
          print("2. Borrow a book")
          print("3. Return a book")
          print("4. Exit")
          choice = input("Enter your choice: ")
          if choice == "1":
            display_all_books()
          elif choice == "2":
            borrow_book()
          elif choice == "3":
            return_book()
          elif choice == "4":
            #exist the loop if user wishes to leave
            break
          else:
            #print statement if incorrect input
            print("Invalid choice. Please try again.")
      #elif to check if user is an admin
      elif user == 'admin':
        while True:
          print("Welcome, " + user + "!")
          print("1. Display books")
          print("2. Add a book")
          print("3. Remove a book")
          print("4. Update book stock")
          print("5. Search for a book")
          print("6. Sort books by isbn")
          print("7. Display all users")
          print("8. Update user role")
          print("9. Exit")
          choice = input("Enter your choice: ")
          #if and elif to call the respective functions
          if choice == "1":
            display_all_books()
          elif choice == "2":
            add_book()
          elif choice == "3":
            remove_book()
          elif choice == "4":
            update_book_stock()
          elif choice == "5":
            search_book()
          elif choice == "6":
            sort_books_by_isbn()
          elif choice == "7":
            display_all_users()
          elif choice == "8":
            update_user_role()
          elif choice == "9":
            #breaks the loop if user wishes to leave
            break
          else:
            print("Invalid choice. Please try again.")
    elif choice == "3":
      break
    else:
      print("Invalid choice. Please try again.")
#Checks to see if the script is running
if __name__ == "__main__":
#if script is running, call the main function to start program
  main()


