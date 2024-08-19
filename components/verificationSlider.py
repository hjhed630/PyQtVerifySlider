# coding: utf-8

from PyQt5.QtWidgets import (
    QSlider,
    QStyle,
    QStyleOptionSlider,
)
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal


class VerificationSlider(QSlider):

    numSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(VerificationSlider, self).__init__(Qt.Orientation.Horizontal, parent)

        self.setFixedSize(300, 40)
        self.setMouseTracking(True)

        self.isPressed = False
        self.isHover = False
        self.mouseMount = 0

        self.loadStyleSheet()

    def paintEvent(self, event):
        super(VerificationSlider, self).paintEvent(event)
        painter = QPainter(self)
        option = QStyleOptionSlider()

        self.initStyleOption(option)

        grooveRect = self.style().subControlRect(
            QStyle.ComplexControl.CC_Slider,
            option,
            QStyle.SubControl.SC_SliderGroove,
            self,
        )

        if not self.isPressed:
            font = QFont()
            font.setFamily("微软雅黑")
            font.setPointSize(10)
            painter.setFont(font)
            painter.setPen(QColor(0, 0, 0, 100))
            painter.drawText(
                grooveRect,
                Qt.AlignmentFlag.AlignCenter,
                self.tr("drag slider to fill puzzle"),
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.isPressed = True
        super(VerificationSlider, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.numSignal.emit(self.value())

            self.isPressed = False
            self.moveAnimation = QPropertyAnimation(self, b"sliderPosition")
            self.moveAnimation.setDuration(800)  # 设置动画持续时间
            self.moveAnimation.setStartValue(self.value())  # 设置动画开始的值
            self.moveAnimation.setEndValue(0)  # 设置动画结束的值
            self.moveAnimation.setLoopCount(1)  # 设置动画循环次数
            self.moveAnimation.setEasingCurve(QEasingCurve.Type.OutQuint)
            self.moveAnimation.start()
            if self.isHover:
                self.animation = QPropertyAnimation(self, b"")
                self.animation.setDuration(300)  # 动画持续时间3000毫秒
                self.animation.setStartValue(0)
                self.animation.setEndValue(100)
                self.animation.valueChanged.connect(
                    lambda x: self.updateHandleColor(
                        x, QColor(27, 145, 250), QColor(255, 255, 255)
                    )
                )
                self.animation.start()
                self.isHover = False

        super(VerificationSlider, self).mouseReleaseEvent(event)  # 调用父类的事件

    def mouseMoveEvent(self, event):
        if not self.isPressed:
            # 初始化滑块的样式选项
            option = QStyleOptionSlider()
            self.initStyleOption(option)

            # 获取handle的矩形区域
            handle_rect = self.style().subControlRect(
                QStyle.ComplexControl.CC_Slider,
                option,
                QStyle.SubControl.SC_SliderHandle,
                self,
            )

            if handle_rect.contains(event.pos()):
                self.isHover = True
                self.mouseMount += 1

                if self.isHover and self.mouseMount == 1:
                    self.hoverAnimation = QPropertyAnimation(self, b"")
                    self.hoverAnimation.setDuration(300)  # 动画持续时间3000毫秒
                    self.hoverAnimation.setStartValue(0)
                    self.hoverAnimation.setEndValue(100)
                    self.hoverAnimation.valueChanged.connect(
                        lambda x: self.updateHandleColor(
                            x, QColor(255, 255, 255), QColor(27, 145, 250)
                        )
                    )
                    self.hoverAnimation.start()
            else:

                self.mouseMount = 0
                if self.isHover:
                    self.animation = QPropertyAnimation(self, b"")
                    self.animation.setDuration(300)  # 动画持续时间3000毫秒
                    self.animation.setStartValue(0)
                    self.animation.setEndValue(100)
                    self.animation.valueChanged.connect(
                        lambda x: self.updateHandleColor(
                            x, QColor(27, 145, 250), QColor(255, 255, 255)
                        )
                    )
                    self.animation.start()
                    self.isHover = False

        super(VerificationSlider, self).mouseMoveEvent(event)

    @property
    def sliderPosition(self):
        return (
            self.style()
            .subControlRect(
                QStyle.CC_Slider,
                self.style().initStyleOption(self),
                QStyle.SC_SliderHandle,
                self,
            )
            .center()
            .x()
        )

    @sliderPosition.setter
    def sliderPosition(self, value):
        # 根据动画的值来设置滑块的位置
        self.setValue((int)(self.maximum() * value))

    def updateHandleColor(self, value, color1, color2):
        ratio = value / 100.0  # 动画进度
        start_color = color1
        end_color = color2

        r1, g1, b1, _ = start_color.getRgbF() 
        r2, g2, b2, _ = end_color.getRgbF()

        current_r = r1 + ratio * (r2 - r1)
        current_g = g1 + ratio * (g2 - g1)
        current_b = b1 + ratio * (b2 - b1)

        current_color = QColor()
        current_color.setRgbF(current_r, current_g, current_b)

        self.setStyleSheet(
            "QSlider::groove:horizontal {height:	35px;width: 290px;border: 1px solid #E4E7EB;background-color: rgb(247, 249, 250);border-radius: 3px;}"
            f"QSlider::handle:horizontal {{width: 35px;height: 35px;margin: -1px -1px;border-radius: 3px;border: 1px solid #C9CCCF;background-color: {current_color.name()};}}"
            "QSlider::handle:horizontal:pressed {width: 35px;height: 35px;margin: -1px -1px;border-radius: 3px;border: 1px solid #1991FA;background-color: #1991FA;}"
            "QSlider::sub-page:horizontal {border: 1px solid #1991FA;border-radius: 3px;background-color: #D1E9FE;height: 35px;}"
        )

    def loadStyleSheet(self):
        self.setStyleSheet(
            "QSlider::groove:horizontal {height:	35px;width: 290px;border: 1px solid #E4E7EB;background-color: rgb(247, 249, 250);border-radius: 3px;}"
            "QSlider::handle:horizontal {width: 35px;height: 35px;margin: -1px -1px;border-radius: 3px;border: 1px solid #C9CCCF;background-color: #ffffff;}"
            "QSlider::handle:horizontal:pressed {width: 35px;height: 35px;margin: -1px -1px;border-radius: 3px;border: 1px solid #1991FA;background-color: #1991FA;}"
            "QSlider::sub-page:horizontal {border: 1px solid #1991FA;border-radius: 3px;background-color: #D1E9FE;height: 35px;}"
        )
