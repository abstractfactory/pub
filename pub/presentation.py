from pub.widget import Pub


def main(port=None):
    import pigui.pyqt5.util
    with pigui.pyqt5.util.application_context():

        win = Pub(port)
        win.resize(*(300, 400))
        win.animated_show()


if __name__ == '__main__':
    import pifou
    pifou.setup_log()
    pifou.setup_log('pub')

    main(port=None)
