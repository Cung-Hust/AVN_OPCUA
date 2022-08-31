import pyodbc

print(pyodbc.drivers())

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};\
    SERVER=CUNG\SQLEXPRESS;\
    Database=avSVAWF2;\
    UID=sa;\
    PWD=admin@123"
)

cursor = conn.cursor()

for row in cursor.execute("select * from tblNode"):
    print(row)
    print(row.Id)
    print(row.Name)
    
conn.close()