import wx

import matplotlib
matplotlib.use('WX')

import matplotlib.pyplot as plt

'''
変調度 [%]
バイアス点 [%]
ディザ量 [%]
'''

def slider_value_change(event):
    obj = event.GetEventObject()
    frame.SetStatusText('Slider value change')
    print(obj.GetValue())

application = wx.App()
 
frame = wx.Frame(None, wx.ID_ANY, 'テストフレーム', size=(800, 800))

frame.SetBackgroundColour('#FFFFFF')
frame.CreateStatusBar()
frame.SetStatusText('python-izm.com')

panel = wx.Panel(frame, wx.ID_ANY, pos=(0, 0))
panel.SetBackgroundColour('#EEEEFF')

stext_1 = wx.StaticText(panel, wx.ID_ANY, 'Mod. degree [%]')
stext_2 = wx.StaticText(panel, wx.ID_ANY, 'Bias point [%]')
stext_3 = wx.StaticText(panel, wx.ID_ANY, 'Pilot [%]')

# 変調度
slider_1 = wx.Slider(panel, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
slider_1.SetMin(0)
slider_1.SetMax(100)
slider_1.SetValue(30)
slider_1.Bind(wx.EVT_SLIDER, slider_value_change)
# slider_1.SetTickFreq(10) # 目盛が表示されないんだけど
# バイアス点
slider_2 = wx.Slider(panel, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
slider_2.SetMin(-100)
slider_2.SetMax(100)
slider_2.SetValue(0)
slider_2.Bind(wx.EVT_SLIDER, slider_value_change)
# パイロット
slider_3 = wx.Slider(panel, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
slider_3.SetMin(0)
slider_3.SetMax(100)
slider_3.SetValue(5)
slider_3.Bind(wx.EVT_SLIDER, slider_value_change)

layout_1 = wx.GridSizer(3, 2, 3, 2)

layout_1.Add(stext_1, flag=wx.GROW)
layout_1.Add(slider_1, flag=wx.GROW)
layout_1.Add(stext_2, flag=wx.GROW)
layout_1.Add(slider_2, flag=wx.GROW)
layout_1.Add(stext_3, flag=wx.GROW)
layout_1.Add(slider_3, flag=wx.GROW)

panel.SetSizer(layout_1)

frame.Show()
application.MainLoop()

