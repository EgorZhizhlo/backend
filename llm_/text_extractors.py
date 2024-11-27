import re
import os
import aiohttp
from PyPDF2 import PdfReader
from docx import Document
from bs4 import BeautifulSoup


class TextFileExtractor:
    """
    Класс для извлечения текста из файлов форматов PDF, DOCX и TXT.
    """

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Извлекает текст из файла указанного типа и возвращает его в бинарном формате (blob).

        :param file_path: Путь к файлу.
        :return: Извлеченный текст в бинарном формате (bytes).
        :raises ValueError: Если формат файла не поддерживается.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension == ".pdf":
            text = TextFileExtractor._extract_from_pdf(file_path)
        elif file_extension == ".docx":
            text = TextFileExtractor._extract_from_docx(file_path)
        elif file_extension == ".txt":
            text = TextFileExtractor._extract_from_txt(file_path)
        else:
            raise ValueError(f"Формат файла не поддерживается: {file_extension}")

        # Преобразуем текст в бинарный формат
        return text

    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """
        Извлекает текст из PDF-файла.

        :param file_path: Путь к PDF-файлу.
        :return: Извлеченный текст.
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text.strip()
        except Exception as e:
            raise ValueError(f"Ошибка при чтении PDF-файла: {e}")

    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """
        Извлекает текст из DOCX-файла.

        :param file_path: Путь к DOCX-файлу.
        :return: Извлеченный текст.
        """
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise ValueError(f"Ошибка при чтении DOCX-файла: {e}")

    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """
        Извлекает текст из TXT-файла.

        :param file_path: Путь к TXT-файлу.
        :return: Извлеченный текст.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except Exception as e:
            raise ValueError(f"Ошибка при чтении TXT-файла: {e}")


class TextUrlExtractor:
    @staticmethod
    async def extract_text(url: str) -> str:
        # Fetch content from the URL using aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Raise an error for bad responses
                html_content = await response.text()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract text from the parsed HTML
        text = soup.get_text(separator=' ', strip=True)

        # Clean the text by removing unwanted characters
        cleaned_text = TextUrlExtractor.clean_text(text)

        # Convert the cleaned text to UTF-8 bytes
        return cleaned_text

    @staticmethod
    def clean_text(text: str) -> str:
        # Remove unwanted characters (e.g., multiple spaces, newlines, etc.)
        text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with a single space
        text = text.strip()  # Remove leading and trailing whitespace
        return text
