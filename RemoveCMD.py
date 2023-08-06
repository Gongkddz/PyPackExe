import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
from tkinter import ttk

class PyPackExe:
    def __init__(self):
        self.python_files = []

        self.window = tk.Tk()
        self.window.title("PyPackExe")

        self.frame1 = tk.Frame(self.window) # 任务列表Frame
        self.frame1.pack()

        tk.Label(self.frame1,text = '任务列表：' ).pack(anchor = 'w')

        self.file_listbox = tk.Listbox(self.frame1, selectmode=tk.MULTIPLE, height=10,width = 100)
        self.file_listbox.pack()

        self.frame2=tk.Frame(self.window)  # 按钮的Frame
        self.frame2.pack(pady = 5)

        select_button = tk.Button(self.frame2, text="选择文件", command=self.select_python_files)
        select_button.pack(side = 'left')

        remove_button = tk.Button(self.frame2, text="移除文件", command=self.remove_selected_files)
        remove_button.pack(side = 'left',padx = 5)

        tk.Label(self.frame2,text = '模式：').pack(side = 'left',padx = 5)

        self.mode_var = tk.StringVar()
        self.mode_combobox = ttk.Combobox(self.frame2, textvariable=self.mode_var, values=["Debug", "Release"])
        self.mode_combobox.pack(side = 'left')
        self.mode_combobox.set("Debug")

        compile_button = tk.Button(self.frame2, text="开始编译", command=self.compile_selected_files)
        compile_button.pack(side = 'left',padx = 10)

    def select_python_files(self):
        python_files = filedialog.askopenfilenames(filetypes=[("Python Files", "*.py")])
        for python_file in python_files:
            if python_file not in self.python_files:
                self.python_files.append(python_file)
                self.file_listbox.insert(tk.END, python_file)

    def remove_selected_files(self):
        selected_indices = self.file_listbox.curselection()
        if len(selected_indices) == 0:
            messagebox.showinfo("提示", "请先选择要移除的文件！")
            return

        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
            del self.python_files[index]

    def compile_selected_files(self):
        if len(self.python_files) == 0:
            messagebox.showinfo("提示", "请选择要编译的文件！")
            return

        mode = self.mode_var.get()

        for python_file in self.python_files:
            self.create_exe_from_python(python_file, mode)

        messagebox.showinfo("提示", "打包完成！")

    def create_exe_from_python(self, python_path, mode):
        python_file_name = os.path.basename(python_path)
        output_exe_name = python_file_name[:-3] + ".exe"

        if mode == "Debug":
            command = f'pyinstaller -F "{python_path}" -n "{output_exe_name}"'
        elif mode == "Release":
            command = f'pyinstaller -F "{python_path}" -n "{output_exe_name}" -w'

        subprocess.call(command, shell=True)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PyPackExe()
    app.run()