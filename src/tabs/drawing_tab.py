"""
Drawing tab for real-time collaborative drawing.
Provides a shared whiteboard where both users can draw simultaneously.
"""

import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSpinBox, QColorDialog, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor, QPixmap, QMouseEvent

from tabs.canvas_widget import CanvasWidget


class DrawingTab(QWidget):
    """Drawing tab with collaborative canvas and drawing tools."""
    
    # Signals
    drawing_data_received = pyqtSignal(dict)
    drawing_data_sent = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the drawing tab interface."""
        layout = QVBoxLayout(self)
        
        # Canvas (create first)
        self.canvas = CanvasWidget()
        self.canvas.drawing_data_sent.connect(self.on_drawing_data_sent)
        
        # Toolbar (create after canvas)
        self.create_toolbar(layout)
        
        # Add canvas to layout
        layout.addWidget(self.canvas)
        
    def create_toolbar(self, parent_layout):
        """Create the drawing toolbar."""
        toolbar = QFrame()
        toolbar.setFrameStyle(QFrame.Shape.StyledPanel)
        toolbar_layout = QHBoxLayout(toolbar)
        
        # Color picker
        color_label = QLabel("Color:")
        self.color_btn = QPushButton()
        self.color_btn.setFixedSize(30, 30)
        self.color_btn.clicked.connect(self.choose_color)
        self.current_color = QColor(0, 0, 0)
        self.update_color_button()
        
        # Brush size
        size_label = QLabel("Size:")
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(1, 50)
        self.size_spinbox.setValue(3)
        self.size_spinbox.valueChanged.connect(self.on_brush_size_changed)
        
        # Clear button
        self.clear_btn = QPushButton("Clear Canvas")
        self.clear_btn.clicked.connect(self.canvas.clear)
        
        # Add widgets to toolbar
        toolbar_layout.addWidget(color_label)
        toolbar_layout.addWidget(self.color_btn)
        toolbar_layout.addWidget(size_label)
        toolbar_layout.addWidget(self.size_spinbox)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.clear_btn)
        
        parent_layout.addWidget(toolbar)
        
    def choose_color(self):
        """Open color picker dialog."""
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            self.update_color_button()
            self.canvas.set_pen_color(color)
            
    def update_color_button(self):
        """Update the color button appearance."""
        self.color_btn.setStyleSheet(
            f"background-color: {self.current_color.name()}; border: 1px solid black;"
        )
        
    def on_brush_size_changed(self, size):
        """Handle brush size change."""
        self.canvas.set_pen_width(size)
        
    def on_drawing_data_sent(self, data):
        """Handle drawing data being sent to peer."""
        # Emit signal to network manager
        self.drawing_data_sent.emit(data)
        
    def receive_drawing_data(self, data):
        """Receive drawing data from peer."""
        self.canvas.receive_drawing_data(data) 