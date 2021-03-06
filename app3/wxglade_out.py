#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.1 on Fri Sep 21 22:52:26 2018
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((578, 445))
        
        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end
        
        # Tool Bar
        self.frame_toolbar = wx.ToolBar(self, -1)
        self.SetToolBar(self.frame_toolbar)
        # Tool Bar end
        self.button_1 = wx.Button(self, wx.ID_ANY, "button_1")
        self.button_2 = wx.Button(self, wx.ID_ANY, "button_2")
        self.button_3 = wx.Button(self, wx.ID_ANY, "button_3")
        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.combo_box_1 = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.spin_ctrl_1 = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=100)
        self.button_4 = wx.ToggleButton(self, wx.ID_ANY, "")
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        self.button_1.Bind(wx.EVT_BUTTON,self.hello)

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame")
        self.frame_toolbar.Realize()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        grid_sizer_1 = wx.GridSizer(0, 3, 0, 0)
        grid_sizer_1.Add(self.button_1, 0, 0, 0)
        grid_sizer_1.Add(self.button_2, 0, 0, 0)
        grid_sizer_1.Add(self.button_3, 0, 0, 0)
        grid_sizer_1.Add(self.text_ctrl_1, 0, 0, 0)
        grid_sizer_1.Add(self.combo_box_1, 0, 0, 0)
        grid_sizer_1.Add(self.spin_ctrl_1, 0, 0, 0)
        grid_sizer_1.Add(self.button_4, 0, 0, 0)
        self.notebook_1.AddPage(self.notebook_1_pane_1, "notebook_1_pane_1")
        grid_sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        grid_sizer_1.Add((160, 119), 0, 0, 0)
        self.SetSizer(grid_sizer_1)
        self.Layout()
        # end wxGlade

    def hello(self,event):
        print('hello world')
        self.button_1.SetLabel('Ouch!')

# end of class MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
