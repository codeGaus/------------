import sqlite3


database_name = "salon_database.db"
database_path = f"databases/{database_name}"


# CRUD операции для таблицы Customer
def create_customer(name, email, phone_number, birthdate, tg_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Customer (name, email, phone_number, birthdate, tg_id) VALUES (?, ?, ?, ?, ?)",
        (name, email, phone_number, birthdate, tg_id),
    )
    conn.commit()
    conn.close()


def read_customer(customer_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer WHERE customer_id = ?", (customer_id,))
    data = cursor.fetchone()
    conn.close()
    return data


def read_customer_by_tg(tg_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer WHERE tg_id = ?", (tg_id,))
    data = cursor.fetchone()
    conn.close()
    return data


def update_customer(customer_id, name, email, phone_number, birthdate):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Customer SET name = ?, email = ?, phone_number = ?, birthdate = ? WHERE customer_id = ?",
        (name, email, phone_number, birthdate, customer_id),
    )
    conn.commit()
    conn.close()


def delete_customer(customer_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Customer WHERE customer_id = ?", (customer_id,))
    conn.commit()
    conn.close()


# CRUD операции для таблицы Employee
def create_employee(name, email, phone_number, role_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Employee (name, email, phone_number, role_id) VALUES (?, ?, ?, ?)",
        (name, email, phone_number, role_id),
    )
    conn.commit()
    conn.close()


def read_employee(employee_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee WHERE employee_id = ?", (employee_id,))
    data = cursor.fetchone()
    conn.close()
    return data


def update_employee(employee_id, name, email, phone_number, role_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Employee SET name = ?, email = ?, phone_number = ?, role_id = ? WHERE employee_id = ?",
        (name, email, phone_number, role_id, employee_id),
    )
    conn.commit()
    conn.close()


def delete_employee(employee_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Employee WHERE employee_id = ?", (employee_id,))
    conn.commit()
    conn.close()


# CRUD операции для таблицы Role
def create_role(role_name):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Role (role_name) VALUES (?)", (role_name,))
    conn.commit()
    conn.close()


def read_role(role_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Role WHERE role_id = ?", (role_id,))
    return cursor.fetchone()
    conn.close()


def update_role(role_id, role_name):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Role SET role_name = ? WHERE role_id = ?", (role_name, role_id)
    )
    conn.commit()
    conn.close()


def delete_role(role_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Role WHERE role_id = ?", (role_id,))
    conn.commit()
    conn.close()


# CRUD операции для таблицы Service
def create_service(service_name):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Service (service_name) VALUES (?)", (service_name,))
    conn.commit()
    conn.close()


def read_service(service_id=None):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    if service_id is not None:
        cursor.execute("SELECT * FROM Service WHERE service_id = ?", (service_id,))
        data = cursor.fetchone()
    else:
        cursor.execute("SELECT * FROM Service")
        data = cursor.fetchall()
    conn.close()
    return data


def update_service(service_id, service_name):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Role Service service_name = ? WHERE service_id = ?", (service_name, service_id)
    )
    conn.commit()
    conn.close()


def delete_service(service_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Service WHERE service_id = ?", (service_id,))
    conn.commit()
    conn.close()


# CRUD операции для таблицы Promotions
def create_promotion(promotion_name):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Promotion (promotion_name) VALUES (?)", (promotion_name,))
    conn.commit()
    conn.close()


def read_promotion(promotion_id=None):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    if promotion_id is not None:
        cursor.execute("SELECT * FROM Promotion WHERE promotion_id = ?", (promotion_id,))
        data = cursor.fetchone()
    else:
        cursor.execute("SELECT * FROM Promotion")
        data = cursor.fetchall()
    conn.close()
    return data


def update_promotion(promotion_id, promotion_name):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Role Promotion promotion_name = ? WHERE promotion_id = ?", (promotion_name, promotion_id)
    )
    conn.commit()
    conn.close()


def delete_promotion(promotion_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Promotion WHERE promotion_id = ?", (promotion_id,))
    conn.commit()
    conn.close()


# CRUD операции для таблицы Appointment
def read_appointment_by_customer_id(customer_id=None):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    if customer_id is not None:
        cursor.execute("SELECT * FROM Appointment WHERE customer_id = ?", (customer_id,))
        data = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM Appointment")
        data = cursor.fetchall()
    conn.close()
    return data


if __name__ == '__main__':
    print(read_service())
