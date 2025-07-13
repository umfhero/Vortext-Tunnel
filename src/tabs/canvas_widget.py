"""
Canvas widget for real-time collaborative drawing.
Handles mouse events and drawing operations.
"""

import json
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor, QPixmap, QMouseEvent


class CanvasWidget(QWidget):
    """Interactive canvas for collaborative drawing."""
    
    # Signals
    drawing_data_sent = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = QColor(0, 0, 0)
        self.pen_width = 3
        
        # Create canvas pixmap
        self.canvas = QPixmap(800, 600)
        self.canvas.fill(Qt.GlobalColor.white)
        
        # Set widget properties
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)
        
    def paintEvent(self, event):
        """Paint the canvas."""
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.canvas)
        
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            
    def mouseMoveEvent(self, event):
        """Handle mouse move events."""
        if self.drawing and event.buttons() & Qt.MouseButton.LeftButton:
            self.draw_line(self.last_point, event.pos())
            self.last_point = event.pos()
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False
            
    def draw_line(self, start_point, end_point):
        """Draw a line on the canvas."""
        painter = QPainter(self.canvas)
        pen = QPen(self.pen_color, self.pen_width, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        painter.drawLine(start_point, end_point)
        
        # Send drawing data to peer
        drawing_data = {
            'type': 'draw_line',
            'start_x': start_point.x(),
            'start_y': start_point.y(),
            'end_x': end_point.x(),
            'end_y': end_point.y(),
            'color': self.pen_color.name(),
            'width': self.pen_width
        }
        self.drawing_data_sent.emit(drawing_data)
        
        # Update the widget
        self.update()
        
    def set_pen_color(self, color):
        """Set the pen color."""
        self.pen_color = color
        
    def set_pen_width(self, width):
        """Set the pen width."""
        self.pen_width = width
        
    def clear(self):
        """Clear the canvas."""
        self.canvas.fill(Qt.GlobalColor.white)
        self.update()
        
        # Send clear command to peer
        clear_data = {
            'type': 'clear_canvas'
        }
        self.drawing_data_sent.emit(clear_data)
        
    def receive_drawing_data(self, data):
        """Receive and apply drawing data from peer."""
        if data['type'] == 'draw_line':
            painter = QPainter(self.canvas)
            pen = QPen(QColor(data['color']), data['width'], Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.drawLine(
                data['start_x'], data['start_y'],
                data['end_x'], data['end_y']
            )
            self.update()
        elif data['type'] == 'clear_canvas':
            self.canvas.fill(Qt.GlobalColor.white)
            self.update() 