import struct
import argparse
import os
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from io import BytesIO

def is_url(path):
    """Check if the path is a URL"""
    try:
        result = urlparse(path)
        return result.scheme in ('http', 'https')
    except:
        return False

def read_file(path):
    """Read file from local path or URL"""
    if is_url(path):
        print(f"Downloading remote file: {path}")
        request = Request(path, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(request, timeout=30) as response:
            return BytesIO(response.read())
    else:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"The file '{path}' does not exist.")
        return open(path, 'rb')

def parse_git_index(index_file):
    """Parse Git index from a file-like object"""
    # Read the index header
    header = index_file.read(12)
    signature, version, num_entries = struct.unpack('!4sII', header)

    # Check if the file is a valid Git index
    if signature != b'DIRC':
        raise ValueError("The file is not a valid Git index.")
    print(f"Index version: {version}, Number of entries: {num_entries}")

    # List to store the filenames
    filenames = []

    for _ in range(num_entries):
        # Read the index entry
        try:
            # Try to read the 62 bytes of metadata for each entry
            entry_header = index_file.read(62)
            if len(entry_header) < 62:
                raise ValueError("Incomplete entry in the index file.")
            
            # Unpack only the main required fields
            unpacked_data = struct.unpack('!10I20sH', entry_header)
            sha1 = unpacked_data[9]  # Keep SHA-1 only as a reference for checking
            
            # The filename field has a variable length
            name_bytes = b''
            while True:
                byte = index_file.read(1)
                if byte == b'\x00':
                    break
                name_bytes += byte
            filename = name_bytes.decode('utf-8', errors='replace')
            filenames.append(filename)

            # Advance to the next entry block (8-byte alignment)
            padding = (8 - (len(entry_header) + len(name_bytes) + 1) % 8) % 8
            index_file.read(padding)

        except struct.error as e:
            print(f"Error reading an entry: {e}")
            break

    return filenames

def main():
    # Configure command-line arguments
    parser = argparse.ArgumentParser(
        description="List files in the Git index and save them to a .txt file",
        epilog="Examples:\n"
               "  Local:  python script.py .git/index output.txt\n"
               "  Remote: python script.py https://example.com/.git/index output.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("index_path", help="Path to the index file (.git/index) or remote URL")
    parser.add_argument("output_file", help="Name of the output file (e.g., files.txt)")
    args = parser.parse_args()

    # Parse the index and get the filenames
    try:
        with read_file(args.index_path) as f:
            filenames = parse_git_index(f)
        
        # Save the listing to the output file with UTF-8 encoding
        with open(args.output_file, 'w', encoding='utf-8') as output_file:
            for filename in filenames:
                output_file.write(filename + '\n')
        
        print(f"File listing saved in '{args.output_file}'.")
        print(f"Total files: {len(filenames)}")

    except Exception as e:
        print(f"Error processing the file: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
