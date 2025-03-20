import pyqtgraph as pg

class GraphWidget(pg.PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackground('w')
        self.getAxis('left').setPen(pg.mkPen(color='k'))
        self.getAxis('bottom').setPen(pg.mkPen(color='k'))
        self.getAxis('left').setTextPen(pg.mkPen(color='k'))
        self.getAxis('bottom').setTextPen(pg.mkPen(color='k'))
        self.showGrid(x=True, y=True, alpha=0.5)
        self.getViewBox().setBackgroundColor('w')