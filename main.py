from PyQt6 import QtWidgets
import sys
from window.main import Main
from qt_material import apply_stylesheet
from static_server.server import main as static_server
import threading


if __name__ == "__main__":
    daemon_thread = threading.Thread(target=static_server, daemon=True)
    daemon_thread.start()
    app = QtWidgets.QApplication(sys.argv)
    # 暗色主题
    # apply_stylesheet(app, theme='dark_teal.xml')
    # 亮色主题
    apply_stylesheet(app, theme='light_teal_500.xml', invert_secondary=True)
    window = Main()
    window.show()
    sys.exit(app.exec())

"""
主题选择:
dark_amber.xml
dark_blue.xml
dark_cyan.xml
dark_lightgreen.xml
dark_medical.xml
dark_pink.xml
dark_purple.xml
dark_red.xml
dark_teal.xml
dark_yellow.xml
light_amber.xml
light_blue.xml
light_blue_500.xml
light_cyan.xml
light_cyan_500.xml
light_lightgreen.xml
light_lightgreen_500.xml
light_orange.xml
light_pink.xml
light_pink_500.xml
light_purple.xml
light_purple_500.xml
light_red.xml
light_red_500.xml
light_teal.xml
light_teal_500.xml
light_yellow.xml
"""
