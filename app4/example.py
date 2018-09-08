import wx

application = wx.App()
 
frame = wx.Frame(None, wx.ID_ANY, 'テストフレーム', size=(800, 800))

frame.SetBackgroundColour('#FFFFFF')
frame.CreateStatusBar()
frame.SetStatusText('python-izm.com')

panel = wx.Panel(frame, wx.ID_ANY, pos=(0, 0))
panel.SetBackgroundColour('#FFEEEE')

button_1 = wx.Button(panel, wx.ID_ANY, 'ボタン１')
button_2 = wx.Button(panel, wx.ID_ANY, 'ボタン２')
button_3 = wx.Button(panel, wx.ID_ANY, 'ボタン３')
button_4 = wx.Button(panel, wx.ID_ANY, 'ボタン４')
button_5 = wx.Button(panel, wx.ID_ANY, 'ボタン５')

layout_1 = wx.BoxSizer(wx.VERTICAL)
box_1_2 = wx.StaticBox(panel, wx.ID_ANY, 'Label 1')
layout_1_1 = wx.BoxSizer(wx.HORIZONTAL)
layout_1_2 = wx.StaticBoxSizer(box_1_2, wx.VERTICAL)

layout_1.Add(layout_1_1, proportion=1)
layout_1.Add(layout_1_2, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

layout_1_1.Add(button_1, proportion=1)
layout_1_1.Add(button_2, proportion=1)
layout_1_1.Add(button_3, proportion=1)

layout_1_2.Add(button_4, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
layout_1_2.Add(button_5, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

panel.SetSizer(layout_1)

'''
button_1 = wx.Button(panel, wx.ID_ANY, 'ボタン１')
button_2 = wx.Button(panel, wx.ID_ANY, 'ボタン２')
button_3 = wx.Button(panel, wx.ID_ANY, 'ボタン３')

box=wx.StaticBox(panel, wx.ID_ANY, 'Label 1')
layout = wx.StaticBoxSizer(box, wx.HORIZONTAL)
# layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(button_1, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
layout.Add(button_2, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
layout.Add(button_3, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

panel.SetSizer(layout)
'''

frame.Show()
application.MainLoop()

