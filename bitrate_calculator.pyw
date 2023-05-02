from PySide6 import QtWidgets
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QIcon, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QListWidget, QGroupBox, QLineEdit, QMessageBox, QFileDialog, QDialog, QComboBox, QTabWidget, QTextEdit
import sys, cv2, os, json

# Завантаження списку усіх мов. Якщо ваша мова відсутня в списку, напишіть мені, я залюбки додам її
with open("configs/languages.json", encoding="utf-8") as languages:
    lang_list = json.load(languages)

# Завантаження даних з налаштувань
    with open("configs/settings.json", encoding="utf-8") as f:
        settings = json.load(f)

# Завантаження перекладу до вибраної мови
for lang_code in lang_list.values():
    if settings['language'] == lang_code:
        try:
            with open(f'lang/{lang_code}.json', "r", encoding="utf-8") as g:
                translation_text = json.load(g)
                break
        except:
            with open(f'lang/enUS.json', "r", encoding="utf-8") as g:
                translation_text = json.load(g)
                break

class BitrateCalculator(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Параметри вікна
        self.setWindowTitle(translation_text["text_window_title"])
        self.setFixedSize(640, 330)

        # Головний віджет вікна (саме на цьому віджеті розташовані усі інші елементи)
        self.widget_main = QWidget(self)
        self.widget_main.setGeometry(0, 0, 640, 330)

        # Створення фрейму "Історія"
        self.groupbox_history = QGroupBox(self.widget_main)
        self.groupbox_history.setTitle(translation_text["text_groupbox_history"])
        self.groupbox_history.setFixedSize(180, 315)
        self.groupbox_history.move(10, 5)

        # Створення списку "Історія"
        self.list_history = QListWidget(self.widget_main)
        self.list_history.setFixedSize(160, 240)
        self.list_history.move(20, 30)

        # Створення кнопки очищення історії
        self.button_history = QPushButton(self.widget_main)
        self.button_history.setText(translation_text["text_button_history"])
        self.button_history.setFixedSize(160, 30)
        self.button_history.move(20, 280)
        self.button_history.clicked.connect(self.event_clear_history)

        # Створення фрейму "Автоматичне заповнення"
        self.label_title_auto = QGroupBox(self.widget_main)
        self.label_title_auto.setTitle(translation_text["text_title_label_auto"])
        self.label_title_auto.setFixedSize(430, 70)
        self.label_title_auto.move(200, 5)

        # Створення кнопки "Вибрати файл"
        self.button_open = QPushButton(self.widget_main)
        self.button_open.setText(translation_text["text_button_open"])
        self.button_open.setFixedSize(410, 30)
        self.button_open.move(210, 30)
        self.button_open.clicked.connect(self.event_open_file)

        # Створення мітки "Ручне заповнення"
        self.label_title_manual = QGroupBox(self.widget_main)
        self.label_title_manual.setTitle(translation_text["text_label_title_manual"])
        self.label_title_manual.setFixedSize(430, 240)
        self.label_title_manual.move(200, 80)

        # Створення мітки "Розмір відео у МБ"
        self.label_video_size = QLabel(self.widget_main)
        self.label_video_size.setText(translation_text["text_label_video_size"])
        self.label_video_size.setFixedWidth(self.label_video_size.sizeHint().width())
        self.label_video_size.move(210, 105)

        # Створення поля до мітки "Розмір відео у МБ"
        self.ltext_dynamic_size1 = 210+self.label_video_size.sizeHint().width()+10

        self.ltext_video_size = QLineEdit(self.widget_main)
        self.ltext_video_size.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*")))
        self.ltext_video_size.setFixedSize(640-self.ltext_dynamic_size1-20, 20)
        self.ltext_video_size.move(self.ltext_dynamic_size1, 105)

        # Створення мітки "Тривалість відео в секундах"
        self.label_video_duration = QLabel(self.widget_main)
        self.label_video_duration.setText(translation_text["text_label_video_duration"])
        self.label_video_duration.setFixedWidth(self.label_video_duration.sizeHint().width())
        self.label_video_duration.move(210, 135)

        # Створення поля до мітки "Тривалість відео в секундах"
        self.ltext_dynamic_size2 = 210+self.label_video_duration.sizeHint().width()+10

        self.ltext_video_duration = QLineEdit(self.widget_main)
        self.ltext_video_duration.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*")))
        self.ltext_video_duration.setFixedSize(640-self.ltext_dynamic_size2-20, 20)
        self.ltext_video_duration.move(self.ltext_dynamic_size2, 135)

        # Створення кнопки "Обчислити"
        self.button_calc = QPushButton(self.widget_main)
        self.button_calc.setText(translation_text["text_button_calc"])
        self.button_calc.setFixedSize(410, 30)
        self.button_calc.move(210, 175)
        self.button_calc.clicked.connect(self.event_calculate)

        # Створення кнопки "Налаштування"
        self.button_settings = QPushButton(self.widget_main)
        self.button_settings.setText(translation_text["text_button_settings"])
        self.button_settings.setFixedSize(195, 30)
        self.button_settings.move(385, 280)
        self.button_settings.clicked.connect(self.event_show_settings)

        # Створення кнопки "Інформація"
        self.button_info_icon = QIcon("icons/info.svg")

        self.button_info = QPushButton(self.widget_main)
        self.button_info.setIcon(self.button_info_icon)
        self.button_info.setFixedSize(30, 30)
        self.button_info.move(590, 280)
        self.button_info.clicked.connect(self.event_show_info)


    def event_clear_history(self):
        if not self.list_history.count() == 0:
            self.list_history.clear()

            self.msg_clear_history = QMessageBox(self)
            self.msg_clear_history.setWindowTitle(translation_text["text_msg_clear_history_title"])
            self.msg_clear_history.setText(translation_text["text_msg_clear_history_desc"])
            self.msg_clear_history.setIcon(QtWidgets.QMessageBox.Icon(QMessageBox.Information))
            self.msg_clear_history.exec()


    def event_open_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(None, translation_text["text_open_dialog_title"], "", "Video Files (*.avi *.mp4 *.mkv *.mov *.wmv *.webm)")

        if self.file_path:
            self.video = cv2.VideoCapture(self.file_path)
            self.video_fps = self.video.get(cv2.CAP_PROP_FPS)
            self.video_frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_duration = self.video_frame_count/self.video_fps

            self.ltext_video_size.setText(str(round(os.path.getsize(self.file_path)/1024/1024, 1)))
            self.ltext_video_duration.setText(str(int(self.video_duration)))


    def event_calculate(self):
        self.result_msg = QMessageBox(self)

        if not self.ltext_video_size.text().strip() or not self.ltext_video_duration.text().strip():
            self.result_msg.setWindowTitle(translation_text["text_msg_result_title_failed"])
            self.result_msg.setText(translation_text["text_msg_result_title_failed_desc"])
            self.result_msg.setIcon(QtWidgets.QMessageBox.Icon(QMessageBox.Critical))
            self.result_msg.exec()
        else:
            self.video_size = float(self.ltext_video_size.text())
            self.video_duration = float(self.ltext_video_duration.text()) 
            self.result = round((self.video_size/self.video_duration)*8*1000, 1)

            self.result_msg.setWindowTitle(translation_text["text_msg_result_title_success"])
            self.result_msg.setText(f"{translation_text['text_msg_result_desc']} - {self.result} {translation_text['text_kbits']}.")
            self.result_msg.setIcon(QtWidgets.QMessageBox.Icon(QMessageBox.Information))
            self.result_msg.exec()

            self.list_history.addItem(f"{self.result} {translation_text['text_kbits']}")

            self.ltext_video_size.clear()
            self.ltext_video_duration.clear()


    def event_show_settings(self):  
        path = 'lang/'
        files = os.listdir(path)

        def event_submit():
            new_language = {'language': ''}

            for i, (language, language_code) in enumerate(lang_list.items()):
                if self.combobox_language.currentText() == language:
                    new_language['language'] = language_code

            with open("configs/settings.json", "w") as f:
                json.dump(new_language, f)

            self.msg_submit = QMessageBox(self)
            self.msg_submit.setWindowTitle(translation_text["text_notify"])
            self.msg_submit.setText(translation_text['text_msg_submit_desc'])
            self.msg_submit.setIcon(QtWidgets.QMessageBox.Icon(QMessageBox.Information))
            self.msg_submit.exec()

            if self.msg_submit:
                self.window_settings.close()
                sys.exit() 

        self.window_settings = QDialog(self)

        self.window_settings.setFixedSize(512, 264)
        self.window_settings.setWindowTitle("Налаштування")

        self.label_language = QLabel(self.window_settings)
        self.label_language.setText(translation_text["text_language"])
        self.label_language.setFixedWidth(self.label_language.sizeHint().width())
        self.label_language.move(10, 20)

        self.combobox_language = QComboBox(self.window_settings)
        self.combobox_language.setFixedSize(512-20-self.label_language.sizeHint().width()-20, 20)
        self.combobox_language.move(20+self.label_language.sizeHint().width()+10, 20)

        for i, (language, language_code) in enumerate(lang_list.items()):
            for file in files:
                filename, extension = os.path.splitext(file)

                if filename == language_code:
                    self.combobox_language.addItem(language)
                    
                    if language_code == settings['language']:
                        index = self.combobox_language.findText(language)
                        self.combobox_language.setCurrentIndex(index)

        self.language_index = self.combobox_language.findText(language)

        self.button_submit = QPushButton(self.window_settings)
        self.button_submit.setText("OK")
        self.button_submit.setFixedSize(120, 25)
        self.button_submit.move(382, 229)
        self.button_submit.clicked.connect(event_submit)

        self.window_settings.exec()


    # Подія показу інформації про програму
    def event_show_info(self):
        with open("LICENSE", encoding="utf-8") as l:
            license_desc = l.read()

        self.window_info = QDialog(self)
        self.window_info.setWindowTitle(translation_text["text_title_info"])
        self.window_info.setFixedSize(600, 300)

        # Шрифт для заголовку
        self.font_title = QFont()
        self.font_title.setPointSize(16)

        # Створення мітки-заголовка
        self.label_version = QLabel(self.window_info)
        self.label_version.setText("PySide Bitrate Calculator 2023.5.1")
        self.label_version.setFont(self.font_title)
        self.label_version.setFixedSize(self.label_version.sizeHint().width(), self.label_version.sizeHint().height())
        self.label_version.move(10, 10)

        # Створення групи з віджетів
        self.tabwidget = QTabWidget(self.window_info)
        self.tabwidget.setFixedSize(580, 240)
        self.tabwidget.move(10, 50)

        # Створення віджета "Про програму"
        self.tab_about = QWidget()

        # Створення мітки опису програми
        self.label_tab_about_desc = QLabel(self.tab_about)
        self.label_tab_about_desc.setText(translation_text["text_desc_about"])
        self.label_tab_about_desc.setWordWrap(True)
        self.label_tab_about_desc.setFixedWidth(550)
        self.label_tab_about_desc.move(10, 10)
        
        # Створення мітки посилання на GitHub
        self.label_link = QLabel(self.tab_about)
        self.label_link.setText(f'{translation_text["text_desc_github"]} <a href="https://github.com/AoHeaven/PySide-Bitrate-Calculator">https://github.com/AoHeaven/PySide-Bitrate-Calculator</a>')
        self.label_link.setWordWrap(True)
        self.label_link.setFixedSize(550, self.label_link.sizeHint().height())
        self.label_link.move(10, self.label_tab_about_desc.sizeHint().height()+10)
    
        # Створення мітки про авторське право
        self.label_copyright = QLabel(self.tab_about)
        self.label_copyright.setText("Copyright © 2023 Ivan Sakhno (AoHeaven).")
        self.label_copyright.setWordWrap(True)
        self.label_copyright.setFixedSize(550, self.label_copyright.sizeHint().height())
        self.label_copyright.move(10, self.label_tab_about_desc.sizeHint().height()+self.label_link.sizeHint().height()-10)

        # Створення віджета "Ліцензія"
        self.tab_license = QWidget()

        # Створення текстового поля з текстом ліцензії
        self.text_license = QTextEdit(self.tab_license)
        self.text_license.setText(license_desc)
        self.text_license.setFixedSize(574, 211)
        self.text_license.setReadOnly(True)
        self.text_license.move(0, 0)


        # Створення віджета "Використовувані бібліотеки"
        self.tab_used_libraries = QWidget()

        # Створення мітки до віджета вище
        self.label_used_libraries = QLabel(self.tab_used_libraries)
        self.label_used_libraries.setText(translation_text["text_used_libraries"])
        self.label_used_libraries.setFixedWidth(self.label_used_libraries.sizeHint().width())
        self.label_used_libraries.move(10, 10)

        # PySide6
        self.label_used_libraries_pyside = QLabel(self.tab_used_libraries)
        self.label_used_libraries_pyside.setText(f'{translation_text["text_used_libraries_pyside"]} 6.5.0')
        self.label_used_libraries_pyside.setFixedWidth(self.label_used_libraries.sizeHint().width())
        self.label_used_libraries_pyside.move(10, self.label_used_libraries.sizeHint().height()+20)

        # OpenCV-Python
        self.label_used_libraries_opencv = QLabel(self.tab_used_libraries)
        self.label_used_libraries_opencv.setText(f'{translation_text["text_used_libraries_opencv"]} 4.7.0.72')
        self.label_used_libraries_opencv.setFixedWidth(self.label_used_libraries.sizeHint().width())
        self.label_used_libraries_opencv.move(10, self.label_used_libraries.sizeHint().height()+self.label_used_libraries_pyside.sizeHint().height()+30)

        # Py2exe
        self.label_used_libraries_autopytoexe = QLabel(self.tab_used_libraries)
        self.label_used_libraries_autopytoexe.setText(f'{translation_text["text_used_libraries_autopytoexe"]} 2.34.0')
        self.label_used_libraries_autopytoexe.setFixedWidth(self.label_used_libraries.sizeHint().width())
        self.label_used_libraries_autopytoexe.move(10, self.label_used_libraries.sizeHint().height()+self.label_used_libraries_pyside.sizeHint().height()+self.label_used_libraries_opencv.sizeHint().height()+40)


        self.tabwidget.addTab(self.tab_about, translation_text["text_title_about"])
        self.tabwidget.addTab(self.tab_license, translation_text["text_title_license"])
        self.tabwidget.addTab(self.tab_used_libraries, translation_text["text_title_used_libraries"])

        self.window_info.exec()


app = QApplication(sys.argv)

window_main = BitrateCalculator()
window_main.show()

app.exec()