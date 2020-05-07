import sqlite3
import time


class Companies:

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
                self.__add(company)
            elif choice == 2:
                self.__show_records(sqlite3.connect('companies.db'))
            elif choice == 3:
                month = float(input("How many months ago?\n"))
                db = sqlite3.connect('companies.db')
                query = """Select * from Companies where epoch_time < {}
                ORDER BY epoch_time DESC""".format(
                    int(time.time() - 2_592_000 * month))
                records = db.execute(query)
                for record in records:
                    print(record)
                db.close()
            elif choice == 9:
                break
            else:
                print('Enter correct response')

    @staticmethod
    def __show_records(db, specific=None):
        if specific is None:
            specific = input("Specific?\n")
        if specific.upper() == 'NO':
            for company in db.execute('''select * from Companies
            order by epoch_time DESC'''):
                print(company)
        elif specific.isdigit():
            print('\nShowing last {} companies\n'.format(specific))
            for company in db.execute('''select * from Companies
            order by epoch_time DESC LIMIT ?''', (int(specific),)):
                print(company)
        else:
            query = """SELECT * FROM Companies
            WHERE CompanyID LIKE '%{}%'""".format(specific)
            specific_companies = db.execute(query)
            for company in specific_companies:
                print(company)

    def __add(self, company):
        db = sqlite3.connect('companies.db')
        self.__show_records(db, company)
        company_entered = input("Enter existing company or new company\n")
        notes = input("Enter notes\n")
        try:
            db.execute('pragma foreign_keys = on')
            db.execute("""INSERT into Companies values
        (?, datetime('now', 'localtime'), ?, ?)""",
                       (company_entered, int(time.time()), notes))
        except sqlite3.OperationalError:
            print("SQL error, company not added")
        except sqlite3.IntegrityError:
            only_notes = input("Edit only notes?\n")
            self.__update(company_entered, notes, only_notes, db)
        else:
            print("Insert successful")
        # self.__db.commit()
        db.close()

    @staticmethod
    def __update(company, new_notes, only_notes, db):
        if only_notes == 'n':
            db.execute("""UPDATE Companies set Last_Updated = datetime('now', 'localtime'),
            epoch_time = ?, Notes = ? where CompanyID = ?""",
                       (int(time.time()), company, new_notes))
        else:
            db.execute("""UPDATE Companies set
            Notes = ? where CompanyID = ?""", (new_notes, company))
        print("Update successful")


companies = Companies()
companies.start()
