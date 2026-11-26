"""Qt adapter for the existing experimental PID-scoped Win32 host."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame
from .window_host import WindowHost

class NativeSurface(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_NativeWindow,True)
        self.setMinimumHeight(260)
        self.setStyleSheet("background:#08090c;border:1px solid #262930;")
        self.on_resize=None
    def bind(self,event,callback,add=None):
        self.on_resize=callback
    def update_idletasks(self):
        self.winId()
    def winfo_id(self):
        return int(self.winId())
    def winfo_width(self):
        return round(self.width()*self.devicePixelRatioF())
    def winfo_height(self):
        return round(self.height()*self.devicePixelRatioF())
    def resizeEvent(self,event):
        super().resizeEvent(event)
        if self.on_resize:
            try:self.on_resize()
            except Exception:
                # The underlying host remains attached; allow explicit detach.
                pass

def make_host(parent=None):
    surface=NativeSurface(parent)
    return surface,WindowHost(surface)
