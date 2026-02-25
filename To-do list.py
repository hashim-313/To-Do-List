import hashlib
import sqlite3 as sqt

conn = sqt.connect('task5.db')
cursor = conn.cursor()
'''User Table 👤👤'''
cursor.execute('''
               create table if not exists Users
               (username TEXT primary key,
                password TEXT NOT NULL);
               ''')
'''Task Table'''
cursor.execute('''
               create table if not exists Task_manager
               (task_id INTEGER primary key AUTOINCREMENT,
                username TEXT REFERENCES Users(username),
                task varchar,
                status TEXT DEFAULT 'Pending ⏳',
                due_date TEXT);
               ''')

conn.commit()
#print(pd.read_sql('Select* From Task_manager;', conn))
''' Password hashing '''
# hashing iu used to Convert a password into a fixed-length coded string 
# mypassword123 to ef92b778ba.. for swcurity purpose. 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
'''
sha-256 convert password into string such as 2cf24dba5fb0a..
hexdigest() provide a clean string b',\xf2M\xba_\xb0\xa3... to  2cf24dba5fb0a30e26e83b2ac5b9e29e...
'''
''' User registration'''
def register():
    username = input("Username: ")
    password = input("Password: ")
    hashed = hash_password(password)
    try:
        cursor.execute("insert into Users values (?,?)", (username, hashed))
        conn.commit()
        print(f'User {username} registered successfully ✅✅')
    except sqt.IntegrityError:
        print(f'User {username} Already Exists❗❗')
''' User login '''
def login():
    username = input("Username: ")
    password = input("Password: ")
    print("-------------------------------------")
    hashed = hash_password(password)
    cursor.execute("select* from Users where username = ? AND password = ?", (username, hashed))
    if cursor.fetchone(): # fetchone is used to provide data which matches.
        print(f'Login Sucessful ‼ \nWelcome {username} 🎉🎉')
        print('\n')
        return username
    else:
        print("Invalid username or password ❌❌")
        return None
''' Add Task '''
def add_task(current_user):
    task = input("Enter you task: ")
    due_date = input("Enter Due Date (YYYY-MM-DD): ")
    qry = "INSERT INTO Task_manager (username, task, due_date) VALUES (?, ?, ?)"
    cursor.execute(qry,(current_user, task, due_date))
    conn.commit()
    print('\n')
    print(f'task added: {task}, due_date on: {due_date}')
    print('\n')
    
#add_task('Physics Chapter 8', '28/3/2026')

def view_task(current_user):
    cursor.execute("Select task_id, task, status, due_date from Task_manager where username = ? order by due_date", (current_user,))
    tasks = cursor.fetchall() # fetchall fuction returns a list of rows from your database.
    print("Your Tasks \n")
    for t in tasks:
        print(f'{t[0]} {t[1]} - {t[2]} --> {t[3]}')
        print('\n')
    conn.commit()

def update_task_status(current_user):
    view_task(current_user)
    task_id = input("Enter task id to be marked as Complete ✅: ").strip()
    cursor.execute("UPDATE Task_manager SET status = 'Completed ✅' WHERE task_id = ? AND username =?", (task_id, current_user))
    conn.commit()
    print('\n')
    print(f'Task {task_id} marked as complete ✅✅.') 
    print('\n')
def delete_task(current_user):
    view_task(current_user)
    task_id = input("Enter task id to be Deleted: ").strip()
    cursor.execute("DELETE FROM Task_manager WHERE task_id = ? AND username= ?",(task_id, current_user))
    conn.commit()
    print('\n')
    print(f'Task {task_id} Deleted.')
    print('\n')
def main_menu():
    while True:
        print('1. Register for New Users')
        print('2. Login if already have an account')
        print('3. Exit')
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                while True:
                    print('1. Add Task to your To-Do list')
                    print('2. View your tasks')
                    print('3. Update your To-Do list Status')
                    print('4. Delete task from your To-Do list')
                    print('5. Logout')
                    task_choice = input("Enter Your task chioce: ").strip()
                    if task_choice == "1":
                        add_task(user)
                    elif task_choice == "2":
                        view_task(user)
                    elif task_choice == "3":
                        update_task_status(user)
                    elif task_choice == "4":
                        delete_task(user)
                    elif task_choice == "5":
                        print("user Logged Out")
                        break
                    else:
                        print("You choosed invalid option ❌\n")
        elif choice == "3":
               print('Good Bye 👋👋')
               break
        else:
              print("Invalid Option ❌ \n")
                    
m = main_menu()
            
           
           
         
                  
                
        
         
