#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.1 on Sun Apr 25 12:39:10 2021
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
        self.SetSize((400, 300))
        self.SetTitle("frame")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        self.button_connect = wx.Button(self.panel_1, wx.ID_ANY, "Connect")
        self.button_connect.SetMinSize((100, 53))
        sizer_2.Add(self.button_connect, 0, wx.EXPAND, 0)

        label_10 = wx.StaticText(self.panel_1, wx.ID_ANY, "disconnect", style=wx.ALIGN_CENTER_HORIZONTAL)
        sizer_2.Add(label_10, 1, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

        label_6 = wx.StaticText(self.panel_1, wx.ID_ANY, "IP Address", style=wx.ALIGN_CENTER_HORIZONTAL)
        label_6.SetMinSize((100, 20))
        sizer_3.Add(label_6, 0, wx.EXPAND, 0)

        self.text_ctrl_4 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_3.Add(self.text_ctrl_4, 1, wx.EXPAND, 0)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)

        label_7 = wx.StaticText(self.panel_1, wx.ID_ANY, "port", style=wx.ALIGN_CENTER_HORIZONTAL)
        label_7.SetMinSize((100, 20))
        sizer_4.Add(label_7, 0, wx.EXPAND, 0)

        self.text_ctrl_5 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_4.Add(self.text_ctrl_5, 1, wx.EXPAND, 0)

        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)

        label_8 = wx.StaticText(self.panel_1, wx.ID_ANY, "user", style=wx.ALIGN_CENTER_HORIZONTAL)
        label_8.SetMinSize((100, 20))
        sizer_5.Add(label_8, 0, wx.EXPAND, 0)

        self.text_ctrl_6 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_5.Add(self.text_ctrl_6, 1, wx.EXPAND, 0)

        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)

        label_9 = wx.StaticText(self.panel_1, wx.ID_ANY, "passwd", style=wx.ALIGN_CENTER_HORIZONTAL)
        label_9.SetMinSize((100, 20))
        sizer_6.Add(label_9, 0, wx.EXPAND, 0)

        self.text_ctrl_7 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_6.Add(self.text_ctrl_7, 1, wx.EXPAND, 0)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        # end wxGlade

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
