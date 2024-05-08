import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QFileDialog


guncel_username = ""

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş")
        self.setGeometry(100, 100, 400, 200)

        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Giriş")
        self.register_button = QPushButton("Kaydol")

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        conn = sqlite3.connect('DATA.db')
        cursor = conn.cursor()
        username = self.username_input.text()
        password = self.password_input.text()
        global guncel_username
        guncel_username = username

        cursor.execute('''SELECT * FROM texts WHERE username = ? AND password = ?''', (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            self.menu_window = MenuWindow()
            self.menu_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış.")

    def register(self):
        conn = sqlite3.connect('DATA.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS texts (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

        username = self.username_input.text()
        password = self.password_input.text()

        cursor.execute('''SELECT * FROM texts WHERE username = ?''', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten mevcut.")
            conn.close()
            return

        try:
            cursor.execute('''INSERT INTO texts (username, password) VALUES (?, ?)''', (username, password))
            conn.commit()
            success = True
        except Exception as e:
            print("Error:", e)
            success = False

        conn.close()

        RegisterResultWindow(success)

class RegisterResultWindow(QMessageBox):
    def __init__(self, success):
        super().__init__()

        if success:
            self.setWindowTitle("Başarılı")
            self.setText("Kayıt başarıyla gerçekleştirildi.")
        else:
            self.setWindowTitle("Başarısız")
            self.setText("Kayıt sırasında bir hata oluştu.")

        self.exec_()

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menü")
        self.setGeometry(100, 100, 400, 200)
        compare_button = QPushButton("Karşılaştır")
        operations_button = QPushButton("İşlemler")
        exit_button = QPushButton("Çıkış")

        layout = QVBoxLayout()
        layout.addWidget(compare_button)
        layout.addWidget(operations_button)
        layout.addWidget(exit_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        operations_button.clicked.connect(self.open_operations_menu)
        compare_button.clicked.connect(self.compare_menu)
        exit_button.clicked.connect(self.close)

    def open_operations_menu(self):
        self.operations_menu = OperationsMenu()
        self.operations_menu.show()
    def compare_menu(self):
        self.ca = CompareMenu()
        self.ca.show()

class OperationsMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("İşlemler")
        self.setGeometry(100, 100, 400, 200)

        password_button = QPushButton("Şifre Değiştir")

        layout = QVBoxLayout()
        layout.addWidget(password_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        password_button.clicked.connect(self.open_password_change_menu)

    def open_password_change_menu(self):
        self.password_change_menu = PasswordChangeMenu()
        self.password_change_menu.show()

class PasswordChangeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şifre Değiştir")
        self.setGeometry(100, 100, 400, 200)

class PasswordChangeMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şifre Değiştir")
        self.setGeometry(100, 100, 400, 200)

        self.old_password_label = QLabel("Mevcut Şifre:")
        self.old_password_input = QLineEdit()
        self.new_password_label = QLabel("Yeni Şifre:")
        self.new_password_input = QLineEdit()
        self.confirm_password_label = QLabel("Yeni Şifreyi Onayla:")
        self.confirm_password_input = QLineEdit()
        self.change_password_button = QPushButton("Değiştir")

        layout = QVBoxLayout()
        layout.addWidget(self.old_password_label)
        layout.addWidget(self.old_password_input)
        layout.addWidget(self.new_password_label)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.change_password_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.change_password_button.clicked.connect(self.change_password)

    def change_password(self):
        new_password = self.new_password_input.text()
        global guncel_username
        conn = sqlite3.connect('DATA.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''UPDATE texts SET password = ? WHERE username = ?''', (new_password, guncel_username))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Şifre başarıyla güncellendi.")
        except Exception as e:
            print("Error:", e)
            QMessageBox.warning(self, "Hata", "Şifre güncelleme sırasında bir hata oluştu.")

        conn.close()
class CompareMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metin Karşılaştır")
        self.setGeometry(100, 100, 400, 200)

        compare_x_button = QPushButton("Levenshtein  Algoritmasıyla Karşılaştır")
        compare_x_button.clicked.connect(self.open_compare_with_x_window)

        compare_y_button = QPushButton("Jaccard Algoritmasıyla Karşılaştır")
        compare_y_button.clicked.connect(self.compare_with_y_algorithm)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(compare_x_button)
        layout.addWidget(compare_y_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_compare_with_x_window(self):
        deger = "x"
        self.compare_x_window = CompareWithXWindow(deger)
        self.compare_x_window.show()
    def compare_with_y_algorithm(self):
        deger = "y"
        self.compare_x_window = CompareWithXWindow(deger)
        self.compare_x_window.show()

class CompareWithXWindow(QMainWindow):
    def __init__(self, deger):
        super().__init__()
        self.setWindowTitle("X Algoritmasıyla Karşılaştır")
        self.setGeometry(200, 200, 400, 200)
        self.kontrol = deger

        self.file1_label = QLabel("Metin 1:")
        self.file1_textbox = QLineEdit()
        self.file1_button = QPushButton("Dosya Seç")

        self.file2_label = QLabel("Metin 2:")
        self.file2_textbox = QLineEdit()
        self.file2_button = QPushButton("Dosya Seç")

        self.compare_button = QPushButton("Karşılaştır")

        layout = QVBoxLayout()
        layout.addWidget(self.file1_label)
        layout.addWidget(self.file1_textbox)
        layout.addWidget(self.file1_button)
        layout.addWidget(self.file2_label)
        layout.addWidget(self.file2_textbox)
        layout.addWidget(self.file2_button)
        layout.addWidget(self.compare_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.file1_button.clicked.connect(self.select_file1)
        self.file2_button.clicked.connect(self.select_file2)
        self.compare_button.clicked.connect(self.compare_texts)

    def select_file1(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Text Files (*.txt)")
        if filename:
            self.file1_textbox.setText(filename)

    def select_file2(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Text Files (*.txt)")
        if filename:
            self.file2_textbox.setText(filename)

    def compare_texts(self):
        file1_path = self.file1_textbox.text()
        file2_path = self.file2_textbox.text()

        try:
            with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
                content1 = file1.read()
                content2 = file2.read()

                if self.kontrol == "x":
                    similarity = self.levenshtein_similarity(content1, content2)
                    print("Levenshtein benzerlik oranı:", similarity)
                    QMessageBox.information(self, "Benzerlik Oranı", f"Levenshtein benzerlik oranı: {similarity}")

                elif self.kontrol == "y":
                    similarity = self.jaccard_similarity(content1, content2)
                    print("jaccard_ benzerlik oranı:", similarity)
                    QMessageBox.information(self, "Benzerlik Oranı", f"Jaccard benzerlik oranı: {similarity}")


        except Exception as e:
            print("Error:", e)
            QMessageBox.warning(self, "HATA", f"Hata: {e}")

    def jaccard_similarity(self, s1, s2):
        set1 = set(s1.split())
        set2 = set(s2.split())

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        similarity = intersection / union if union != 0 else 0

        return similarity

    def levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def levenshtein_similarity(self, s1, s2):
        distance = self.levenshtein_distance(s1, s2)
        max_length = max(len(s1), len(s2))
        similarity = (max_length - distance) / max_length
        return similarity
def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
