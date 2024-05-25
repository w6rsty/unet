import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.font_manager import FontProperties
from functools import cmp_to_key
import matplotlib

matplotlib.rc("font", family='Microsoft YaHei')

font_title = FontProperties(size=20, weight=600)
font1 = FontProperties(size=14, weight=600)
font2 = FontProperties(size=12, weight=600)

class TimeSeriesAnimationChart:
    def __init__(self, root, datasets, val, time, name, bar_display_num=10, title=''):
        self.root = root
        self.root.title("数据展示工具")

        # 在 TimeSeriesAnimationChart 类中的 __init__ 方法中添加一个新的属性用于存储已走过的进度条颜色
        self.progress_bar_color = "blue"

        self.datasets = datasets
        self.val = val
        self.time = time
        self.name = name
        self.colors = None
        self.bar_display_num = bar_display_num
        self.title = title
        self.current_frame = 0

        self.fig, self.ax = plt.subplots(figsize=(15, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=600, variable=self.progress_var, command=self.on_progress_bar_changed)
        self.progress_bar.pack(fill=tk.X, expand=True, padx=10, pady=20)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)

        # 创建一个新的框架用于包含按钮
        self.button_frame = tk.Frame(self.control_frame)
        self.button_frame.pack(side=tk.BOTTOM, pady=10)  # 设置按钮框架的位置

        # 调整按钮的大小
        button_width = 15
        button_height = 2

        self.start_button = tk.Button(self.button_frame, text="开始", command=self.start_animation, width=button_width, height=button_height)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.button_frame, text="暂停", command=self.pause_animation, width=button_width, height=button_height)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.frames = []
        self.animator = None

        self.progress_bar_color = "blue"  # 新增属性，用于存储已走过的进度条颜色

    def on_progress_bar_changed(self, value):
        if self.animator:
            if self.animator.event_source:
                self.animator.event_source.stop()
        frame_index = int(float(value) / 100 * (len(self.frames) - 1))
        if not hasattr(self, 'updating') or not self.updating:
            self.updating = True
            self.update_chart_for_frame_index(frame_index)
            self.updating = False
        

    def update_chart_for_frame_index(self, frame_index):
        if frame_index >= 0 and frame_index < len(self.frames):
            self.current_frame = self.frames[frame_index]
            self._draw_bar_chart(self.current_frame)
            self.canvas.draw()

    def start_animation(self):
        if not self.animator:
            self.create_animation()
        self.animator.event_source.start()

    def pause_animation(self):
        if self.animator:
            self.animator.event_source.stop()

    def create_animation(self, interval=200, repeat=False, cmp=None, reverse=False):
        if self._check_dataset():
            print("文件检查错误")
            return

        self.colors = self._load_colors()
        self._make_frame(cmp, reverse)

        def update(frame):
            self._draw_bar_chart(frame)
            progress_value = self.frames.index(frame) / len(self.frames) * 100
            self.progress_var.set(progress_value)

        self.animator = animation.FuncAnimation(self.fig, update, frames=self.frames, interval=interval, repeat=repeat)

    def _load_colors(self):
        custom_colors = {
            '中国': '#1f77b4',
            '美国': '#ff7f0e',
            '印度': '#2ca02c',
        }
        name_list = list(set(self.datasets[self.name].values))
        color_list = [custom_colors.get(name, '#d62728') for name in name_list]
        return dict(zip(name_list, color_list))

    def _check_dataset(self):
        assert isinstance(self.datasets, pd.DataFrame)
        columns = [self.val, self.time, self.name]
        try:
            df = self.datasets[columns]
        except KeyError:
            print("索引错误")
            return -1

        for col in columns:
            if df[col].isnull().sum() != 0:
                print('{} 有空值!'.format(col))
                return -1

        if isinstance(self.datasets[self.val][0], str):
            self.datasets[self.val] = self.datasets[self.val].apply(lambda x: eval(x.replace(',', '')))

        return 0

    def _make_frame(self, cmp=None, reverse=False):
        times = list(set(self.datasets[self.time].values))
        if cmp is not None:
            cmp = cmp_to_key(cmp)
        times.sort(key=cmp, reverse=reverse)
        self.frames = times

    def _draw_bar_chart(self, k):
        dff = self.datasets[self.datasets[self.time].eq(k)].sort_values(by=self.val, ascending=True).tail(self.bar_display_num)
        self.ax.clear()
        self.ax.barh(dff[self.name], dff[self.val], color=[self.colors[x] for x in dff[self.name]])

        dx = 0.01
        for i, (value, name) in enumerate(zip(dff[self.val], dff[self.name])):
            self.ax.text(value * (1 - dx), i, name, size=14, weight=600, color='#242424', ha='right', va='bottom', fontproperties=font1)
            self.ax.text(value * (1 + dx), i, f'{value:,.0f}', size=14, ha='left', va='center')
        self.ax.text(1, 0.25, k, transform=self.ax.transAxes, color='#777777', size=46, ha='right', weight=800)
        self.ax.text(0, 1.05, "{}".format(self.val), transform=self.ax.transAxes, size=12, color='#777777')
        self.ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        self.ax.xaxis.set_ticks_position('top')
        self.ax.tick_params(axis='x', colors='#777777', labelsize=12)
        self.ax.set_yticks([])
        self.ax.margins(0, 0.01)
        self.ax.grid(which='major', axis='x', linestyle='-')
        self.ax.set_axisbelow(True)
        self.ax.text(0, 1.10, '{}-{}'.format(self.frames[0], self.frames[-1]), transform=self.ax.transAxes, size=24, weight=600, ha='left')

        plt.box(False)
        plt.title('{}'.format(self.title), fontproperties=font_title, color='#777777')

def main():
    file_path = '近年糖尿病患病人口.csv'
    bar_display_num = 10
    datasets = pd.read_csv(file_path)
    root = tk.Tk()
    my_app = TimeSeriesAnimationChart(root, datasets, 'val', 'year', 'country', bar_display_num, "1959-2018年世界各国糖尿病人口变化")
    my_app.create_animation()

    root.mainloop()



if __name__ == "__main__":
    main()
