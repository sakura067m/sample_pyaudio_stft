import sys

import numpy as np

from PyQt5.QtWidgets import QApplication
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis

app = QApplication(sys.argv)
chart = QChart()
b_set = QBarSet("test")
series = QBarSeries()
b_set.append(np.arange(5, dtype=np.float64))
series.append(b_set)
chart.addSeries(series)
chart.createDefaultAxes()
chart.setAnimationOptions(QChart.SeriesAnimations);

axisX = QBarCategoryAxis()
axisX.append((*"12345",))

chart.setAxisX(axisX, series)

chartView = QChartView(chart)
##chartView.setRenderHint(QPainter.Antialiasing)

chartView.show()
app.exec_()
