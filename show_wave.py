import serial
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

ser = serial.Serial('COM4', 115200, timeout=1)

HISTORY_LEN = 50000   # 历史缓存长度，越大能看越长时间
DISPLAY_LEN = 2000    # 默认显示窗口长度
fs = 10000            # 采样率Hz

app = QtWidgets.QApplication([])
main_widget = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout(main_widget)
win = pg.GraphicsLayoutWidget(title="STM32示波器（完全版）")
plot = win.addPlot(title="实时波形")
curve = plot.plot()
plot.setLabel('bottom', 'Time', units='ms')
layout.addWidget(win)

history_buffer = [0] * HISTORY_LEN
paused = False
display_start = HISTORY_LEN - DISPLAY_LEN # 当前显示窗口起点

# 暂停/恢复按钮
pause_btn = QtWidgets.QPushButton("暂停")
def pause_resume():
    global paused
    paused = not paused
    pause_btn.setText("恢复" if paused else "暂停")
pause_btn.clicked.connect(pause_resume)
layout.addWidget(pause_btn)

# 滑块用于浏览历史数据
slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
slider.setMinimum(0)
slider.setMaximum(HISTORY_LEN - DISPLAY_LEN)
slider.setValue(display_start)
def slider_changed(value):
    global display_start
    display_start = value
slider.valueChanged.connect(slider_changed)
layout.addWidget(slider)

# 缩放按钮区
hbox = QtWidgets.QHBoxLayout()
x_zoom_in = QtWidgets.QPushButton("X放大")
x_zoom_out = QtWidgets.QPushButton("X缩小")
y_zoom_in = QtWidgets.QPushButton("Y放大")
y_zoom_out = QtWidgets.QPushButton("Y缩小")
hbox.addWidget(x_zoom_in)
hbox.addWidget(x_zoom_out)
hbox.addWidget(y_zoom_in)
hbox.addWidget(y_zoom_out)
layout.addLayout(hbox)

def x_zoom_in_func():
    global DISPLAY_LEN, display_start
    DISPLAY_LEN = max(100, int(DISPLAY_LEN*0.8))
    display_start = max(0, HISTORY_LEN - DISPLAY_LEN)
    slider.setMaximum(HISTORY_LEN - DISPLAY_LEN)
    slider.setValue(display_start)
def x_zoom_out_func():
    global DISPLAY_LEN, display_start
    DISPLAY_LEN = min(HISTORY_LEN, int(DISPLAY_LEN*1.25))
    display_start = max(0, HISTORY_LEN - DISPLAY_LEN)
    slider.setMaximum(HISTORY_LEN - DISPLAY_LEN)
    slider.setValue(display_start)
def y_zoom_in_func():
    plot.getViewBox().scaleBy((1, 0.8))
def y_zoom_out_func():
    plot.getViewBox().scaleBy((1, 1.25))

x_zoom_in.clicked.connect(x_zoom_in_func)
x_zoom_out.clicked.connect(x_zoom_out_func)
y_zoom_in.clicked.connect(y_zoom_in_func)
y_zoom_out.clicked.connect(y_zoom_out_func)

main_widget.setWindowTitle("STM32实时示波器（完全版）")
main_widget.show()

def update():
    global history_buffer, display_start
    if not paused:
        while ser.in_waiting:
            s = ser.readline().decode('latin1').strip()
            if s.isdigit():
                history_buffer = history_buffer[1:] + [int(s)]
        # 自动滚动到最新
        display_start = HISTORY_LEN - DISPLAY_LEN
        slider.setValue(display_start)
    # 显示当前窗口数据
    t = [i * 1000 / fs for i in range(DISPLAY_LEN)]
    curve.setData(t, history_buffer[display_start:display_start+DISPLAY_LEN])

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

app.exec_()