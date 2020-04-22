import sqlite3
import time


class Companies:
    def __init__(self):
        self.__db = None

    def start(self):
        choice = 0
        while True:
            try:
                choice = int(input("""\n1.Add or Update\n2.Show Records\n"""
                                   """3.Which to apply\n9.Quit\n"""))
            except ValueError:
                pass
            if choice == 1:
                company = input("Enter company " +
                                "('get out' to go back to menu)\n")
                if company == 'get out':
                    continue
                self.__db = sqlite3.connect('companies.db')
                self.__add(company)
                # self.__db.commit()
                self.__db.close()
            elif choice == 2:
                self.__show_records()
            elif choice == 3:
                month = float(input("How many months ago?\n"))
                self.__db = sqlite3.connect('companies.db')
                query = """Select * from Companies where epoch_time < {}
                ORDER BY epoch_time DESC""".format(
                    int(time.time() - 2_592_000 * month))
                records = self.__db.execute(query)
                for record in records:
                    print(record)
                self.__db.close()
            elif choice == 9:
                break
            else:
                print('Enter correct response')

    def __show_records(self):
        specific = input("Specific?\n")
        self.__db = sqlite3.connect('companies.db')
        if specific.upper() == 'NO':
            for com in self.__db.execute('''select * from Companies
            order by epoch_time DESC'''):
                print(com)
        else:
            query = """SELECT * FROM Companies
            WHERE CompanyID LIKE '%{}%'""".format(specific)
            specific_companies = self.__db.execute(query)
            for company in specific_companies:
                print(company)
        self.__db.close()

    def __add(self, company):
        notes = input("Enter notes\n")
        try:
            self.__db.execute('pragma foreign_keys = on')
            self.__db.execute("""INSERT into Companies values
        (?, datetime('now', 'localtime'), ?, ?)""",
                              (company, int(time.time()), notes))
        except sqlite3.OperationalError:
            print("SQL error, company not added")
        except sqlite3.IntegrityError:
            self.__update(company, notes)
        else:
            print("Insert successful")

    def __update(self, company, new_notes):
        self.__db.execute("""UPDATE Companies set Last_Updated = datetime('now', 'localtime'),
        epoch_time = ?, Notes = ? where CompanyID = ?""",
                          (int(time.time()), company, new_notes))
        print("Update successful")


companies = Companies()
companies.start()
