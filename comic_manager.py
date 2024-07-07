import sqlite3

class Manager:
    def __init__(self, db_name='comicdb.db'):
        self.db_name = db_name
        self.username = None
        self.user_id = None
        self.clearance_level = None

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_comicdb(self):
        conn = self.connect()
        cursor = conn.cursor()

        # Create volume table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS volume (
                volume_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Create publisher table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS publisher (
                publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Create series table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS series (
                series_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                volume_id INTEGER NOT NULL,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (volume_id) REFERENCES volume (volume_id),
                FOREIGN KEY (publisher_id) REFERENCES publisher (publisher_id)
            )
        ''')

        # Create comic table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comic (
                comic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_url TEXT,
                description TEXT,
                series_id INTEGER NOT NULL,
                current_price REAL,
                issue_num INTEGER NOT NULL,
                cover_price REAL NOT NULL,
                FOREIGN KEY (series_id) REFERENCES series (series_id)
            )
        ''')

        # Create user table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                clearance_level INTEGER NOT NULL
            )
        ''')

        # Create collection table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection (
                collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                comic_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user (user_id),
                FOREIGN KEY (comic_id) REFERENCES comic (comic_id)
            )
        ''')

        conn.commit()
        conn.close()
    
    def reset_data(self):
        conn = self.connect()
        cursor = conn.cursor()

        # Delete all rows from each table
        cursor.execute('DELETE FROM volume')
        cursor.execute('DELETE FROM publisher')
        cursor.execute('DELETE FROM series')
        cursor.execute('DELETE FROM comic')
        cursor.execute('DELETE FROM user WHERE username != ?', ('admin',))
        cursor.execute('DELETE FROM collection')

        conn.commit()
        conn.close()

    def add_user(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO user (username, password, clearance_level) VALUES (?, ?, 1)
        ''', (username, password))

        conn.commit()
        conn.close()

    def add_admin(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO user (username, password, clearance_level) VALUES (?, ?, 5)
        ''', (username, password))

        conn.commit()
        conn.close()
    
    def add_series(self, name, volume_id, publisher_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO series (name, volume_id, publisher_id) VALUES (?, ?, ?)
        ''', (name, volume_id, publisher_id))

        conn.commit()
        conn.close()

    def show_all_series(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM series
        ''')
        series = cursor.fetchall()
        conn.close()
        return series

    def add_publisher(self, name):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO publisher (name) VALUES (?)
        ''', (name,))

        conn.commit()
        conn.close()
    
    def show_all_publishers(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM publisher
        ''')

        publishers = cursor.fetchall()

        conn.close()
        return publishers

    def add_volume(self, num):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO volume (name) VALUES (?)
        ''', (f'Vol. {num}',))

        conn.commit()
        conn.close()

    def show_all_volumes(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM volume
        ''')

        volumes = cursor.fetchall()

        conn.close()
        return volumes
        
    def delete_series(self, series_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM series WHERE series_id = ?
        ''', (series_id,))

        conn.commit()
        conn.close()

    def delete_volume(self, volume_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM volume WHERE volume_id = ?
        ''', (volume_id,))

        conn.commit()
        conn.close()

    def delete_publisher(self, publisher_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM publisher WHERE publisher_id = ?
        ''', (publisher_id,))

        conn.commit()
        conn.close()

    def show_all_comics(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.comic_id, s.name, c.issue_num 
            FROM comic c
            INNER JOIN series s ON s.series_id = c.series_id
        ''')

        comics = cursor.fetchall()

        conn.close()
        if comics:
            return comics
        else:
            return None

    def delete_comic(self, comic_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM comic WHERE comic_id = ?
        ''', (comic_id,))

        conn.commit()
        conn.close()

    def add_comic(self, series_id, issue_num, cover_price):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO comic (series_id, issue_num, cover_price) VALUES (?, ?, ?)
        ''', (series_id, issue_num, cover_price))

        conn.commit()
        conn.close()

    def update_comic(self, comic_id, image_url=None, description=None, series_id=None, current_price=None, issue_num=None, cover_price=None):
        conn = self.connect()
        cursor = conn.cursor()

        if image_url:
            cursor.execute('UPDATE comic SET image_url = ? WHERE comic_id = ?', (image_url, comic_id))
        if description:
            cursor.execute('UPDATE comic SET description = ? WHERE comic_id = ?', (description, comic_id))
        if series_id:
            cursor.execute('UPDATE comic SET series_id = ? WHERE comic_id = ?', (series_id, comic_id))
        if current_price:
            cursor.execute('UPDATE comic SET current_price = ? WHERE comic_id = ?', (current_price, comic_id))
        if issue_num:
            cursor.execute('UPDATE comic SET issue_num = ? WHERE comic_id = ?', (issue_num, comic_id))
        if cover_price:
            cursor.execute('UPDATE comic SET cover_price = ? WHERE comic_id = ?', (cover_price, comic_id))

        conn.commit()
        conn.close()
    
    def add_to_collection(self, comic_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO collection (user_id, comic_id) VALUES (?, ?)
        ''', (self.user_id, comic_id))

        conn.commit()
        conn.close()

    def show_user_comics(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT s.name AS series_name, c.issue_num
            FROM collection co
            INNER JOIN comic c ON c.comic_id = co.comic_id
            INNER JOIN series s ON c.series_id = s.series_id
            WHERE co.user_id = ?
        ''', (self.user_id,))

        comics = cursor.fetchall()

        conn.close()
        return comics

    def login_user(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT user_id, username, clearence_level FROM user WHERE username = ? AND password = ?
        ''', (username, password))

        user = cursor.fetchone()

        if user:
            self.user_id = user[0]
            self.username = user[1]
            self.clearance_level = user[2]

        conn.close()

        return user
    
    def update_volume(self, volume_id, name=None):
        conn = self.connect()
        cursor = conn.cursor()

        if name:
            cursor.execute('UPDATE volume SET name = ? WHERE volume_id = ?', (f'Vol. {name}', volume_id))

        conn.commit()
        conn.close()

    def update_publisher(self, publisher_id, name=None):
        conn = self.connect()
        cursor = conn.cursor()

        if name:
            cursor.execute('UPDATE publisher SET name = ? WHERE publisher_id = ?', (name, publisher_id))

        conn.commit()
        conn.close()

    def update_series(self, series_id, name=None, volume_id=None, publisher_id=None):
        conn = self.connect()
        cursor = conn.cursor()

        if name:
            cursor.execute('UPDATE series SET name = ? WHERE series_id = ?', (name, series_id))
        if volume_id:
            cursor.execute('UPDATE series SET volume_id = ? WHERE series_id = ?', (volume_id, series_id))
        if publisher_id:
            cursor.execute('UPDATE series SET publisher_id = ? WHERE series_id = ?', (publisher_id, series_id))

        conn.commit()
        conn.close()

    def get_series(self, series_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM series WHERE series_id = ?''', (series_id,))

        series = cursor.fetchone()

        if series:
            return series
        else:
            return None

