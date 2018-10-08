import wx

import matplotlib
matplotlib.interactive(True)
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure

'''
変調度 [%]
バイアス点 [%]
ディザ量 [%]
'''

def slider_value_change(event):
    obj = event.GetEventObject()
    frame.SetStatusText('Slider value change')
    line.set_data([1, 2, 3], [i + obj.GetValue() / 50.0 for i in [1, 2, 0]])
    canvas.draw()

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
# slider_2.Bind(wx.EVT_SLIDER, slider_value_change)
# パイロット
slider_3 = wx.Slider(panel, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
slider_3.SetMin(0)
slider_3.SetMax(100)
slider_3.SetValue(5)
# slider_3.Bind(wx.EVT_SLIDER, slider_value_change)

# プロット領域作成
fig = Figure()
axs = fig.add_subplot(111)
line, = axs.plot([], [])
axs.set_xlim((1, 3))
axs.set_ylim((0, 4))
# fig.tight_layout() ## tight_layout : falling back to Agg renderer
line.set_data([1, 2, 3], [2, 3, 1])
canvas = FigureCanvasWxAgg(panel, wx.ID_ANY, fig)

layout_1 = wx.GridSizer(4, 2, 4, 2)

layout_1.Add(stext_1, flag=wx.GROW)
layout_1.Add(slider_1, flag=wx.GROW)
layout_1.Add(stext_2, flag=wx.GROW)
layout_1.Add(slider_2, flag=wx.GROW)
layout_1.Add(stext_3, flag=wx.GROW)
layout_1.Add(slider_3, flag=wx.GROW)
layout_1.Add(canvas, flag=wx.GROW)

panel.SetSizer(layout_1)

frame.Show()
application.MainLoop()

