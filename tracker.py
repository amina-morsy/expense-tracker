import sqlite3

print("Expense tracker")




def init_db():
   connection=sqlite3.connect("expenses.db")  # opens a database file or creaetes it if it doesn't exist
   connection.execute("""       
                      CREATE TABLE IF NOT EXISTS expenses (
                          id INTEGER PRIMARY KEY,
                          amount INTEGER NOT NULL,
                          category TEXT NOT NULL,
                          date TEXT NOT NULL,
                          details TEXT NOT NULL
                          )
                      """)  #exectue sends SQL to the database
                      
   connection.commit()  # saves the code on githun
   connection.close() #closes the file properly
   
   
def add_expense(amount, category, date, details):
    amount_cents=round(amount*100) #since we chose to store money as cents, round avoids tiny errors
    connection=sqlite3.connect("expenses.db")
    connection.execute("""
                       INSERT INTO expenses(amount, category, date, details)
                       VALUES(?, ?, ?, ?)
                       """, (amount_cents, category, date, details))  #insert into adds a new row, each ? is a placeholder that SQL fills safely, we never put user input directly into SQL since thats how injection attacks happen, SQL creates the id automatically
                       
    connection.commit()
    connection.close()
    
                       
    
   
                      
   
init_db()

print("Database ready.")
              
    
    