if __name__ == '__main__':
    while True:
        manager = Manager()
        print('''
        1.) Login
        2.) Register
    ''')
        beginning_num = input('Please Select an option: ')
        if beginning_num == '1':
            while True:
                username = input('Please enter your username: ')
                password = input('Please enter your password: ')
                user = manager.login_user(username, password)
                if user:
                    break
                else:
                    print('1.) Try again\n2.) Return to Menu')
                    login_num = input('Please Select an option: ')
                    if login_num == '1':
                        continue
                    elif login_num == '2':
                        break
        elif beginning_num == '2':
            username = input('Please enter your username: ')
            password = input('Please enter your password: ')
            manager.add_user(username, password)
            while True:
                username = input('Please enter your username: ')
                password = input('Please enter your password: ')
                user = manager.login_user(username, password)
                if user:
                    break
                else:
                    print('1.) Try again\n2.) Return to Menu')
                    login_num = input('Please Select an option: ')
                    if login_num == '1':
                        continue
                    elif login_num == '2':
                        break
        if manager.username is not None:
            while True:
                print('What would you like to do?')
                print('1.) Select\n2.) Insert\n3.) Delete\n4.) Update\n5.) Return to Menu')
                action_num = input('Please Select An option: ')
                if action_num == '1' and manager.clearance_level > 0:
                    collection_table = manager.show_user_comics()
                    for comic in collection_table:
                        print(f'{collection_table.index(comic) + 1}.) {comic[0]} #{comic[1]}')
                    input('Hit Enter to continue')
                elif action_num == '2' and manager.clearance_level > 1:
                    print('What would you like to Insert?')
                    print('1.) Volume\n2.) Publisher\n3.) Series\n4.) Comic\n5.) Add to Collection')
                    crud_num = input('Please Select an Option: ')
                    if crud_num == '1':
                        print('Enter Volume')
                        while True:
                            try:
                                volume_num = int(input('Please Enter a Volume Number: '))
                                break
                            except ValueError:
                                print("That's not a valid number. Please enter an integer.")
                        manager.add_volume(volume_num)
                        print("\nVolume Successfully Added\n")
                    elif crud_num == '2':
                        print('Enter Publisher')
                        name = input('Please enter a publisher name: ')
                        manager.add_publisher(name)
                        print("\nPublisher Successfully Added\n")
                    elif crud_num == '3':
                        print('Enter Series')
                        publishers = manager.show_all_publishers()
                        volumes = manager.show_all_volumes()
                        while True:
                            if publishers and volumes:
                                while True:
                                    print('Please select a publisher:')
                                    for publisher in publishers:
                                        print(f'{publishers.index(publisher) + 1}.) {publisher[1]}')
                                    try:
                                        publisher_num = int(input('Please Select a number: '))
                                        if 0 <= publisher_num - 1 < len(publishers):
                                            break
                                        else:
                                            print('Please enter a valid option')
                                    except ValueError:
                                        print("That's not a valid number. Please enter an integer.")
                                print('Please select a Volume')
                                while True:
                                    for volume in volumes:
                                        print(f'{volumes.index(volume) + 1}.) {volume[1]}')
                                    try:
                                        volume_num = int(input('Please Select a number: '))
                                        if 0 <= volume_num - 1 < len(volumes):
                                            break
                                        else:
                                            print('Please enter a valid option')
                                    except ValueError:
                                        print("That's not a valid number. Please enter an integer.")
                                name = input('Please enter the series name: ')
                                manager.add_series(name, volumes[volume_num-1][0], publishers[publisher_num-1][0])
                                print("\nSeries Successfully Added\n")
                                break
                            else:
                                print('Please add a publisher and volume first')
                    elif crud_num == '4':
                        print('Enter Comic')
                        while True:
                            try:
                                issue_num = int(input('Please enter an issue number: '))
                                print('Cover Price Example: 2.99')
                                cover_price = format(float(input('Please enter a Cover Price: ')), '.2f')
                                break
                            except ValueError:
                                print('Enter a valid number')
                        series_table = manager.show_all_series()
                        if not series_table:
                            print("Please add a Series")
                            break
                        else:
                            if issue_num and cover_price:
                                while True:
                                    print('\nPlease Pick a Series')
                                    for series in series_table:
                                        print(f'{series_table.index(series)+1}.) {series[1]}')
                                    try:
                                        series_num = int(input('Please Chose a Series Name: '))
                                        if 0 <= series_num - 1 < len(series_table):
                                            break
                                        else:
                                            raise ValueError
                                    except ValueError:
                                        print('Enter a valid number that is in the list')
                                manager.add_comic(series_table[series_num-1][0], issue_num, cover_price)
                                print("\nComic Successfully Added\n")
                    elif crud_num == '5':
                        print('Enter Collection')
                        comics_table = manager.show_all_comics()
                        if comics_table:
                            while True:
                                for comic in comics_table:
                                    print(f'{comics_table.index(comic) + 1}.) {comic[1]} #{comic[2]}')
                                try:
                                    comic_num = int(input('Please choose a Comic: '))
                                    if 0 <= comic_num - 1 < len(comics_table):
                                        break
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print('Please enter a valid number that is within the range')
                            manager.add_to_collection(comics_table[comic_num-1][0])
                            print("\nComic Successfully Added\n")
                        else:
                            print("Please Add A Comic Before Adding to Collection")
                elif action_num == '3' and manager.clearance_level > 2:
                    print('What would you like to Delete?')
                    print('1.) Volume\n2.) Publisher\n3.) Series\n4.) Comic\n5.) Delete From Collection')
                    crud_num = input('Please Select an Option: ')
                    if crud_num == '1':
                        print('Delete Volume')
                        while True:
                            volume_table = manager.show_all_volumes()
                            for volume in volume_table:
                                print(f'{volume_table.index(volume)+1}.) {volume[1]}')
                            try:
                                volume_num = int(input('Please Enter a Volume Number: '))
                                if 0 <= volume_num - 1 < len(volume_table):
                                    break
                                else:
                                    raise ValueError
                            except ValueError:
                                print("That's not a valid number. Please enter an integer.")
                        manager.delete_volume(volume_table[volume_num-1][0])
                        print("\nVolume Successfully Deleted\n")
                    elif crud_num == '2':
                        print('Delete Publisher')
                        publisher_table = manager.show_all_publishers()
                        if publisher_table:
                            while True:
                                for publisher in publisher_table:
                                    print(f'{publisher_table.index(publisher) + 1}.) {publisher[1]}')
                                try:
                                    publisher_num = int(input('Please select a publisher name: '))
                                    if 0 <= publisher_num - 1 < len(publisher_table):
                                        break
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print('Please enter a valid number')
                            manager.delete_publisher(publisher_table[publisher_num-1][0])
                            print("\nPublisher Successfully Deleted\n")
                    elif crud_num == '3':
                        print('Delete Series')
                        series_table = manager.show_all_series()
                        if series_table:
                            while True:
                                for series in series_table:
                                    print(f'{series_table.index(series) + 1}.) {series[1]}')
                                try:
                                    series_num = int(input('Please Select a number: '))
                                    if 0 <= series_num - 1 < len(series_table):
                                        break
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print("That's not a valid number. Please enter an integer.")
                            manager.delete_series(series_table[series_num-1][0])
                            print("\nSeries Successfully Deleted\n")
                        else:
                            print("Please Enter a Series First")
                    elif crud_num == '4':
                        print('Delete Comic')
                        comic_table = manager.show_all_comics()
                        if comic_table:
                            while True:
                                for comic in comic_table:
                                    print(f'{comic_table.index(comic) + 1}.) {comic[1]} #{comic[2]}')
                                try:
                                    comic_num = int(input('Please Choose a Comic: '))
                                    if 0 <= comic_num - 1 < len(comic_table):
                                        break
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print('Please enter a valid number that is in the list')
                            manager.delete_comic(comic_table[comic_num-1][0])
                            print("\nComic Successfully Deleted\n")
                        else:
                            print('\nPlease Enter a Comic First\n')
                    elif crud_num == '5':
                        print('Delete From Collection')
                        while True:
                            collection_table = manager.show_user_comics()
                            if collection_table:
                                while True:
                                    for comic in collection_table:
                                        print(f'{collection_table.index(comic) + 1}.) {comic[1]} #{comic[2]}')
                                    try:
                                        comic_num = int(input('Please Choose a Comic: '))
                                        if 0 <= comic_num - 1 < len(collection_table):
                                            break
                                        else:
                                            raise ValueError
                                    except ValueError:
                                        print('Please enter a valid number')
                                manager.delete_collection(collection_table[comic_num-1][0])
                                print("\nComic Successfully Deleted\n")
                                break
                            else:
                                print("\nPlease Enter a Comic to Collection First\n")
                                break
                elif action_num == '4' and manager.clearance_level > 3:
                    print('What would you like to Update?')
                    print('1.) Volume\n2.) Publisher\n3.) Series\n4.) Comic')
                    crud_num = input('Please Select an Option: ')
                    if crud_num == '1':
                        print('Update Volume')
                        volume_table = manager.show_all_volumes()
                        while True:
                            for volume in volume_table:
                                print(f'{volume_table.index(volume) + 1}.) {volume[1]}')
                            try:
                                volume_num = int(input('Please Choose a Volume: '))
                                if 0 <= volume_num - 1 < len(volume_table):
                                    break
                                else:
                                    raise ValueError
                            except ValueError:
                                print('Please enter a valid number')
                        while True:
                            try:
                                volume_id = volume_table[volume_num-1][0]
                                volume_num = int(input('Please Enter a Volume Number: '))
                                break
                            except ValueError:
                                print("That's not a valid number. Please enter an integer.")
                        manager.update_volume(volume_id, volume_num)
                        print("\nVolume Successfully Updated\n")
                    elif crud_num == '2':
                        print('Update Publisher')
                        publisher_table = manager.show_all_publishers()
                        if publisher_table:
                            while True:
                                for publisher in publisher_table:
                                    print(f'{publisher_table.index(publisher) + 1}.) {publisher[1]}')
                                try:
                                    publisher_num = int(input('Please Choose a Publisher: '))
                                    if 0 <= publisher_num - 1 < len(publisher_table):
                                        break
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print('Please enter a valid number')
                            publisher_id = publisher_table[publisher_num-1][0]
                            name = input('Please enter a publisher name: ')
                            manager.update_publisher(publisher_id, name)
                            print("\nPublisher Successfully Updated\n")
                        else:
                            print('Please Enter a Publisher First')
                    elif crud_num == '3':
                        print('Update Series')
                        series_table = manager.show_all_series()
                        if series_table:
                            while True:
                                for series in series_table:
                                    print(f'{series_table.index(series) + 1}.) {series[1]}')
                                try:
                                    series_num = int(input('Please Choose a Series: '))
                                    if 0 <= series_num - 1 < len(series_table):
                                        break
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print('Please enter a valid number')
                            series_id = series_table[series_num-1][0]
                            volumes = manager.show_all_volumes()
                            publishers = manager.show_all_publishers()
                            if publishers and volumes:
                                while True:
                                    for volume in volumes:
                                        print(f'{volumes.index(volume) + 1}.) {volume[1]}')
                                    try:
                                        volume_num = int(input('Please select a Volume: '))
                                        if 0 <= volume_num - 1 < len(volumes):
                                            break
                                        else:
                                            print('Please enter a valid option')
                                    except ValueError:
                                        print("That's not a valid number. Please enter an integer.")
                                while True:
                                    for publisher in publishers:
                                        print(f'{publishers.index(publisher) + 1}.) {publisher[1]}')
                                    try:
                                        publisher_num = int(input('Please select a Publisher: '))
                                        if 0 <= publisher_num - 1 < len(publishers):
                                            break
                                        else:
                                            print('Please enter a valid option')
                                    except ValueError:
                                        print("That's not a valid number. Please enter an integer.")
                                name = input('Please enter the series name: ')
                                manager.update_series(series_id, name, volumes[volume_num-1][0], publishers[publisher_num-1][0])
                                print("\nSeries Successfully Updated\n")
                            else:
                                print('Please Add a Publisher and Volume First')
                        else:
                            print('Please Enter a Series First')
                    elif crud_num == '4':
                        print('Update Comic')
                        comics_table = manager.show_all_comics()
                        if comics_table:
                            while True:
                                for comic in comics_table:
                                    print(f'{comics_table.index(comic) + 1}.) {comic[1]} #{comic[2]}')
                                try:
                                    comic_num = int(input('Please Choose a Comic: '))
                                    if 0 <= comic_num - 1 < len(comics_table):
                                        break
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print('Please enter a valid number')
                            series_table = manager.show_all_series()
                            if series_table:
                                comic_id = comics_table[comic_num-1][0]
                                while True:
                                    try:
                                        issue_num = int(input('Please enter an issue number: '))
                                        print('Cover Price Example: 2.99')
                                        cover_price = format(float(input('Please enter a Cover Price: ')), '.2f')
                                        break
                                    except ValueError:
                                        print('Enter a valid number')
                                while True:
                                    for series in series_table:
                                        print(f'{series_table.index(series) + 1}.) {series[1]}')
                                    try:
                                        series_num = int(input('Please Pick a Series: '))
                                        if 0 <= series_num - 1 < len(series_table):
                                            break
                                        else:
                                            raise ValueError
                                    except ValueError:
                                        print('Enter a valid number that is in the list')
                                manager.update_comic(comic_id, series_table[series_num-1][0], issue_num, cover_price)
                                print("\nComic Successfully Updated\n")
                            else:
                                print("Please Add a Series First")
                        else:
                            print('Please Add a Comic First')
                elif action_num == '5':
                    break
                else:
                    print("You do not have the required clearance level for this action")