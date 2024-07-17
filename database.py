import sqlite3
class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
            with self.connection:
                return bool(len(self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)))

    def gallery_add_like(self, like, key):
            with self.connection:
                return self.connection.execute("UPDATE gallery SET likes = ? WHERE uin = ?", (like, key,))
    def calc_exists(self, user_id):
            with self.connection:
                return bool(len(self.cursor.execute("SELECT * FROM calculator WHERE user_id = ?", (user_id,)).fetchmany(1)))

    def topic(self, naming):
        with self.connection:
            return self.cursor.execute(f"SELECT topic FROM headers WHERE naming = ?", (naming, )).fetchall()

    def all_topic(self):
        with self.connection:
            return self.cursor.execute(f"SELECT topic FROM headers" ).fetchall()

    def add_topic(self, topic, naming):
            with self.connection:
                return self.connection.execute("INSERT INTO headers (topic, naming) VALUES (?, ?)", (topic, naming,))
    def delete_headers(self, key):
        with self.connection:
            return self.cursor.execute(f"DELETE FROM headers WHERE topic = ?", (key, ))

    def name(self, key):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM products WHERE id = ? and previous = 'Начало' ", (key,)).fetchall()

    def gallery_name(self):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM gallery WHERE previous = 'Начало'").fetchall()

    def gallery_start(self):
        with self.connection:
            return self.cursor.execute(f"SELECT uin FROM gallery WHERE previous = 'Начало'").fetchall()

    def gallery_end(self):
        with self.connection:
            return self.cursor.execute(f"SELECT uin FROM gallery WHERE next = 'Конец'").fetchall()


    def uin(self):
        with self.connection:
            return self.cursor.execute(f"SELECT uin FROM products").fetchall()

    def gallery_uin(self):
        with self.connection:
            return self.cursor.execute(f"SELECT uin FROM gallery").fetchall()

    def get_label(self, key):
        with self.connection:
            return self.cursor.execute(f"SELECT id FROM headers WHERE topic = ?", (key,)).fetchone()

    def neighbours(self, uin, label):
        with self.connection:
            return self.cursor.execute(f"SELECT previous, next FROM products WHERE uin = ? and label = ? ", (uin, label)).fetchall()
    def gallery_neighbours(self, uin):
        with self.connection:
            return self.cursor.execute(f"SELECT previous, next FROM gallery WHERE uin = ? ", (uin,)).fetchall()

    def excel_users(self):
        with self.connection:
            return self.cursor.execute(f"SELECT user_id, first_name, last_name FROM users ").fetchall()
    def call_name(self, key):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM products WHERE uin = ? ", (key,)).fetchall()

    def gallery_call_name(self, key):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM gallery WHERE uin = ? ", (key,)).fetchall()

    def change_1(self, next, uin):
        with self.connection:
            return self.cursor.execute("UPDATE products SET next = ? WHERE uin = ?", (next, uin,))

    def change_2(self, previous, uin):
        with self.connection:
            return self.cursor.execute("UPDATE products SET previous = ? WHERE uin = ?", (previous, uin,))

    def gallery_change_1(self, next, uin):
        with self.connection:
            return self.cursor.execute("UPDATE gallery SET next = ? WHERE uin = ?", (next, uin,))

    def gallery_change_2(self, previous, uin):
        with self.connection:
            return self.cursor.execute("UPDATE gallery SET previous = ? WHERE uin = ?", (previous, uin,))

    def gallery_get_uin(self, key):
        with self.connection:
            return self.cursor.execute(f"SELECT likes FROM gallery WHERE uin = ? ", (key,)).fetchall()

    def add_user(self, user_id, first_name, last_name, username):
            with self.connection:
                return self.connection.execute("INSERT INTO users (user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)", (user_id, first_name, last_name, username))

    def get_username(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT username FROM users WHERE user_id = ? ", (user_id,)).fetchall()

    def referrals(self, who_invite, invited, date, time):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO referrals (who_invite, invited, date, time) VALUES (?, ?, ?, ?)", (who_invite, invited, date, time,))

    def add_calc(self, user_id):
            with self.connection:
                return self.connection.execute("INSERT INTO calculator (user_id) VALUES (?)", (user_id,))

    def user_update(self, first_name, last_name, username, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET first_name = ?, last_name = ?, username = ?, active = 1  WHERE user_id = ?", (first_name, last_name, username, user_id,))

    def user_update_age(self, age, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET age = ? WHERE user_id = ?", (age, user_id,))

    def user_update_email(self, email, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET e_mail = ? WHERE user_id = ?", (email, user_id,))

    def user_update_language(self, language, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id,))

    def user_politics(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT politics FROM users WHERE user_id = ?", ( user_id,))

    def set_user_politics(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET politics = 1 WHERE user_id = ?", (user_id,))

    def user_update_phone_number(self, number, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET phone_number = ? WHERE user_id = ?", (number, user_id,))

    def user_update_spawn(self, spawn_point, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET spawn_point = ? WHERE user_id = ?", (spawn_point, user_id,))

    def get_lang(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT language FROM users WHERE user_id = ?", (user_id,)).fetchall()

    def get_dop_calc(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT tax, amortization, profit, work FROM calculator WHERE user_id = ?", (user_id,)).fetchall()

    def add_card(self, id, uin, label, name, description, previous, next, photo, file_id, link, link_text):
            with self.connection:
                return self.connection.execute("INSERT INTO products (id, uin, label, name, description, previous, next, photo, file_id, link, text_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, uin, label, name, description, previous, next, photo, file_id, link, link_text,))

    def add_gallery_card(self, uin, name, previous, next, photo, file_id, link, link_text):
            with self.connection:
                return self.connection.execute("INSERT INTO gallery (uin, name, previous, next, photo, file_id, link, text_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (uin, name, previous, next, photo, file_id, link, link_text,))

    def calc_update(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET styrofoam = 0, expanded = 0, roof = 0, glue = 0, priming = 0, acrylic = 0, varnish = 0, materials = 0  WHERE user_id = ?", (user_id, ))

    def update_styrofoam(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET styrofoam = ?  WHERE user_id = ?", (key, user_id, ))

    def update_warning(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET warning = ?  WHERE user_id = ?", (key, user_id, ))

    def get_warning(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT warning FROM calculator WHERE user_id = ?", (user_id,)).fetchall()

    def update_roof(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET roof = ?  WHERE user_id = ?", (key, user_id, ))

    def update_expanded(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET expanded = ?  WHERE user_id = ?", (key, user_id, ))

    def update_priming(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET priming = ?  WHERE user_id = ?", (key, user_id, ))

    def update_acrylic(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET acrylic = ?  WHERE user_id = ?", (key, user_id,))

    def update_varnish(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET varnish = ?  WHERE user_id = ?", (key, user_id,))

    def update_glue(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET glue = ?  WHERE user_id = ?", (key, user_id,))

    def update_materials(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET materials = ?  WHERE user_id = ?", (key, user_id,))

    def update_tax(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET tax = ?  WHERE user_id = ?", (key, user_id,))

    def update_amortization(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET amortization = ?  WHERE user_id = ?", (key, user_id,))

    def update_profit(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET profit = ?  WHERE user_id = ?", (key, user_id,))

    def update_work(self, key, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE calculator SET work = ?  WHERE user_id = ?", (key, user_id,))

    def calc_state(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM calculator WHERE user_id = ?", (user_id,)).fetchall()

    def get_topic(self, key):
        with self.connection:
            return self.cursor.execute(f"SELECT topic FROM headers WHERE id = ? ", (key,)).fetchall()

    def delete(self, uin):
        with self.connection:
            return self.cursor.execute("DELETE FROM products WHERE uin = ?", (uin, ))

    def delete_1(self, nxt, uin):
        with self.connection:
            return self.cursor.execute("UPDATE products SET next = ? WHERE uin = ?", (nxt, uin, ))

    def delete_2(self, prv, uin):
        with self.connection:
            return self.cursor.execute("UPDATE products SET previous = ? WHERE uin = ?", (prv, uin, ))

    def gallery_delete(self, uin):
        with self.connection:
            return self.cursor.execute("DELETE FROM gallery WHERE uin = ?", (uin, ))

    def gallery_delete_1(self, nxt, uin):
        with self.connection:
            return self.cursor.execute("UPDATE gallery SET next = ? WHERE uin = ?", (nxt, uin, ))
    def gallery_delete_2(self, prv, uin):
        with self.connection:
            return self.cursor.execute("UPDATE gallery SET previous = ? WHERE uin = ?", (prv, uin, ))

    def gallery_update_name(self, name, uin):
        with self.connection:
            return self.cursor.execute("UPDATE gallery SET name = ? WHERE uin = ?", (name, uin, ))

    def gallery_update_buttons(self, link, text_link, uin):
        with self.connection:
            return self.cursor.execute("UPDATE gallery SET link = ?, text_link = ? WHERE uin = ?", (link, text_link, uin, ))

    def gallery_update_photo(self, photo, uin):
        with self.connection:
            return self.cursor.execute("UPDATE gallery SET photo = ? WHERE uin = ?", (photo, uin, ))

    def gallery_update_file_id(self, file, uin):
        with self.connection:
            return self.cursor.execute("UPDATE gallery SET file_id = ? WHERE uin = ?", (file, uin, ))

    def statistics(self):
        with self.connection:
            return self.cursor.execute("SELECT text FROM messages").fetchall()

    def statistics_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM messages").fetchall()

    def add_statistics(self, user_id, text, date, time):
            with self.connection:
                return self.connection.execute("INSERT INTO messages (user_id, text, date, time) VALUES (?, ?, ?, ?) ", (user_id, text, date, time))

    def add_mailing(self, name, message_id, chat_id, buttons):
            with self.connection:
                return self.connection.execute("INSERT INTO mailing (name, message_id, chat_id, buttons) VALUES (?, ?, ?, ?) ", (name, message_id, chat_id, buttons))

    def get_mailing(self, key):
        with self.connection:
            return self.cursor.execute(f"SELECT name, chat_id, buttons FROM mailing WHERE message_id = ? ", (key,)).fetchall()

    def get_user_firstname(self, key):
        with self.connection:
            return self.cursor.execute(f"SELECT first_name FROM users WHERE user_id = ? ", (key,)).fetchall()

    def get_user_lastname(self, key):
        with self.connection:
            return self.cursor.execute(f"SELECT last_name FROM users WHERE user_id = ? ", (key,)).fetchall()

    def get_user(self, key):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM users WHERE user_id = ? ", (key,)).fetchall()

    def get_count_users(self):
        with self.connection:
            return self.cursor.execute(f"SELECT COUNT(*) FROM users").fetchone()

    def get_all_users(self):
        with self.connection:
            return self.cursor.execute(f"SELECT user_id FROM users WHERE active = 1").fetchall()
    def product_update_name(self, name, uin):
        with self.connection:
            return self.cursor.execute("UPDATE products SET name = ? WHERE uin = ?", (name, uin, ))

    def product_update_description(self, name, uin):
        with self.connection:
            return self.cursor.execute("UPDATE products SET description = ? WHERE uin = ?", (name, uin, ))

    def product_update_buttons(self, link, text_link, uin):
        with self.connection:
            return self.cursor.execute("UPDATE products SET link = ?, text_link = ? WHERE uin = ?", (link, text_link, uin, ))

    def product_update_photo(self, photo, uin):
        with self.connection:
            return self.cursor.execute("UPDATE products SET photo = ? WHERE uin = ?", (photo, uin, ))

    def product_update_file_id(self, file, uin):
        with self.connection:
            return self.cursor.execute("UPDATE products SET file_id = ? WHERE uin = ?", (file, uin, ))

    def user_set_active(self, active, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id, ))

    def add_telegraph(self, telegraph, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET telegraph = ? WHERE user_id = ?", (telegraph, user_id, ))

    def get_telegraph(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT telegraph FROM users WHERE user_id = ?", (user_id, )).fetchall()

    def name_update(self):
        with self.connection:
            return self.cursor.execute(f"SELECT text_link FROM products WHERE label < 15", ).fetchall()

    def insert_translate(self, RU, EN):
        with self.connection:
            return self.connection.execute("INSERT INTO translate (RU, ENG) VALUES (?, ?) ", (RU, EN,))

    def get_translation(self, RU):
        with self.connection:
            return self.cursor.execute(f"SELECT ENG FROM translate WHERE RU = ?", (RU, )).fetchall()

    def get_en_translation(self, ENG):
        with self.connection:
            return self.cursor.execute(f"SELECT RU FROM translate WHERE ENG = ?", (ENG, )).fetchall()

    def get_admins(self):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM admins", ()).fetchall()

    def add_admin(self, admin_id):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO admins (admin_id) VALUES (?)", (admin_id, ))

    def delete_admin(self, admin_id):
        with self.connection:
            return self.cursor.execute(f"DELETE FROM admins WHERE admin_id = ?", (admin_id, ))

    def get_admin(self, user_id):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM admins WHERE admin_id = ?", (user_id, )).fetchall()

    def get_admin_id_menu(self):
        with self.connection:
            return self.cursor.execute(f"SELECT admin_id FROM admins WHERE change_menu = 1 ", ).fetchall()

    def get_admin_id_gall(self):
        with self.connection:
            return self.cursor.execute(f"SELECT admin_id FROM admins WHERE change_gallery = 1",).fetchall()

    def get_admin_id_mail(self):
        with self.connection:
            return self.cursor.execute(f"SELECT admin_id FROM admins WHERE mailing = 1", ).fetchall()

    def get_admin_id_stat(self):
        with self.connection:
            return self.cursor.execute(f"SELECT admin_id FROM admins WHERE get_statistics = 1", ).fetchall()

    def update_admin_change_menu(self, change_menu, user_id,):
        with self.connection:
            return self.cursor.execute("UPDATE admins SET change_menu = ? WHERE admin_id = ?", (change_menu, user_id, ))

    def update_admin_change_gallery(self, change_gallery, user_id,):
        with self.connection:
            return self.cursor.execute("UPDATE admins SET change_gallery = ? WHERE admin_id = ?", (change_gallery, user_id, ))

    def update_admin_mailing(self, mailing, user_id,):
        with self.connection:
            return self.cursor.execute("UPDATE admins SET mailing = ? WHERE admin_id = ?", (mailing, user_id, ))

    def update_admin_get_statistics(self,get_statistics, user_id,):
        with self.connection:
            return self.cursor.execute("UPDATE admins SET get_statistics = ? WHERE admin_id = ?", (get_statistics, user_id, ))
    def commit(self):
        with self.connection:
            return self.connection.commit()