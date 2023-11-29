import sqlite3, os
class DbManager:
    def __init__(self):
        self.db_name =os.path.join(os.path.dirname(__file__), '.', 'bot.db')
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.connection.commit()

    
    def create_table(self, table_name, columns):
        columns_str = ', '.join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});"
        self.execute(create_table_query)

    def insert_into_table(self, table_name, values):
        placeholders = ', '.join(['?'] * len(values))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        self.execute(insert_query, values)
        
    def update(self, table_name, set_values, conditions=None):
            set_str = ", ".join([f"{column} = ?" for column in set_values.keys()])
            condition_str = ""
            if conditions:
                condition_str = " WHERE " + " AND ".join(conditions)
            update_query = f"UPDATE {table_name} SET {set_str}{condition_str};"
            values = list(set_values.values())
            if conditions:
                values += conditions
            self.execute(update_query, values)

          
    def increment(self,tableName, condition=None,**colWithValue):
        condition_str = " WHERE " + " AND ".join(condition)
        if colWithValue['column']=='transactions':
            self.cursor.execute(("UPDATE "+tableName+" SET "+ colWithValue['column']+"="+colWithValue['column']+" || "+str(colWithValue['newValue'])+condition_str+";"))
            return
        self.cursor.execute(("UPDATE "+tableName+" SET "+ colWithValue['column']+"="+colWithValue['column']+"+"+str(colWithValue['newValue'])+condition_str+";"))
        self.connection.commit()
                 
    def select_from_table(self, table_name, columns=None, conditions=None):
        column_str = "*"
        if columns:
            column_str = ", ".join(columns)
        condition_str = ""
        if conditions:
            condition_str = " WHERE " + " AND ".join(conditions)
        select_query = f"SELECT {column_str} FROM {table_name}{condition_str};"
        return self.fetch_all(select_query)
    
    def delete_table(self, table_name):
        delete_query = f"DROP TABLE IF EXISTS {table_name};"
        self.execute(delete_query)

    def close(self):
        self.connection.close()


    def fetch_all(self, query, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return self.cursor.fetchone()
    def renitialise(self, table_name):
        delete_query = f"DELETE FROM {table_name};"
        self.execute(delete_query)


   
    def addColumn(self,tableName, columnName, columnType):
        self.cursor.execute(("ALTER TABLE "+tableName+" ADD COLUMN "+columnName+" "+columnType+";"))
        self.connection.commit()
##helpers
    def turnToList(self,pairs):
        result=[]
        for pair in pairs:
            result.append(pair[0])
        return result