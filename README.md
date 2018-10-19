# Python training

## Matplotlib
### `plt.figure()`, `fig.add_subplot()`
```py
import matplotlib.pyplot as plt

fig = plt.figure()
axs = fig.add_subplot(111)
line, = axs.plot([], [])
line.set_data([1, 2, 3], [2, 3, 1])
fig.show()
```

### `plt.subplots()`
```py
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 2)
line.append(axs[0, 0].plot([], [])
line[0].set_data([1, 2, 3], [2, 3, 1])
fig.show()
```

### wxPythonに埋め込み
```py
import matplotlib
matplotlib.interactive(True)
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure

import wx

app = wx.App()
frame = wx.Frame(None, wx.ID_ANY, 'Test Frame')
panel = wx.Panel(frame, wx.ID_ANY, pos=(0, 0))
layout = wx.BoxSizer(wx.VERTICAL)

fig = plt.figure()
axs = fig.add_subplot(111)
line, = axs.plot([], [])

canvas = FigureCanvasWxAgg(panel, wx.ID_ANY, fig)
layout.Add(canvas, flag=wx.GROW)
panel.SetSizer(layout)

line.set_data([1, 2, 3], [2, 3, 1])
canvas.draw()

frame.Show()
app.MainLoop()
```

## wxPython

- [wxPython | Python-izm](https://www.python-izm.com/gui/wxpython/)
- [wxPython API Documentation - wxPython Phoenix 4.0.3 documentation](https://docs.wxpython.org/)
- [wxPython ~ Python Tutorial](http://www.java2s.com/Tutorial/Python/0380__wxPython/Catalog0380__wxPython.htm)

```py
import wx

app = wx.App()
frame = wx.Frame(None, wx.ID_ANY, 'Test Frame')
panel = wx.Panel(frame, wx.ID_ANY, pos=(0, 0))

stext = wx.StaticText(panel, wx.ID_ANY, 'Static Text')

layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(stext)

panel.SetSizer(layout)
frame.Show()
app.MainLoop()
```

```py
import wx
import wx.grid

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Grid",size=(640,480))
        grid = wx.grid.Grid(self)
        grid.CreateGrid(50,50)
        for row in range(20):
            for col in range(6):
                grid.SetCellValue(row, col,"cell (%d,%d)" % (row, col))

app = wx.App()
frame = TestFrame()
frame.Show()
app.MainLoop()
```

