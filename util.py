import chardet


def detect_file_encoding(file_path: str) -> str:
    f = open(file_path, "rb")
    data = f.read(4)
    f.close()
    return chardet.detect(data)["encoding"]