# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import text_extraction
import text_playback


book_path = "./Shelf/fleming-casino-royale.epub"
book2_path = "./Shelf/various-childrens-book-of-christmas-stories.epub"
book_sw_path = "./Shelf/Star Wars - Aftermath - Debito di Vita (Chuck Wendig).epub"

title, text = text_extraction.extract_text(book_path)
clean = text_extraction.clean_text(text)
print(title)
print(text)
print(clean)

for chapter in clean:
    sentences = clean[chapter]
    text_playback.play_sentence(chapter)
    for sentence in sentences:
        text_playback.play_sentence(sentence)
