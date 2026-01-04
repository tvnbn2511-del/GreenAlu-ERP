import os

# Tên file kết quả
output_file = 'full_project_context.txt'

# Các thư mục và file muốn BỎ QUA (Không cần AI đọc)
ignore_dirs = {'.git', 'venv', '__pycache__', 'migrations', 'media', 'static'}
ignore_files = {'db.sqlite3', 'export_code.py', '.gitignore'}
# Các đuôi file muốn lấy code
allowed_extensions = {'.py', '.html', '.css', '.js'}

def is_ignored(path, names):
    # Hàm lọc bỏ thư mục không cần thiết
    return {name for name in names if name in ignore_dirs}

with open(output_file, 'w', encoding='utf-8') as outfile:
    # Duyệt qua tất cả thư mục
    for root, dirs, files in os.walk('.', topdown=True):
        # Lọc bỏ thư mục rác
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file in ignore_files:
                continue
            
            # Chỉ lấy các file code (.py, .html...)
            if file_extension in allowed_extensions:
                file_path = os.path.join(root, file)
                
                # Ghi tên file làm tiêu đề
                outfile.write(f"\n{'='*50}\n")
                outfile.write(f"FILE: {file_path}\n")
                outfile.write(f"{'='*50}\n")
                
                # Ghi nội dung file
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write("\n")
                except Exception as e:
                    outfile.write(f"[Lỗi không đọc được file: {e}]\n")

print(f"Xong! Đã gom toàn bộ code vào file: {output_file}")