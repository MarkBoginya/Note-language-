import tkinter as tk
from tkinter import messagebox, ttk
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка базы данных
DATABASE_URI = 'mssql+pyodbc://@DESKTOP-LFCJ22H/language_learning?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes'
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()

# Определение модели
class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    german_word = Column(String(255), nullable=False)
    translation = Column(String(255), nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Функции для работы с базой данных
def add_word(german_word, translation):
    new_word = Word(german_word=german_word, translation=translation)
    session.add(new_word)
    session.commit()

def update_word(word_id, german_word, translation):
    word = session.query(Word).filter_by(id=word_id).first()
    word.german_word = german_word
    word.translation = translation
    session.commit()

def delete_word(word_id):
    word = session.query(Word).filter_by(id=word_id).first()
    session.delete(word)
    session.commit()

def search_words(query):
    return session.query(Word).filter(Word.german_word.contains(query) | Word.translation.contains(query)).all()

def get_all_words():
    return session.query(Word).all()

# Функции для работы с GUI
def refresh_treeview():
    for row in tree.get_children():
        tree.delete(row)
    for word in get_all_words():
        tree.insert('', tk.END, values=(word.id, word.german_word, word.translation))

def on_add():
    german_word = german_word_entry.get()
    translation = translation_entry.get()
    if german_word and translation:
        add_word(german_word, translation)
        refresh_treeview()
        german_word_entry.delete(0, tk.END)
        translation_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Both fields are required.")

def on_update():
    selected_item = tree.selection()[0]
    word_id = tree.item(selected_item)['values'][0]
    german_word = german_word_entry.get()
    translation = translation_entry.get()
    if german_word and translation:
        update_word(word_id, german_word, translation)
        refresh_treeview()
        german_word_entry.delete(0, tk.END)
        translation_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Both fields are required.")

def on_delete():
    selected_item = tree.selection()[0]
    word_id = tree.item(selected_item)['values'][0]
    delete_word(word_id)
    refresh_treeview()

def on_search():
    query = search_entry.get()
    results = search_words(query)
    for row in tree.get_children():
        tree.delete(row)
    for word in results:
        tree.insert('', tk.END, values=(word.id, word.german_word, word.translation))

def on_select(event):
    selected_item = tree.selection()[0]
    word_id, german_word, translation = tree.item(selected_item)['values']
    german_word_entry.delete(0, tk.END)
    german_word_entry.insert(0, german_word)
    translation_entry.delete(0, tk.END)
    translation_entry.insert(0, translation)

# Создание графического интерфейса
root = tk.Tk()
root.title("Language Learning")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="German Word:").grid(row=0, column=0, padx=10, pady=5)
german_word_entry = tk.Entry(frame, width=30)
german_word_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Translation:").grid(row=1, column=0, padx=10, pady=5)
translation_entry = tk.Entry(frame, width=30)
translation_entry.grid(row=1, column=1, padx=10, pady=5)

add_button = tk.Button(frame, text="Add Word", command=on_add)
add_button.grid(row=2, column=0, padx=10, pady=5)

update_button = tk.Button(frame, text="Update Word", command=on_update)
update_button.grid(row=2, column=1, padx=10, pady=5)

delete_button = tk.Button(frame, text="Delete Word", command=on_delete)
delete_button.grid(row=2, column=2, padx=10, pady=5)

search_entry = tk.Entry(frame, width=30)
search_entry.grid(row=3, column=0, padx=10, pady=5)

search_button = tk.Button(frame, text="Search", command=on_search)
search_button.grid(row=3, column=1, padx=10, pady=5)

columns = ('ID', 'German Word', 'Translation')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('ID', text='ID')
tree.heading('German Word', text='German Word')
tree.heading('Translation', text='Translation')
tree.pack(pady=20)

tree.bind('<<TreeviewSelect>>', on_select)

refresh_treeview()

root.mainloop()
