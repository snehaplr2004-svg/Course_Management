import mysql.connector
class Enrollment:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user="root",password="root",host="localhost",
                database="course_enrollment",use_pure=True)
            print("Connected Successfully")
        except :
            print("Failed Connection")

    def enroll(self, name, course, duration, date, fee, status):
        try:
            cursor = self.connection.cursor()

            if duration <= 0 or fee < 0:
                print("Invalid duration or fee")
            else:
                query = "insert into enrollments(student_name,course_name,duration_months,enrollment_date,fee,status) values(%s,%s,%s,%s,%s,%s)"

                data = (name, course, duration, date, fee, status)

                cursor.execute(query, data)
                self.connection.commit()

                print("Enrolled Successfully")

        except:
            print("Failed to enroll")

    def read(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM enrollments order by fee desc"
            cursor.execute(query)
            records = cursor.fetchall()
            if records:
                for row in records:
                    print(row)
            else:
                print("No records found")
        except:
            print("Failed to read:")

    def retrieve(self, choice, value):
        try:
              cursor = self.connection.cursor()

              if choice == 1:
                   query = "select * from enrollments where enrollment_id=%s"
                   data = (value,)
              else:
                   query = "select * from enrollments where student_name like %s or course_name like %s"
                   data = (value, value)

              cursor.execute(query, data)
              records = cursor.fetchall()

              if records:
                   for row in records:
                       print(row)
              else:
                   print("No records found")

        except:
              print("Failed to retrieve")

    def update(self, id, status, fee):
        try:
            cursor = self.connection.cursor()
            if fee == "":
                query = """
                UPDATE enrollments
                SET status=%s
                WHERE enrollment_id=%s
                """
                data = (status, id)
            else:
                if float(fee) < 0:
                    print("Fee cannot be negative")
                    return
                query = """
                UPDATE enrollments
                SET status=%s, fee=%s
                WHERE enrollment_id=%s
                """
                data = (status, float(fee), id)

            cursor.execute(query, data)
            self.connection.commit()
            if cursor.rowcount > 0:
                print("Updated Successfully")
            else:
                print("No record found")

        except:
            print("Failed to update")

    def delete(self, id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM enrollments WHERE enrollment_id=%s"
            data=(id,)
            cursor.execute(query,data)
            self.connection.commit()
            if cursor.rowcount > 0:
                print("Deleted Successfully")
            else:
                print("No record found")
        except:
            print("Failed to delete")
    def summary(self):
        try:
            cursor = self.connection.cursor()

            query = "select count(*), sum(fee), avg(fee) from enrollments"
            cursor.execute(query)
            record = cursor.fetchone()

            print("Total Enrollments:", record[0])
            print("Total Fees:", record[1])
            print("Average Fee:", record[2])

            query = "select status, count(*) from enrollments group by status"
            cursor.execute(query)
            records = cursor.fetchall()

            print("Enrollment Status:")
            for row in records:
                print(row[0], ":", row[1])

        except:
            print("Failed to generate summary")

p = Enrollment()
while True:
        print("1. Enroll Student")
        print("2. View All Enrollments")
        print("3. Search Enrollment")
        print("4. Update Enrollment Status")
        print("5. Delete Enrollment")
        print("6. Enrollment Summary")
        print("7. Exit")

        ch = int(input("Enter your choice: "))

        if ch == 1:
            s = input("Enter student name: ")
            c = input("Enter course name: ")
            d = int(input("Enter duration in months: "))
            en = input("Enter enrollment date: ")
            fee = int(input("Enter fee: "))
            status = input("Enter status (Active/Completed/Cancelled): ")
            p.enroll(s, c, d, en, fee, status)
        elif ch == 2:
            p.read()
        elif ch == 3:
            print("1. Search by Enrollment ID")
            print("2. Search by Student/Course Name")
            choice = int(input("Enter choice: "))
            if choice == 1:
                i = int(input("Enter enrollment ID: "))
                p.retrieve(1, i)
            elif choice == 2:
                name = input("Enter student name or course name: ")
                p.retrieve(2, name)
            else:
                print("Invalid choice")
        elif ch == 4:
            i = int(input("Enter enrollment ID: "))
            status = input("Enter new status: ")

            fee = input("Enter new fee (Press Enter to skip): ")

            p.update(i, status, fee)

        elif ch == 5:
            i = int(input("Enter enrollment ID: "))
            p.delete(i)
        elif ch == 6:
            p.summary()

        elif ch == 7:
            exit()