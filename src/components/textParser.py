from ebooklib import epub, ITEM_DOCUMENT
import ebooklib
from bs4 import BeautifulSoup

from src.components.configManager import configManager

class textParser:
    REPLACESTRINGS = [
        "Chapter ",
        "Table of Contents"
    ]
    def __init__(self):
        self.cm = configManager()
        self.cfg = self.cm.load()

    def parse(self, file_path):
        ext = file_path.split(".")[-1]
        match ext:
            case "txt" : 
                with open(file_path, "r") as f:
                    text = f.read()
                    f.close()
                words = [text.split()] #put in a single "chapter"
                wordcount = len(words[0])
                ch_count = 1
                wordcount_ch = wordcount

            case "epub" :
                ### LLM gen section
                book = epub.read_epub(file_path)
                chapters = []
                for item in book.get_items_of_type(ITEM_DOCUMENT):
                    soup = BeautifulSoup(item.get_content(), "html.parser")
                    # Remove scripts/styles if present
                    for tag in soup(["script", "style"]):
                        tag.decompose()
                    text = soup.get_text(separator="\n", strip=True)
                    if text:
                        chapters.append(text)
                ###

                blank = self.cfg["blank"]
                words, wordcount = [], 0
                for c in chapters:
                    for r in self.REPLACESTRINGS:
                        c = c.replace(r, r.replace(" ",blank))
                    words += [c.split()] 
                    wordcount += len(c)
                wordcount_ch = len(words[0])
                ch_count = len(words)
                        
        return (words, wordcount, wordcount_ch, ch_count)