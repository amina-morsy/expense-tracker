import sqlite3
import argparse




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
                      
   connection.commit()  # saves the code on github
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
    
                       

def list_expenses():
    connection=sqlite3.connect("expenses.db")
    cursor=connection.execute("""
                              SELECT id, amount, category, date, details FROM expenses ORDER BY date DESC
                              
                              """)  #select says give me those columns from expenses table and sort them by newest first DESC= descending, the results come back as cursor(pointer)
    rows= cursor.fetchall()  #fetchall collects every result into a list, each item in the list is one expense, stored as a tuple
    connection.close() # no commit this time because commit saves changes and reading doesn't cause changes
    if not rows:
        print("No expenses yet.")
        return 
    for row in rows:
        ids, amount, category, date, details=row
        euros=amount/100
        print(f'{ids}, {date}, {category}, {euros:.2f}, {details}')
        
        
def summary():
    connection=sqlite3.connect("expenses.db")
    cursor=connection.execute(
        """SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC
        """  #group by category puts all expenses with the same category into one group
        # sum(amount) adds up the amounts within each group
        # order by sum(amount) dessc puts biggest spending first
        )
    by_category=cursor.fetchall()
    cursor_month= connection.execute("""SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM expenses GROUP BY month ORDER BY month DESC""")
    by_month=cursor_month.fetchall()
    connection.close()
    if not by_category:
        print("No expenses yet")
        return
    
    print("By category:")
    total=0
    for row in by_category:
        category, cents=row
        total+=cents
        print(f" {category}  {cents/100:.2f}")
    print("By month: ")
    for row in by_month:
        months, cents=row
        print(f" {months}  {cents/100:.2f}")

    print(f"Total: {total/100:.2f}")
    
def delete_expense(expense_id):
    connection=sqlite3.connect("expenses.db")
    cursor=connection.execute("""DELETE FROM expenses WHERE id=?""", (expense_id,) ) #the WHERE id =? limits the delete to one row, without it everything will be deleted. the comma after the expense_id is to make it a one item tuple because the values must be a tuple
    deleted=cursor.rowcount #rowcount tells you how many rows the command affected
    connection.commit()
    connection.close()
    if deleted==0:
        print(f"No expense found with id {expense_id}")
    else:
        print(f"Expense {expense_id} deleted.")
        
    
    
    
    
          
        
    
    
def main():
    init_db() #calling this first guarantees the table exists before any command runs
    parser=argparse.ArgumentParser(description="Simple expense tracker") #parse readas what the user typed, the description shows up in the automatic help message.
    subparsers= parser.add_subparsers(dest="command")  #add and list are subcommands, dest="command" means store which subcommand the user typed in a variable called command so you can check it later.
    add_parser=subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument('amount', type=float)
    add_parser.add_argument("category")
    add_parser.add_argument("date")
    add_parser.add_argument("details")
    subparsers.add_parser("list", help="Show all expenses")
    subparsers.add_parser("summary", help="Show spending totals")
    delete_parser=subparsers.add_parser("delete", help="Delete an expense by ID")
    delete_parser.add_argument("id", type=int)
    args=parser.parse_args() 

    if args.command=="add": 
        add_expense(args.amount, args.category, args.date, args.details)
        print("Expense added")
    elif args.command=="list":
        list_expenses()
    elif args.command=="summary":
        summary()
    elif args.command =="delete":
        delete_expense(args.id)
    else:
        parser.print_help()  #so when user types just python tracker.py with no command, they get instructions instead of nothing
   
    
        
if __name__=="__main__":
    main()
    
        
    
    