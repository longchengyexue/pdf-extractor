import PyPDF2
import os

print("=" * 50)
print("        PDF 页面提取工具")
print("=" * 50)

# 第一步：输入文件路径
while True:
    input_path = input("\n请输入 PDF 文件路径（直接把文件拖入窗口）：").strip().strip('"')
    if os.path.exists(input_path):
        print(f"✅ 文件找到：{input_path}")
        break
    else:
        print("❌ 文件不存在，请重新输入路径！")

# 第二步：读取 PDF 总页数
with open(input_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    total_pages = len(reader.pages)
    print(f"✅ 该 PDF 共有 {total_pages} 页")

# 第三步：输入起始页
while True:
    try:
        start_page = int(input(f"\n请输入起始页码（1 到 {total_pages}）："))
        if 1 <= start_page <= total_pages:
            break
        else:
            print(f"❌ 请输入 1 到 {total_pages} 之间的数字！")
    except ValueError:
        print("❌ 请输入数字！")

# 第四步：输入结束页
while True:
    try:
        end_page = int(input(f"请输入结束页码（{start_page} 到 {total_pages}）："))
        if start_page <= end_page <= total_pages:
            break
        else:
            print(f"❌ 请输入 {start_page} 到 {total_pages} 之间的数字！")
    except ValueError:
        print("❌ 请输入数字！")

# 第五步：设置输出路径
folder = os.path.dirname(input_path)
default_output = os.path.join(folder, "output.pdf")
print(f"\n默认保存路径：{default_output}")
custom = input("直接按回车使用默认路径，或输入新路径：").strip().strip('"')
output_path = custom if custom else default_output

# 第六步：提取页面
with open(input_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    writer = PyPDF2.PdfWriter()

    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])
        print(f"已添加第 {page_num + 1} 页")

    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

print(f"\n✅ 完成！已提取第 {start_page} 页到第 {end_page} 页")
print(f"✅ 文件已保存到：{output_path}")
input("\n按回车键退出...")
