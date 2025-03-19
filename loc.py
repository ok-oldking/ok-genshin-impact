import os


def count_lines_of_code(folder_path, extensions=None):
    total_lines = 0
    extensions = extensions or ['.py', '.cpp', '.h', '.js', '.html']  # Specify file types to count

    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        total_lines += len(lines)
                        print(f"{file}: {len(lines)} lines")
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")

    print(f"\nTotal lines of code: {total_lines}")
    return total_lines


# Example usage
folder_path = r'src'  # Replace with the folder path
count_lines_of_code(folder_path)
