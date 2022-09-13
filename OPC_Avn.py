from opcua import Client, ua
import pyodbc
import sqlite3
import threading

client = Client("opc.tcp://CUNG:49320")
print(pyodbc.drivers())

count = 0

info = ["KWh", "Energy", "Voltage_1", "Voltage_2", "Voltage_3", "Voltage_N", "Current_1", "Current_2", "Current_3", "Current_AVG", "Power_1", "Power_2", "Power_3", "Power_Factor_1", "Power_Factor_2", "Power_Factor_3", "Power_Factor_Total"]

def connect_sqlite():
    try:
        conn_sqlite = sqlite3.connect('test.db')
        print("Opened database successfully")
        conn_sqlite.execute('''CREATE TABLE IF NOT EXISTS tblArchivedMinute
                (ID INT PRIMARY KEY     NOT NULL,
                NodeName       CHAR(50)    NOT NULL,
                KWh            Float,
                Energy         Float,
                Voltage_1      Float,
                Voltage_2      Float,
                Voltage_3      Float,
                Voltage_N      Float,
                Current_1      Float,
                Current_2      Float,
                Current_3      Float,
                Current_AVG    Float,
                Power_1        Float,
                Power_2        Float,
                Power_3        Float,
                Power_Factor_1 Float,
                Power_Factor_2 Float,
                Power_Factor_3 Float,
                Power_Factor_Total Float);''')
        print("Table created successfully")

        conn_sqlite.commit()
        print("Records created successfully")

        return conn_sqlite

    except Exception as e:
        print(f"Connect database failed: {e}")
        return

def connect_sqlserver():
    conn_sqlserver = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};\
        SERVER=CUNG\SQLEXPRESS;\
        Database=Avani.Andon.Energy;\
        UID=sa;\
        PWD=admin@123"
    )
    try:
        client.connect()
        return conn_sqlserver
    except Exception as e:
        print(f"Error: {e}")
        return

def define_node(conn_sqlite, conn_sqlserver):
    cursor = conn_sqlserver.cursor()
    query = cursor.execute("select COUNT(*) from tblNode")
    count = query.fetchone()[0]
    for row in cursor.execute("select * from tblNode"):
        # print(f"{row.Id}  - - - {row.Name}")
        query = f"INSERT OR REPLACE INTO tblArchivedMinute (ID,NodeName) VALUES ({row.Id}, '{row.Name}')"
        # print(query)
        conn_sqlite.execute(query)
        conn_sqlite.commit()

def update_node_value_sqlite(conn_sqlite, conn_sqlserver):
    cursor = conn_sqlserver.cursor()
    for record in cursor.execute("select * from tblArchivedMinute where id > 982470"):
        print(f"{record.Id}  - - - {record.NodeName}")
        sql = f"UPDATE tblArchivedMinute SET \
            KWh = {record.ActiveEnergy}, \
            Energy = {record.ActiveEnergy}, \
            Voltage_1 = {record.Volt_1N_AVG}, \
            Voltage_2 = {record.Volt_2N_AVG}, \
            Voltage_3 = {record.Volt_3N_AVG}, \
            Voltage_N = {record.Volt_AVG_LN_AVG}, \
            Current_1 = {record.Current_1_AVG}, \
            Current_2 = {record.Current_2_AVG}, \
            Current_3 = {record.Current_3_AVG}, \
            Current_AVG = {record.Current_N_AVG}, \
            Power_1 = {record.ActivePower_1_AVG}, \
            Power_2 = {record.ActivePower_2_AVG}, \
            Power_3 = {record.ActivePower_3_AVG}, \
            Power_Factor_1 = {record.PowerFactor_1_AVG}, \
            Power_Factor_2 = {record.PowerFactor_2_AVG}, \
            Power_Factor_3 = {record.PowerFactor_3_AVG}, \
            Power_Factor_Total = {record.PowerFactor_Total_AVG} \
            WHERE ID = {record.NodeId}"
        # print(sql)
        conn_sqlite.execute(sql)
        conn_sqlite.commit()

def update_node_value_opc(conn_sqlite):
    sql = "SELECT * FROM tblArchivedMinute"
    cur = conn_sqlite.cursor()
    cur.execute(sql)
    records = cur.fetchall()
    for record in records:
        # print(record[1])
        for i in info:
            try:
                var = client.get_node(f"ns=2;s=Channel2.Device2.{record[1]}-{i}")
                # print("Value")
                # print(record[info.index(f"{i}") + 2])
                print(f"Channel2.Device2.{record[1]}-{i}")
                value = record[info.index(f"{i}") + 2]
                if value is not None:
                    data = round(value, 3)
                    print(data)
                    dv = ua.DataValue(ua.Variant(data, ua.VariantType.Float))
                    var.set_value(dv)
            except Exception as e:
                print(f"Error: {e}")
                pass

def main():
    conn1 = connect_sqlite()
    conn2 = connect_sqlserver()
    update_node_value_sqlite(conn1, conn2)
    update_node_value_opc(conn1)
    conn1.close()
    conn2.close()
    client.disconnect()

if __name__ == "__main__":
    main()