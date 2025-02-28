from PyQt5.QtCore import pyqtSignal

from boundary.Admin.UI.AdminMenu_Dialog_AddProfile import *
from controller.Admin.CreateProfileController import CreateProfileController
from PyQt5.QtWidgets import QMessageBox, QDialog


class DialogAddProfile(QDialog):

    # 为dialog窗口设置触发信号
    profileAdded = pyqtSignal()


    def __init__(self, parent=None):
        super(DialogAddProfile, self).__init__(parent)
        self.ui = Ui_Dialog_AddProfile()
        self.ui.setupUi(self)

        self.ui.PushButton_create.clicked.connect(self.profileCreate)

    # GUI窗口拖动
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获得鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)   # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
#todo 3 create profile
    def profileCreate(self):
        try:
            # 获取输入框和组合框中的值
            profileName = self.ui.LineEdit_profile.text()


            # 调用后端的 createUser 方法
            create_control = CreateProfileController()
            success = create_control.createProfile(profileName)

            if success:
                QMessageBox.information(self, 'Success', f"Successful create new profile")
                self.profileAdded.emit()
                self.accept()  # 关闭对话框
                return True
            else:
                QMessageBox.warning(self, "Error", "Could not create user.")
                return False
        except Exception as e:
            # 打印或记录异常信息
            print(f"Failed to create user: {e}")
            QMessageBox.warning(self, "Error", f"Failed to create user: {e}")
            # 返回 False
            return False