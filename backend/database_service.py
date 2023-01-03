import time

import mysql.connector


class DatabaseService:
    def __init__(self, database_configuration):
        for _ in range(10):
            try:
                self.db = mysql.connector.connect(host=database_configuration['host'],
                                                  user=database_configuration['user'],
                                                  password=database_configuration['password'],
                                                  database=database_configuration['database'])
                print("Connected to database")
                break
            except Exception as ex:
                print(f"Exception ocurred while connecting to database: {ex}")
                time.sleep(5)

    def __del__(self):
        self.db.close()

    def create_database(self):
        cursor = self.db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Measurements
        (ID INTEGER PRIMARY KEY AUTO_INCREMENT,
        MeasurementTime DATETIME,
        Language VARCHAR(10) NOT NULL DEFAULT "",
        FibonacciCount INTEGER NOT NULL DEFAULT 0,
        TestDuration VARCHAR(25) NOT NULL DEFAULT ""
        );''')

        cursor.close()

    def delete_measurement(self, measurement_id):
        cursor = self.db.cursor(dictionary=True)
        measurement_to_delete_query = '''DELETE FROM Measurements WHERE ID = %s'''
        cursor.execute(measurement_to_delete_query, (measurement_id,))
        self.db.commit()
        cursor.close()

    def add_measurement(self, data):
        cursor = self.db.cursor(dictionary=True)
        query = '''INSERT INTO Measurements "(MeasurementTime, Language, FibonacciCount, TestDuration)"
        VALUES (%s, %s, %s, %s)'''

        data_to_add = (data['measurement_time'], data['language'], data['fibonacci_count'], data['test_duration'])
        cursor.execute(query, data_to_add)
        self.db.commit()
        cursor.close()

    def get_measurements(self):
        cursor = self.db.cursor(dictionary=True)
        query = '''SELECT * FROM Measurements'''
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_measurement(self, measurement_id):
        cursor = self.db.cursor(dictionary=True)
        query = '''SELECT * FROM Measurements WHERE ID = %s'''
        cursor.execute(query, (measurement_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
