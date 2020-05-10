import sqlite3
import time


class Companies:

    def __init__(self):
        self.__db = sqlite3.connect('companies.db')

    def start(self):
        choice = 0
        while True:
            try:
                choice = int(input("""\n1.Add or Update\n2.Show Records\n"""
                                   """3.Which to apply\n4.Log rejection\n"""
                                   """5.Commit\n9.Quit\n"""))
            except ValueError:
                pass
            if choice == 1:
                company = input("Enter company " +
                                "('get out' to go back to menu)\n")
                if company == 'get out':
                    continue
                self.__add(company)
            elif choice == 2:
                self.__show_records()
            elif choice == 3:
                self.__show_which_to_apply()
            elif choice == 4:
                company_entered = input("Enter Company\n")
                self.__show_records(company_entered)
            elif choice == 5:
                self.__commit()
            elif choice == 9:
                break
            else:
                print('Enter correct response')

    def __show_which_to_apply(self):
        month = float(input("How many months ago?\n"))
        query = """Select * from Companies where epoch_time < {}
                ORDER BY epoch_time DESC""".format(
            int(time.time() - 2_592_000 * month))
        for record in self.__db.execute(query):
            print(record)

    def __show_records(self, specific=None):
        if specific is None:
            specific = input("Specific?\n")
        if specific.upper() == 'NO':
            for company in self.__db.execute('''select * from Companies
            order by epoch_time DESC'''):
                print(company)
        elif specific.isdigit():
            print('\nShowing last {} companies\n'.format(specific))
            for company in self.__db.execute('''select * from Companies
            order by epoch_time DESC LIMIT ?''', (int(specific),)):
                print(company)
        else:
            query = """SELECT * FROM Companies
            WHERE CompanyID LIKE '%{}%'""".format(specific)
            specific_companies = list(self.__db.execute(query))
            for company in specific_companies:
                print(company)
            return len(specific_companies)

    def __add(self, company):
        count = self.__show_records(company)
        if count != 0:
            company = input("Enter existing company or new company\n")
        notes = input("Enter notes\n")
        jobs_quantity = int(input("How many jobs?\n"))
        try:
            self.__db.execute('pragma foreign_keys = on')
            self.__db.execute("""INSERT into Companies values
        (?, datetime('now', 'localtime'), ?, ?, ?)""",
                              (company, int(time.time()),
                               notes, jobs_quantity))
        except sqlite3.OperationalError:
            print("SQL error, company not added")
        except sqlite3.IntegrityError:
            only_notes = input("Edit only notes?\n")
            self.__update(company, notes, only_notes)
        else:
            print("Insert successful")

    def __update(self, company, new_notes, only_notes):
        if only_notes == 'n':
            self.__db.execute("""UPDATE Companies set Last_Updated = datetime('now', 'localtime'),
            epoch_time = ?, Notes = ? where CompanyID = ?""",
                              (int(time.time()), company, new_notes))
        else:
            self.__db.execute("""UPDATE Companies set
            Notes = ? where CompanyID = ?""", (new_notes, company))
        print("Update successful")

    def __log_rejection(self, company):
        rejection_quantity = int(input("How many rejections?\n"))
        self.__db.execute("""UPDATE Companies set
        Jobs = Jobs - ? where CompanyID = ?""", (rejection_quantity, company))

    def __commit(self):
        self.__db.commit()

    def stop(self):
        self.__db.close()


companies = Companies()
companies.start()
companies.stop()
