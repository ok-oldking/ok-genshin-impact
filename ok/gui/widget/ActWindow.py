from PySide6.QtCore import Signal, QEvent
from PySide6.QtWidgets import QVBoxLayout
from qfluentwidgets import SplitTitleBar, LineEdit, PrimaryPushButton, BodyLabel

from ok import Logger
from ok import og
from ok.gui.Communicate import communicate
from ok.gui.util.Alert import alert_error
from ok.gui.widget.BaseWindow import BaseWindow

logger = Logger.get_logger(__name__)


class ActWindow(BaseWindow):
    result_event = Signal(bool, str)

    def __init__(self, icon=None, message=None):
        super().__init__()
        self.user_closed = True
        self.message = message

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        self.setWindowTitle(self.tr("软件激活"))

        if icon is not None:
            self.setWindowIcon(icon)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch()
        self.setLayout(self.vbox)
        self.vbox.setContentsMargins(40, 40, 40, 40)

        if self.message:
            self.message_label = BodyLabel(self.message)
            self.vbox.addWidget(self.message_label)

        self.key_input = LineEdit(self)
        self.vbox.addWidget(self.key_input)
        self.key_input.setPlaceholderText(self.tr("激活码"))
        self.key_input.setClearButtonEnabled(True)

        if og.config.get('auth').get('use_uid'):
            self.uid_input = LineEdit(self)
            self.uid_input.setPlaceholderText(self.tr("你的游戏编号, 如102630612345, 将会绑定此账号使用无法更改"))
            self.vbox.addWidget(self.uid_input)
        else:
            self.uid_input = None

        self.activate_btn = PrimaryPushButton(self.tr("激活"))
        self.vbox.addWidget(self.activate_btn)
        self.vbox.addStretch()

        if og.config.get('auth').get('trial'):
            self.trial_btn = PrimaryPushButton(self.tr("试用"))
            self.trial_btn.clicked.connect(self.trial)
            self.vbox.addWidget(self.trial_btn)
            self.vbox.addStretch()

        self.result_event.connect(self.on_result)
        self.activate_btn.clicked.connect(self.activate)

    def activate(self):
        if not self.key_input.text():
            alert_error(self.tr("请输入激活码!"))
            return

        if self.uid_input and not self.uid_input.text():
            alert_error(self.tr("请输入游戏编号!"))
            return

        og.handler.post(self.do_check_auth)
        self.show_loading()

    def trial(self):
        og.handler.post(self.do_trial)
        self.show_loading()

    def do_trial(self):
        success, result = og.app.trial()
        if success:
            self.result_event.emit(True, self.tr('验证成功!'))
        else:
            self.result_event.emit(False, self.tr(result))

    def on_result(self, success, message):
        logger.info(f'on_result: {success}, {message}')
        if success:
            self.user_closed = False
            self.close()
            og.app.do_show_main()
        else:
            alert_error(message)
        self.close_loading()

    def do_check_auth(self):
        uid = (self.uid_input and self.uid_input.text()) or "none"
        success, result = og.app.check_auth(self.key_input.text(), uid)
        if success:
            self.result_event.emit(True, self.tr('验证成功!'))
        else:
            self.result_event.emit(False, self.tr('验证失败!'))

    def closeEvent(self, event):
        logger.debug('closeEvent')
        if og.ok.exit_event.is_set():
            logger.info("Window closed exit_event.is_set")
            event.accept()
            return
        else:
            logger.info(f"Window closed exit_event.is not set, self.user_closed {self.user_closed}")
            if self.user_closed:
                og.ok.quit()
            event.accept()

    def showEvent(self, event):
        if event.type() == QEvent.Show:
            logger.info("MessageWindow has fully displayed")
            communicate.start_success.emit()
        super().showEvent(event)
