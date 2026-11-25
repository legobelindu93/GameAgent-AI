"""Experimental Win32 host for explicitly launched native application windows."""
import sys

class WindowHost:
    def __init__(self,container):
        self.container=container
        self.window=None
        self.saved=None
        self.container.bind("<Configure>",self.resize,add="+")
    def _api(self):
        if sys.platform!="win32":raise RuntimeError("Windows only")
        import win32gui,win32con,win32process
        return win32gui,win32con,win32process
    def candidates(self,pid):
        g,c,p=self._api()
        found=[]
        def visit(hwnd,_):
            if p.GetWindowThreadProcessId(hwnd)[1]==pid and g.IsWindowVisible(hwnd) and not g.GetWindow(hwnd,c.GW_OWNER):
                title=g.GetWindowText(hwnd)
                if title:found.append((hwnd,title))
            return True
        g.EnumWindows(visit,None)
        return found
    def attach(self,hwnd,pid):
        g,c,p=self._api()
        if not g.IsWindow(hwnd) or p.GetWindowThreadProcessId(hwnd)[1]!=pid:raise ValueError("Window is not owned by selected process")
        self.detach()
        self.container.update_idletasks()
        style=g.GetWindowLong(hwnd,c.GWL_STYLE)
        parent=g.GetParent(hwnd)
        rect=g.GetWindowRect(hwnd)
        self.saved=(parent,style,rect)
        self.window=hwnd
        try:
            g.SetWindowLong(hwnd,c.GWL_STYLE,(style & ~(c.WS_POPUP|c.WS_CAPTION|c.WS_THICKFRAME))|c.WS_CHILD)
            g.SetParent(hwnd,self.container.winfo_id())
            if g.GetParent(hwnd)!=self.container.winfo_id():raise RuntimeError("Windows rejected embedding")
            g.SetWindowPos(hwnd,0,0,0,1,1,c.SWP_NOZORDER|c.SWP_NOACTIVATE|c.SWP_FRAMECHANGED)
            self.resize()
        except Exception:
            self.detach()
            raise
    def resize(self,event=None):
        if self.window is None:return
        g,c,p=self._api()
        if not g.IsWindow(self.window):
            self.window=None;self.saved=None;return
        g.MoveWindow(self.window,0,0,max(1,self.container.winfo_width()),max(1,self.container.winfo_height()),True)
    def detach(self):
        if self.window is None:return
        g,c,p=self._api()
        hwnd=self.window
        parent,style,(x,y,r,b)=self.saved
        if g.IsWindow(hwnd):
            g.SetParent(hwnd,parent)
            g.SetWindowLong(hwnd,c.GWL_STYLE,style)
            g.SetWindowPos(hwnd,0,x,y,r-x,b-y,c.SWP_NOZORDER|c.SWP_NOACTIVATE|c.SWP_FRAMECHANGED)
        self.window=None;self.saved=None
