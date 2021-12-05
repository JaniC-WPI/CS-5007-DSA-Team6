from tkinter import *

class ScrolledWindow(Frame):
    """
    1. Master widget gets scrollbars and a canvas. Scrollbars are connected
    to canvas scrollregion.

    2. self.scrollwindow is created and inserted into canvas

    Usage Guideline:
    Assign any widgets as children of <ScrolledWindow instance>.scrollwindow
    to get them inserted into canvas

    __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs)
    docstring:
    Parent = master of scrolled window
    canv_w - width of canvas
    canv_h - height of canvas

    """


    def __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas

       """
        super().__init__(parent, *args, **kwargs)

        self.__parent = parent

        # creating a canvas
        self.__canv = Canvas(self.__parent)
        # placing a canvas into frame
        self.__canv.pack(side=LEFT, fill=Y)
        # creating a scrollbars
        self.__yscrlbr = Scrollbar(self.__parent, orient="vertical", command=self.__canv.yview)
        self.__yscrlbr.pack(side=RIGHT, fill=Y)
        self.__canv.config(yscrollcommand=self.__yscrlbr.set)

        # creating a frame in canvas
        self.scrollwindow = Frame(self.__parent)
        self.__canv.create_window((0, 0), window=self.scrollwindow, anchor='nw')

        #self.__yscrlbr.lift(self.scrollwindow)
        self.scrollwindow.bind('<Configure>', self._configure_window)
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.__canv.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.__canv.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.__canv.yview_scroll(int(-1*(event.delta/120)), "units")

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        self.__canv.config(scrollregion='0 0 %s %s' % size)
        if self.scrollwindow.winfo_reqwidth() != self.__canv.winfo_width():
            # update the __canvas's width to fit the inner frame
            self.__canv.config(width=self.scrollwindow.winfo_reqwidth())
        if self.scrollwindow.winfo_reqheight() != self.__canv.winfo_height():
            # update the canvas's width to fit the inner frame
            self.__canv.config(height=self.scrollwindow.winfo_reqheight())
