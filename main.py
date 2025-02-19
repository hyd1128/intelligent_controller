import sys
import threading
from PyQt6 import QtWidgets

from window_pyqt.main import Window
from window_webview.main import Main
from qt_material import apply_stylesheet
from flask import Flask, send_from_directory

########################################################################
# 需要使用webview的时候才开启此项功能
#######################################################################
# server = Flask(__name__, static_folder="static")
#
#
# @server.route('/')
# def serve_index():
#     return send_from_directory(server.static_folder, 'index.html')
#
#
# @server.route('/<path:filename>')
# def serve_static(filename):
#     return send_from_directory(server.static_folder, filename)
#
#
# @server.route("/test")
# def test():
#     return "flask项目已启动"
#
#
# def server_():
#     server.run(
#         host="0.0.0.0",
#         port=8041,
#         debug=False
#     )
###########################################################################


if __name__ == "__main__":
    ##############################################################
    # webview实例化代码
    #####################
    # daemon_thread = threading.Thread(target=server_, daemon=True)
    # daemon_thread.start()
    # app = QtWidgets.QApplication(sys.argv)
    # # 暗色主题
    # # apply_stylesheet(app, theme='dark_teal.xml')
    # # 亮色主题
    # apply_stylesheet(app, theme='light_teal_500.xml', invert_secondary=True)
    #
    # window = Main()
    # window.show()
    # sys.exit(app.exec())
    ################################################################
    ################################################################
    # pyqt fluent widget实例化代码
    ############################
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
    ##################################################################

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
