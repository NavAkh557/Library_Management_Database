import sqlite3
import hashlib
import getpass

connection = sqlite3.connect("library management database.db")
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, role TEXT)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS books (title Text, author TEXT, isbn INT, stock INT)")
def register ():
  username = input("Enter your username: ")
  password = getpass.getpass("Enter your password: ")
  role = input("Enter your role (admin/user): ")
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
def add_book():
  title = input("Enter the title of the book: ")
  author = input("Enter the author of the book: ")
  isbn = input("Enter the ISBN of the book: ")
  stock = input("Enter the number of copies of the book: ")
  cursor.execute("INSERT INTO books VALUES (?,?,?,?)", (title, author, isbn, stock))
  connection.commit()
  print("Book added successfully!")
def remove_book():
  isbn = input("Enter the ISBN of the book to remove: ")
  cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
  connection.commit()
  print("Book removed successfully!")
def display_books():
  cursor.execute("SELECT * FROM books")
  books = cursor.fetchall()
  if books:
    for book in books:
      print(f"Title: {book[0]}, Author: {book[1]}, ISBN: {book[2]}, Stock: {book[3]}")
    