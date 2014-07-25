from __future__ import absolute_import

# pigui library
import pigui
import pigui.style
import pigui.pyqt5.widgets.application.widget

# pifou dependencies
from PyQt5 import QtWidgets

import zmq

pigui.style.register('pub')


class Pub(pigui.pyqt5.widgets.application.widget.ApplicationBase):
    def __init__(self, port=None, parent=None):
        super(Pub, self).__init__(parent)
        self.setWindowTitle("Pub")

        body = QtWidgets.QWidget()

        context = zmq.Context.instance()
        self.insocket = context.socket(zmq.PUSH)

        if port:
            endpoint = "tcp://127.0.0.1:{}".format(port)
            self.insocket.connect(endpoint)
            self.notify("Connecting to {}".format(endpoint))

        comment_box = QtWidgets.QPlainTextEdit()
        comment_box.setPlaceholderText("Comment..")
        accept_button = QtWidgets.QPushButton('Publish')
        accept_button.pressed.connect(self.publish)
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.pressed.connect(self.animated_close)

        for widget_, name_ in {body: 'Body',
                               accept_button: 'AcceptButton',
                               cancel_button: 'CancepButton',
                               comment_box: 'CommentBox'}.iteritems():
            widget_.setObjectName(name_)

        l = QtWidgets.QVBoxLayout(body)
        l.addWidget(comment_box)
        l.addWidget(accept_button)
        l.addWidget(cancel_button)

        self.set_widget(body)

        comment_box.setFocus(True)

        self.port = port

    def publish(self):
        if not self.port:
            return self.notify("Not connected to any host")

        comment = self.findChild(QtWidgets.QWidget, 'CommentBox').toPlainText()

        msg = {'type': 'command',
               'command': 'publish',
               'payload': comment}

        self.insocket.send_json(msg)

        self.animated_close()


if __name__ == '__main__':
    pigui.setup_log()

    import pigui.pyqt5.util
    with pigui.pyqt5.util.application_context():

        win = Pub()
        win.resize(*(300, 400))
        win.animated_show()
