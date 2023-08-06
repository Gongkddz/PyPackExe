import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
from tkinter import ttk

class PyPackExe:
    def __init__(self):
        self.python_files = []
        self.output_exe_name = ""

        self.window = tk.Tk()
        self.window.title("PyPackExe")

        tk.Label(self.window, text='任务列表').pack(anchor='w')
        self.file_listbox = tk.Listbox(self.window, selectmode=tk.MULTIPLE, height=10, width=100)
        self.file_listbox.pack(padx=10, pady=10)

        self.frame1 = tk.Frame()
        self.frame1.pack()

        select_button = tk.Button(self.frame1, text="选择文件", command=self.select_python_files)
        select_button.pack(padx=10, pady=5, side='left')

        remove_button = tk.Button(self.frame1, text="移除文件", command=self.remove_selected_files)
        remove_button.pack(padx=10, pady=5, side='left')

        self.mode_var = tk.StringVar()
        self.frame2 = tk.Frame()
        self.frame2.pack(pady=5)
        tk.Label(self.frame2, text='编译模式：').pack(side='left')
        self.mode_combobox = ttk.Combobox(self.frame2, textvariable=self.mode_var, values=["Debug", "Release"])
        self.mode_combobox.pack(side='left')
        self.mode_combobox.set("Debug")

        exe_name_label = tk.Label(self.frame2, text="输出EXE文件名:")
        exe_name_label.pack(padx=10, side='left')

        self.output_exe_name = os.path.splitext(os.path.basename(__file__))[0]
        self.exe_name_label = tk.Label(self.frame2, text=self.output_exe_name)
        self.exe_name_label.pack(side='left')

        compile_button = tk.Button(self.frame1, text="开始编译", command=self.compile_selected_files)
        compile_button.pack(padx=10, pady=5, side='left')

        self.output_text = tk.Text(self.window, height=10, state=tk.DISABLED, width=100)
        self.output_text.pack(padx=10, pady=10)

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
        self.output_exe_name = self.output_exe_name
        if not self.output_exe_name:
            messagebox.showinfo("提示", "请先输入输出EXE文件名！")
            return

        for python_file in self.python_files:
            self.create_exe_from_python(python_file, mode)

        messagebox.showinfo("提示", "打包完成！")

    def create_exe_from_python(self, python_path, mode):
        python_file_name = os.path.basename(python_path)
        if self.output_exe_name.endswith('.exe'):
            output_exe_name = self.output_exe_name
        else:
            output_exe_name = self.output_exe_name + ".exe"

        if mode == "Debug":
            command = f'pyinstaller -F "{python_path}" -n "{output_exe_name}"'
        elif mode == "Release":
            command = f'pyinstaller -F "{python_path}" -n "{output_exe_name}" -w'

        process = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
                                   universal_newlines = True)
        output_lines = process.communicate()[0]
        for line in output_lines.splitlines():
            self.output_text.config(state = tk.NORMAL)
            self.output_text.insert(tk.END, line)
            self.output_text.config(state = tk.DISABLED)
            self.output_text.see(tk.END)
        process.wait()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PyPackExe()
    app.run()