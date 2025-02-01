from abc import abstractmethod
import os
import locale
import sys
import chardet
from ccwc import SUCCESS, FILE_ERROR, STDIN_ERROR
from typing import NamedTuple


class Response(NamedTuple):
    content_length: int
    error_code: int


class ContentCounter(object):
    """
    Abstract class for counting content
    """
    def __init__(self, user_input: str):
        self.user_input = user_input
    
    @abstractmethod
    def count_content(self) -> Response:
        raise NotImplementedError("Abstract method cannot be instantiated in a base class!")


class FileContentCounter(ContentCounter):
    """
    The file-related class for counting
    """
    def __init__(self, file_name: str):
        super().__init__(file_name)
    

    def generate_path(self) -> str:
        current_path = os.getcwd()
        file_path = os.path.join(current_path, self.user_input)
        return file_path
    

    def detect_encoding(self) -> str:
        file_path = self.generate_path()
        with open(file_path, 'rb') as file_reader:
            content_snippet = file_reader.read(4096)
            encoding = chardet.detect(content_snippet)
            return encoding
    

    @abstractmethod
    def read_content(self):
        raise NotImplementedError("Abstract method cannot be instantiated in base class!")


class FileByteCounter(FileContentCounter):
    """
    File content byte counter
    """
    def __init__(self, file_name: str):
        super().__init__(file_name)


    def read_content(self) -> bytes:
        file_path = self.generate_path()
        with open(file_path, 'rb') as file_reader:
            content = file_reader.read()
        return content


    def count_content(self) -> int:
        try:
            content = self.read_content()
            return Response(len(content),SUCCESS)
        except FileNotFoundError:
            return Response(0, FILE_ERROR)


class FileLineCounter(FileContentCounter):
    """
    File content line counter 
    """
    def __init__(self, file_name: str):
        super().__init__(file_name)

    
    def read_content(self) -> str:
        file_path = self.generate_path()
        encoding = self.detect_encoding().get('encoding')
        with open(file_path, "r", encoding=encoding) as file_reader:
            content = file_reader.readlines()
        return content


    def count_content(self) -> int:
        try:
            content = self.read_content()
            return Response(len(content), SUCCESS)
        except FileNotFoundError:
            return Response(0, FILE_ERROR)


class FileWordCounter(FileContentCounter):
    """
    File word counter
    """

    def __init__(self, file_name: str):
        super().__init__(file_name)


    def read_content(self) -> str:
        file_path = self.generate_path()
        encoding = self.detect_encoding().get('encoding')
        with open(file_path, "r", encoding=encoding) as file_reader:
            content = file_reader.read()
        return content


    def count_content(self) -> int:
        try:
            content = self.read_content()
            words = content.split()
            return Response(len(words), SUCCESS)
        except FileNotFoundError:
            return Response(0, FILE_ERROR)         


class FileCharCounter(FileByteCounter):
    """
    FIle character counter with consideration of the locale
    If the current locale does not support multibyte characters then read as bytes
    """
    def __init__(self, file_name: str):
        super().__init__(file_name)


    LOCALE_SUPPORT_MULTIBYTE = ["UTF-8", "ISO-8859-2", "Windows-1250"]

    def read_content(self) -> str:
        """
        Reading in bytes is needed for BOM handling
        Decoding from bytes using default system locale ensures the BOM is accounted for
        If this fails, opt for encoding of file
        """
        current_locale = locale.getlocale()[1]
    
        if current_locale in self.LOCALE_SUPPORT_MULTIBYTE:
            file_path = self.generate_path()
            try:
                with open(file_path, "rb") as file_reader:
                    content = file_reader.read().decode(current_locale)
            except UnicodeDecodeError:
                with open(file_path, "rb") as file_reader:
                    encoding = self.detect_encoding().get('encoding')
                    content = file_reader.read().decode(encoding)
            return content
        else:
            super().read_content(self)


class StdInByteCounter(ContentCounter):
    """
    Read standard input as an argument and counts its content
    """ 
    def __init__(self):
        std_input = sys.stdin.buffer.read()
        super().__init__(std_input)

    
    def count_content(self) -> int:
        try:
            return Response(len(self.user_input), SUCCESS)
        except Exception:
            return Response(0, STDIN_ERROR)


class StdInLineCounter(ContentCounter):
    """
    Read standard input as an argument and count lines
    """
    def __init__(self):
        std_input = sys.stdin.readlines()
        super().__init__(std_input)
    
    
    def count_content(self) -> int:
        try:
            return Response(len(self.user_input), SUCCESS)
        except Exception:
            return Response(0, STDIN_ERROR)


class StdInWordCounter(StdInByteCounter):
    """
    Read standard input as an argument and count words
    """
    def __init__(self):
        super().__init__()
    

    def count_content(self) -> int:
        try:
            content = self.user_input
            words = [word for word in content.split()]
            return Response(len(words), SUCCESS)
        except Exception:
            return Response(0, STDIN_ERROR)


class StdInCharCounter(StdInByteCounter):
    """
    Read standard input as an arguemnt and count character considering the locale
    """
    def __init__(self):
        super().__init__()
    

    LOCALE_SUPPORT_MULTIBYTE = ["UTF-8", "ISO-8859-2", "Windows-1250"]

    def count_content(self) -> int:
        current_locale = locale.getlocale()[1]

        if current_locale in self.LOCALE_SUPPORT_MULTIBYTE:
            content = self.user_input.decode(current_locale)
            return Response(len(content), SUCCESS)
        else:
            super().count_content()
