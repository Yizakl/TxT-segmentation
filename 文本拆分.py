import os
import chardet
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle

# 注册支持中文的字体（如 Microsoft YaHei）
LabelBase.register(name='Microsoft YaHei', fn_regular='C:/Windows/Fonts/msyh.ttc')

def detect_file_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def split_file(input_file, num_parts=2):
    """将文件拆分为指定份数"""
    try:
        # 检测编码并读取文件
        with open(input_file, 'rb') as f:
            encoding = detect_file_encoding(input_file)
            lines = f.read().decode(encoding).splitlines()
        total_lines = len(lines)

        if num_parts <= 0 or num_parts > total_lines:
            raise ValueError("拆分份数必须是正整数且不超过总行数！")

        # 创建 TXTCache 文件夹
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cache_dir = os.path.join(current_dir, "TXTCache")
        os.makedirs(cache_dir, exist_ok=True)

        # 获取文件名（无扩展名）
        file_name = os.path.splitext(os.path.basename(input_file))[0]

        # 拆分逻辑
        part_size = total_lines // num_parts
        remainder = total_lines % num_parts
        start = 0
        for i in range(num_parts):
            end = start + part_size + (1 if i < remainder else 0)
            output_file = os.path.join(cache_dir, f"{file_name}_part{i + 1}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines[start:end]) + "\n")
            start = end

        return cache_dir, num_parts
    except Exception as e:
        raise RuntimeError(f"拆分失败: {str(e)}")


class FileSplitterApp(App):

    def build(self):
        self.title = "文件拆分工具"

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # 使用 Microsoft YaHei 字体和黑色字体颜色
        self.label = Label(text="请选择要拆分的文件", font_size='20sp', font_name='Microsoft YaHei', color=(0, 0, 0, 1))  # 黑色字体
        self.layout.add_widget(self.label)

        # 添加文件选择器，允许选择所有文件
        self.file_chooser = FileChooserIconView(filters=['*.*'])  # 显示所有文件
        self.layout.add_widget(self.file_chooser)

        # 添加拆分份数输入框
        self.split_input = TextInput(hint_text="请输入拆分份数", multiline=False, size_hint_y=None, height=30, font_name='Microsoft YaHei', foreground_color=(0, 0, 0, 1))  # 黑色字体
        self.layout.add_widget(self.split_input)

        # 添加拆分按钮
        self.split_button = Button(text="拆分文件", size_hint_y=None, height=50, font_name='Microsoft YaHei', color=(0, 0, 0, 1))  # 黑色字体
        self.split_button.bind(on_press=self.split_file_action)
        self.layout.add_widget(self.split_button)

        # 进度条
        self.progress_bar = ProgressBar(max=100, value=0, size_hint_y=None, height=30)
        self.layout.add_widget(self.progress_bar)

        # 设置背景色为灰色
        with self.layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)  # 灰色背景
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
            self.layout.bind(size=self.update_rect, pos=self.update_rect)

        return self.layout

    def update_rect(self, instance, value):
        """更新矩形背景的位置和大小"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def split_file_action(self, instance):
        """拆分文件"""
        file_path = self.file_chooser.selection[0] if self.file_chooser.selection else None
        if not file_path:
            self.show_popup("错误", "请先选择一个文件")
            return

        try:
            num_parts = int(self.split_input.text)
            if num_parts <= 0:
                raise ValueError("拆分份数必须大于 0")

            self.progress_bar.value = 10  # 初始化进度
            # 执行拆分
            cache_dir, parts = split_file(file_path, num_parts)
            self.progress_bar.value = 100
            self.show_popup("成功", f"文件已成功拆分为 {parts} 份！结果保存在 {cache_dir}")
        except Exception as e:
            self.show_popup("错误", str(e))

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()


if __name__ == '__main__':
    FileSplitterApp().run()
