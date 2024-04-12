import sqlite3

class Database:
    def __init__(self):
        self.con=sqlite3.connect("todo.db")
        self.cursor=self.con.cursor()

        
    def get_tasks(self):
        # query="SELECT * FROM tasks ORDER BY priority"
        query="SELECT * FROM tasks"
        result=self.cursor.execute(query)
        tasks=result.fetchall()
        return tasks
    
    def add_new_task(self, new_title, new_description, new_time):
        try:
            query=f"INSERT INTO tasks(title, description, time) VALUES ('{new_title}', '{new_description}', '{new_time}')"
            self.cursor.execute(query)
            self.con.commit()
            return True
        except:
            return False
        
    def remove_tasks(self, id):
        query=f"DELETE FROM tasks WHERE id={id}"
        self.cursor.execute(query)
        self.con.commit()

    def task_done(self, id):
        query=f"UPDATE tasks SET status=1 WHERE id={id}"
        self.cursor.execute(query)
        self.con.commit()
    

