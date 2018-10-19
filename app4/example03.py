import numpy as np
import wx

import matplotlib
matplotlib.interactive(True)
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure

# -----------------------------------------------------------------------------
#  Frame
# -----------------------------------------------------------------------------

class SimFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, 'Mech-Zehnder Modulator Controller Simulator', size=(700, 800))
        self.CreateStatusBar()
        self.SetStatusText('python-izm.com')
        self.GetStatusBar().SetBackgroundColour(None)

        self.SetMenuBar(SimMenu())

        root_panel = wx.Panel(self, wx.ID_ANY)

        self.panel_1 = TitlePanel(root_panel)
        self.panel_2 = InputPanel(root_panel)
        self.panel_3 = OutputPanel(root_panel)

        root_layout = wx.BoxSizer(wx.VERTICAL)
        root_layout.Add(self.panel_1, 0, wx.GROW | wx.ALL, border=10)
        root_layout.Add(self.panel_2, 0, wx.GROW | wx.ALL, border=10)
        root_layout.Add(self.panel_3, 0, wx.GROW | wx.ALL, border=10)
        root_panel.SetSizer(root_layout)
        root_layout.Fit(root_panel)

        self.panel_1.slider_1.Bind(wx.EVT_SLIDER, self.replot)
        self.panel_1.slider_2.Bind(wx.EVT_SLIDER, self.replot)
        self.panel_1.slider_3.Bind(wx.EVT_SLIDER, self.replot)

    def replot(self, event=wx.EVT_SLIDER):
        mod_degree = self.panel_1.slider_1.GetValue() / 100.0
        bias_point = self.panel_1.slider_2.GetValue() / 100.0

        self.panel_2.replot(bias_point, mod_degree)

# -----------------------------------------------------------------------------
#  Menu bar
# -----------------------------------------------------------------------------
class SimMenu(wx.MenuBar):
    def __init__(self):
        super().__init__()
        menu_file = wx.Menu()
        menu_file.Append(wx.ID_ANY, '保存')
        menu_file.Append(wx.ID_ANY, '終了')
        menu_edit = wx.Menu()
        menu_edit.Append(wx.ID_ANY, 'コピー')
        menu_edit.Append(wx.ID_ANY, 'ペースト')
          
        self.Append(menu_file, 'ファイル')
        self.Append(menu_edit, '編集')

# -----------------------------------------------------------------------------
#  Panel 1 : Title and Control
# -----------------------------------------------------------------------------
class TitlePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        self.SetBackgroundColour('#FFFFEE')

        font_1 = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        font_2 = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        title_text = wx.StaticText(self, wx.ID_ANY, 'Mach-Zehnder Modulator Controller Simulator')
        title_text.SetFont(font_1)

        panel_controller = wx.Panel(self, wx.ID_ANY)

        stext_1 = wx.StaticText(panel_controller, wx.ID_ANY, '\nMod. degree [%]')
        stext_2 = wx.StaticText(panel_controller, wx.ID_ANY, '\nBias point [%]')
        stext_3 = wx.StaticText(panel_controller, wx.ID_ANY, '\nPilot [%]')
        stext_1.SetFont(font_2)
        stext_2.SetFont(font_2)
        stext_3.SetFont(font_2)

        self.slider_1 = wx.Slider(panel_controller, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_VALUE_LABEL)
        self.slider_1.SetMin(0)
        self.slider_1.SetMax(100)
        self.slider_1.SetValue(30)
        self.slider_2 = wx.Slider(panel_controller, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_VALUE_LABEL)
        self.slider_2.SetMin(-100)
        self.slider_2.SetMax(100)
        self.slider_2.SetValue(0)
        self.slider_3 = wx.Slider(panel_controller, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_VALUE_LABEL)
        self.slider_3.SetMin(0)
        self.slider_3.SetMax(100)
        self.slider_3.SetValue(5)

        layout_controller = wx.FlexGridSizer(rows=3, cols=2, gap=(0, 0))
        layout_controller.Add(stext_1, flag=wx.GROW)
        layout_controller.Add(self.slider_1, flag=wx.GROW)
        layout_controller.Add(stext_2, flag=wx.GROW)
        layout_controller.Add(self.slider_2, flag=wx.GROW)
        layout_controller.Add(stext_3, flag=wx.GROW)
        layout_controller.Add(self.slider_3, flag=wx.GROW)
        layout_controller.AddGrowableCol(1)

        panel_controller.SetSizer(layout_controller)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(title_text, flag=wx.GROW | wx.ALL, border=10)
        layout.Add(panel_controller, flag=wx.GROW | wx.ALL, border=10)
        self.SetSizer(layout)

# -----------------------------------------------------------------------------
#  Panel 2 : Input Waveform
# -----------------------------------------------------------------------------
class InputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        self.SetBackgroundColour('#EEEEFF')

        self.fig = Figure()

        self.axs = self.fig.add_subplot(1, 1, 1)
        self.axs.set_xlim((-np.pi, np.pi))
        self.axs.set_ylim((0, 1.1))

        self.line_2, = self.axs.plot([], [], color='black', linestyle='--', linewidth=0.5)
        self.line_3, = self.axs.plot([], [], color='blue', linestyle='-', linewidth=2.0)
        self.line_4, = self.axs.plot([], [], color='blue', linestyle='None', marker='o')

        self.canvas = FigureCanvasWxAgg(self, wx.ID_ANY, self.fig)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.canvas, flag=wx.GROW)
        self.SetSizer(layout)

        xp = np.arange(-np.pi, np.pi, 0.01)
        yp = 0.5 - 0.5*np.cos(xp)
        self.line_2.set_data(xp, yp)

    def replot(self, bias_point=0.0, mod_degree=0.3):
        xp = np.arange(np.pi * (bias_point - mod_degree), np.pi * (bias_point + mod_degree), 0.01)
        yp = 0.5 - 0.5*np.cos(xp)
        self.line_3.set_data(xp, yp)
        xp = np.array([np.pi * (bias_point - mod_degree), np.pi * (bias_point + mod_degree)])
        yp = 0.5 - 0.5*np.cos(xp)
        self.line_4.set_data(xp, yp)
        self.canvas.draw()

# -----------------------------------------------------------------------------
#  Panel 3 : Output Waveform
# -----------------------------------------------------------------------------
class OutputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        self.SetBackgroundColour('#FFEEEE')


if __name__ == '__main__':
    application = wx.App()
    frame = SimFrame()
    frame.Show()
    frame.replot()
    application.MainLoop()
