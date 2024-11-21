import psycopg2
from datetime import datetime

"""
    Database handler
"""
class DatabaseManager:
    def __init__(self):
        self.connect_to_database()

    """
        Database connection
    """
    def connect_to_database(self):
        DB_HOST = "34.123.56.222"
        DB_PORT = "5432"
        DB_NAME = "metrics_data"
        DB_USER = "postgres"
        DB_PASSWORD = "keren123"

        try:
            self.conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            self.cursor = self.conn.cursor()
            print("Connected to PostgreSQL database.")
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            exit(1)

    def save_energy_data(self, data):
        reading_time_dt = datetime.strptime(data["reading_time"], "%Y-%m-%d %H:%M:%S") if data["reading_time"] else None

        self.cursor.execute("""
            INSERT INTO energy_data (reading_time, position, meter_type, meter_serial_number, active_energy_import, active_energy_export, reactive_energy_import, 
                                    reactive_energy_export, apparent_energy_import, apparent_energy_export)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (reading_time_dt, data["position"], data["meter_type"], data["meter_serial_number"], 
            data["active_energy_import"], data["active_energy_export"], data["reactive_energy_import"], 
            data["reactive_energy_export"], data["apparent_energy_import"], data["apparent_energy_export"]))

        self.conn.commit()
        print("Data saved to PostgreSQL database.")

    """
        Execute querry
    """
    def execute_query(self, query, params):
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        return result
    
    """
        Get All Anomaly
    """
    def get_anomaly(self):
        query = """
                SELECT 
                    energy_data.id, 
                    energy_data.position, 
                    energy_data.reading_time 
                FROM 
                    energy_data 
                INNER JOIN 
                    anomaly_data 
                ON 
                    energy_data.id = anomaly_data.energy_data_id
                """
        
        result = self.execute_query(query, None)
        return result

    """
        Get Anomaly by ID
    """
    def get_anomaly_by_id(self, param):
        query = """
                SELECT 
                    energy_data.reading_time,
                    energy_data.position,
                    energy_data.meter_type,
                    energy_data.meter_serial_number,
                    energy_data.active_energy_import,
                    energy_data.active_energy_export,
                    energy_data.reactive_energy_import,
                    energy_data.reactive_energy_export,
                    energy_data.apparent_energy_import,
                    energy_data.apparent_energy_export,
                    anomaly_data.anomaly_type
                FROM 
                    energy_data 
                INNER JOIN 
                    anomaly_data 
                ON 
                    energy_data.id = anomaly_data.energy_data_id
                WHERE 
                    energy_data.id = %s
                """
        result = self.execute_query(query, [param])  
        return result[0] if result else None


    """
        Get data
    """
    def get_data(self, location, startdate=None, enddate=None):
        query = "SELECT * FROM energy_data WHERE position = %s"
        params = [location]

        if startdate:
            query += " AND reading_time >= %s"
            params.append(startdate)
        
        if enddate:
            query += " AND reading_time <= %s"
            params.append(enddate)
        
        query += " ORDER BY reading_time DESC"

        result = self.execute_query(query, params)
        return result