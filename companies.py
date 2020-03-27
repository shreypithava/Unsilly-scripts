import sqlite3
import time


def add(comp, db1):
    try:
        db1.execute('pragma foreign_keys = on')
        db1.execute("INSERT into Companies values (?, datetime('now', 'localtime'), ?)",
                    (comp, int(time.time())))
    except sqlite3.OperationalError:
        print("SQL error, company not added")
    except sqlite3.IntegrityError:
        update(comp, db1)
    else:
        print("Insert successful")


def update(comp, db2):
    db2.execute("UPDATE Companies set Last_Updated = datetime('now', 'localtime'), epoch_time = ? where CompanyID = ?",
                (int(time.time()), comp))
    print("Update successful")


def show_records():
    specific = input("Specific?")
    db3 = sqlite3.connect('companies.db')
    if specific.upper() == 'NO':
        for com in db3.execute('select * from Companies order by CompanyID'):
            print(com)
    else:
        for com in db3.execute('select * from Companies where CompanyID = ?', specific):
            print(com)
    db3.close()


companies = []

with open("companies.txt", 'r') as f:
    for line in f.readlines():
        companies.append(line.strip().upper())

while True:
    choice = int(input("1.Add or Update\n2.Show Records\n9.Quit\n"))
    if choice == 1:
        company = input("Enter company\n")
        db = sqlite3.connect('companies.db')
        add(company, db)
        db.commit()
        db.close()
    elif choice == 2:
        show_records()
    else:
        break
