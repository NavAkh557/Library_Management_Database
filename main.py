import sqlite3
import hashlib
import getpass

connection = sqlite3.connect("Eldritch Library Management Database.db")
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, role TEXT)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS books (title Text, author TEXT, isbn INT, stock INT)")
def register ():
  username = input("Enter your username: ")
  password = getpass.getpass("Enter your password: ")
  role = input("Assign role (admin/guest): ")
  cursor.execute("INSERT INTO users VALUES (?,?,?)", (username, password, role))
  connection.commit()
  print("Registration successful!")
def login():
  username = input("Enter your username: ")
  password = getpass.getpass("Enter your password: ")
  cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
  user = cursor.fetchone()
  if user:
    print("Login successful!")
    return user[0]
  else:
    print("Invalid username or password.")
    return None
def display_all_books():
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  cursor.execute('''
    SELECT * FROM books
    ''')
  books = cursor.fetchall()
  if books:
    print ("Title\t\tAuthor\t\tISBN\t\tavailable")
    print("-" * 50)
    for book in books:
      print (f" {book[0]:<8} | {book[1]:<10} | {book[2]:<10} | {book[3]:<10}")
  else:
    print("No books in library")
  connection.close()
def add_book():
  title = input("Enter the title of the book: ")
  author = input("Enter the author of the book: ")
  isbn = input("Enter the ISBN of the book: ")
  stock = input("Enter the number of copies of the book: ")
  cursor.execute("INSERT INTO books VALUES (?,?,?,?)", (title, author, isbn, stock))
  connection.commit()
  print("Book has been added successfully!")
def remove_book():
  isbn = input("Enter the ISBN of the book to remove: ")
  cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
  connection.commit()
  print("Book has been removed successfully!")
def update_book_stock():
  isbn = input("Enter the ISBN of the book to update: ")
  new_stock = input("Enter number of stock: ")
  cursor.execute("UPDATE books SET stock = ? WHERE isbn = ?", (new_stock, isbn))
  connection.commit()
  print("Book stock has been updated successfully!")
def search_book():
  search_term = input("Enter the title of the book you would like to search: ")
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + search_term + '%',))
  books = cursor.fetchall()
  if books:
    print ("Title\t\tAuthor\t\tISBN\t\tAvailable")
    print ("-" * 50)
    for book in books:
      print (f" {book[0]:<20} | {book[1]:<20} | {book[2]:<20} | {book[3]:<20}")
  else:
    print ("No books are currantly available in the Libary")
def borrow_book():
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  cursor.execute('''
    SELECT * FROM books
    ''')
  books = cursor.fetchall()
  if books:
    print ("Title\t\tAuthor\t\tISBN\t\tAvailable")
    print ("-" * 50)
    for book in books:
      print (f" {book[0]:<8} | {book[1]:<10} | {book[2]:<10} | {book[3]:<10}")
    isbn = input("Enter the isbn of the book you wish to borrow: ")
    cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
    book = cursor.fetchone()
    if book:
      if book[3] > 0:
        cursor.execute("UPDATE books SET available = available - 1 WHERE isbn = ?", (isbn))
        connection.commit()
        print("Book borrowed successfully!")
      else:
        print("Sorry, the book is currently not available.")
    else:
      print("Unable to find book.")
  else:
    print ("No books are available in the Libary")
  connection.close()
def return_book():
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  cursor.execute('''
    SELECT * FROM books
    ''')
  books = cursor.fetchall()
  if books:
    print ("Title\t\tAuthor\t\tISBN\t\tAvailable")
    print ("-" * 50)
    for book in books:
      print (f" {book[0]:<8} | {book[1]:<10} | {book[2]:<10} | {book[3]:<10}")
    isbn = input("Enter the isbn of the book to return: ")
    cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
    book = cursor.fetchone()
    if book:
      if book[4] < book[3]:
        cursor.execute("UPDATE books SET available = available + 1 WHERE isbn = ?", (isbn,))
        connection.commit()
        print("Book has been returned successfully!")
      else:
        print("Sorry, the book is unable to be returned.")
    else:
      print("Book not found.")
  else:
    print ("No books are available in the Libary")
  connection.close()
def display_all_users():
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  cursor.execute('''
    SELECT * FROM users
    ''')
  users = cursor.fetchall()
  if users:
    print ("Username\tRole")
    print ("-" * 50)
    for user in users:
      print (f" {user[0]:<10} | {user[1]:<10}")
  else:
    print ("No users are available in the Libary")
  connection.close()
def update_user_role():
  username = input("Enter the Username of the user to update: ")
  role = input("Enter the new role of the user (admin/user): ")
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  cursor.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
  print("User role has been updated successfully!")
  connection.commit() 
def sort_books_by_isbn():
  connection = sqlite3.connect('Eldritch Library Management Database.db')
  cursor = connection.cursor()
  cursor.execute( 'SELECT * FROM books ORDER BY isbn')
  books = cursor.fetchall()
  if books:
    print ("Books sorted by isbn")
    print ("Title\t\tAuthor\t\tISBN\t\tAvailable")
    print ("-" * 50)
    for book in books:
      print (f" {book[0]:<8} | {book[1]:<10} | {book[2]:<10} | {book[3]:<10}")
  else:
    print ("No books are available in the Libary")
  connection.close()
def main():
  while True:
    print("Welcome to the Eldritch Library Management System!")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
      register()
    elif choice == "2":
      user = login()
      if user == 'guest':
        while True:
          print("Welcome, " + user + "!")
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
            break
          else:
            print("Invalid choice. Please try again.")
      elif user == 'admin' or user == 'user' :
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
            break
          else:
            print("Invalid choice. Please try again.")
    elif choice == "3":
      break
    else:
      print("Invalid choice. Please try again.")
if __name__ == "__main__":
  main()


