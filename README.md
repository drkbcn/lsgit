# 🐍 Git Index File Lister

**Python script to list the files inside a `.git` `index` file.** Perfect for cases where `git ls-files` doesn't work due to incomplete dumps or damaged repositories!

## 🚀 About this Script

This script parses the `.git/index` file directly and lists all tracked files, bypassing `git` commands. Ideal for use in recovery situations, corrupted repos, or when you need direct access to file listings in the Git index.

### 🧰 Features

- Extracts and lists all file entries in the Git index.
- **Supports both local and remote index files** (HTTP/HTTPS URLs).
- Avoids dependency on `git` CLI, perfect for incomplete repositories.
- Saves output to a `.txt` file, making it easy to analyze or share file lists.
- **No external dependencies** - uses only Python standard library.

## ⚙️ Usage

Run the script by specifying the path to the `.git/index` file (local or remote URL) and an output file name.

### Local File
```bash
python lsgit.py /path/to/.git/index output.txt
```

### Remote File
```bash
python lsgit.py https://example.com/.git/index output.txt
```

### Examples

**Local repository:**
```bash
python lsgit.py /home/user/project/.git/index file_list.txt
```

**Remote repository:**
```bash
python lsgit.py https://target-site.com/.git/index remote_files.txt
```

This command will generate a `file_list.txt` or `remote_files.txt` with all files listed in the Git index.

## 🛠 Requirements

- Python 3.6+
- No external dependencies required!
- Works on any system with Python installed

### requirements.txt
```txt
# No external dependencies required
# Python 3.6+ required
```

## 📄 Code Overview

The script:
1. Detects whether the input is a local file or remote URL.
2. Reads the `.git/index` file (locally or downloads it remotely).
3. Parses entries in binary mode, capturing file paths in UTF-8.
4. Outputs the results to the specified text file.

Error handling ensures a smooth run even with non-UTF-8 characters or partially corrupted data.

## 🔍 Use Cases

- **Security Testing**: Enumerate files in exposed `.git` directories on web servers.
- **Repository Recovery**: Extract file listings from corrupted or incomplete Git repositories.
- **Forensics**: Analyze Git index files without a full repository checkout.
- **Automation**: Integrate into scripts that need to process Git index data programmatically.

## 👥 Contributing

Want to make it even better? Contributions are welcome! Simply fork the project, make your changes, and submit a pull request.

## 📜 License

This project is open-source under the MIT License. Feel free to use, modify, and distribute it as you like.

---

Let's make Git indexing easier, one script at a time! 🚀
