import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
import os


def select_file():
    path = filedialog.askopenfilename(
        title="选择 PDF 文件",
        filetypes=[("PDF 文件", "*.pdf")]
    )
    if path:
        input_path_var.set(path)
        try:
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                total = len(reader.pages)
            total_pages_var.set(f"共 {total} 页")
            total_pages_count.set(total)
            start_entry.config(state="normal")
            end_entry.config(state="normal")
            run_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("错误", f"无法读取 PDF：{e}")


def run_export():
    input_path = input_path_var.get()
    total = total_pages_count.get()

    try:
        start = int(start_var.get())
        end = int(end_var.get())
    except ValueError:
        messagebox.showerror("错误", "页码必须是数字！")
        return

    if not (1 <= start <= total):
        messagebox.showerror("错误", f"起始页必须在 1 到 {total} 之间！")
        return
    if not (start <= end <= total):
        messagebox.showerror("错误", f"结束页必须在 {start} 到 {total} 之间！")
        return

    # 默认输出路径
    folder = os.path.dirname(input_path)
    default_output = os.path.join(folder, "output.pdf")

    output_path = filedialog.asksaveasfilename(
        title="保存文件",
        initialdir=folder,
        initialfile="output.pdf",
        defaultextension=".pdf",
        filetypes=[("PDF 文件", "*.pdf")]
    )
    if not output_path:
        return

    try:
        with open(input_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            writer = PyPDF2.PdfWriter()
            for i in range(start - 1, end):
                writer.add_page(reader.pages[i])
        with open(output_path, 'wb') as out:
            writer.write(out)
        messagebox.showinfo("完成", f"已提取第 {start} 页到第 {end} 页\n保存至：{output_path}")
    except Exception as e:
        messagebox.showerror("错误", f"提取失败：{e}")


# 主窗口
root = tk.Tk()
root.title("PDF 页面提取工具")
root.resizable(False, False)

input_path_var = tk.StringVar()
total_pages_var = tk.StringVar(value="请先选择文件")
total_pages_count = tk.IntVar(value=0)
start_var = tk.StringVar()
end_var = tk.StringVar()

padding = {"padx": 15, "pady": 8}

# 选择文件区域
frame1 = tk.LabelFrame(root, text="第一步：选择 PDF 文件", padx=10, pady=10)
frame1.pack(fill="x", padx=15, pady=(15, 5))

tk.Entry(frame1, textvariable=input_path_var, width=45, state="readonly").pack(side="left", padx=(0, 8))
tk.Button(frame1, text="浏览...", command=select_file, width=8).pack(side="left")
tk.Label(frame1, textvariable=total_pages_var, fg="gray").pack(side="left", padx=(12, 0))

# 页码输入区域
frame2 = tk.LabelFrame(root, text="第二步：输入页码范围", padx=10, pady=10)
frame2.pack(fill="x", padx=15, pady=5)

tk.Label(frame2, text="起始页：").grid(row=0, column=0, sticky="e", pady=4)
start_entry = tk.Entry(frame2, textvariable=start_var, width=8, state="disabled")
start_entry.grid(row=0, column=1, sticky="w", padx=(4, 20))

tk.Label(frame2, text="结束页：").grid(row=0, column=2, sticky="e")
end_entry = tk.Entry(frame2, textvariable=end_var, width=8, state="disabled")
end_entry.grid(row=0, column=3, sticky="w", padx=4)

# 执行按钮
run_button = tk.Button(root, text="提取并保存 PDF", command=run_export,
                       state="disabled", width=20, height=2,
                       bg="#0078D7", fg="white", font=("", 11, "bold"))
run_button.pack(pady=(10, 18))

root.mainloop()
