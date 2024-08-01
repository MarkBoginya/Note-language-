import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка базы данных
DATABASE_URI = 'mssql+pyodbc://@DESKTOP-LFCJ22H/language_learning?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes'
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()

# Определение модели
class Phrase(Base):
    __tablename__ = 'phrases'
    id = Column(Integer, primary_key=True, autoincrement=True)
    german_phrase = Column(String(255), nullable=False)
    translation = Column(String(255), nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Функции для работы с базой данных
def add_phrase(german_phrase, translation):
    new_phrase = Phrase(german_phrase=german_phrase, translation=translation)
    session.add(new_phrase)
    session.commit()

def update_phrase(phrase_id, german_phrase, translation):
    phrase = session.query(Phrase).filter_by(id=phrase_id).first()
    phrase.german_phrase = german_phrase
    phrase.translation = translation
    session.commit()

def delete_phrase(phrase_id):
    phrase = session.query(Phrase).filter_by(id=phrase_id).first()
    session.delete(phrase)
    session.commit()

def search_phrases(query):
    return session.query(Phrase).filter(Phrase.german_phrase.contains(query) | Phrase.translation.contains(query)).all()

def get_all_phrases():
    return session.query(Phrase).all()

# Функции для работы с GUI
def refresh_treeview():
    for row in tree.get_children():
        tree.delete(row)
    for phrase in get_all_phrases():
        tree.insert('', 'end', values=(phrase.german_phrase, phrase.translation))

def on_add():
    german_phrase = german_phrase_entry.get()
    translation = translation_entry.get()
    if german_phrase and translation:
        add_phrase(german_phrase, translation)
        refresh_treeview()
        german_phrase_entry.delete(0, tk.END)
        translation_entry.delete(0, tk.END)
    else:
        ttk.Messagebox.show_error("Both fields are required.", "Error")

def on_update():
    selected_item = tree.selection()[0]
    german_phrase, translation = tree.item(selected_item)['values']
    new_german_phrase = german_phrase_entry.get()
    new_translation = translation_entry.get()
    if new_german_phrase and new_translation:
        phrase_id = session.query(Phrase).filter_by(german_phrase=german_phrase, translation=translation).first().id
        update_phrase(phrase_id, new_german_phrase, new_translation)
        refresh_treeview()
        german_phrase_entry.delete(0, tk.END)
        translation_entry.delete(0, tk.END)
    else:
        ttk.Messagebox.show_error("Both fields are required.", "Error")

def on_delete():
    selected_item = tree.selection()[0]
    german_phrase, translation = tree.item(selected_item)['values']
    phrase_id = session.query(Phrase).filter_by(german_phrase=german_phrase, translation=translation).first().id
    delete_phrase(phrase_id)
    refresh_treeview()

def on_search():
    query = search_entry.get()
    results = search_phrases(query)
    for row in tree.get_children():
        tree.delete(row)
    for phrase in results:
        tree.insert('', 'end', values=(phrase.german_phrase, phrase.translation))

def on_select(event):
    selected_item = tree.selection()[0]
    german_phrase, translation = tree.item(selected_item)['values']
    german_phrase_entry.delete(0, tk.END)
    german_phrase_entry.insert(0, german_phrase)
    translation_entry.delete(0, tk.END)
    translation_entry.insert(0, translation)

# Создание графического интерфейса
root = ttk.Window(themename="darkly")
root.title("Language Learning")
root.geometry("800x600")

frame = ttk.Frame(root, padding=10)
frame.pack(pady=20, fill=tk.BOTH, expand=True)

ttk.Label(frame, text="German Phrase:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
german_phrase_entry = ttk.Entry(frame, width=50, font=("Helvetica", 12))
german_phrase_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame, text="Translation:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
translation_entry = ttk.Entry(frame, width=50, font=("Helvetica", 12))
translation_entry.grid(row=1, column=1, padx=10, pady=5)

button_frame = ttk.Frame(frame)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

add_button = ttk.Button(button_frame, text="Add Phrase", command=on_add, bootstyle=SUCCESS)
add_button.pack(side=tk.LEFT, padx=10)

update_button = ttk.Button(button_frame, text="Update Phrase", command=on_update, bootstyle=INFO)
update_button.pack(side=tk.LEFT, padx=10)

delete_button = ttk.Button(button_frame, text="Delete Phrase", command=on_delete, bootstyle=DANGER)
delete_button.pack(side=tk.LEFT, padx=10)

search_frame = ttk.Frame(frame)
search_frame.grid(row=3, column=0, columnspan=2, pady=10)

search_entry = ttk.Entry(search_frame, width=50, font=("Helvetica", 12))
search_entry.pack(side=tk.LEFT, padx=10)

search_button = ttk.Button(search_frame, text="Search", command=on_search, bootstyle=PRIMARY)
search_button.pack(side=tk.LEFT, padx=10)

columns = ('German Phrase', 'Translation')
tree = ttk.Treeview(frame, columns=columns, show='headings', bootstyle=INFO)
tree.heading('German Phrase', text='German Phrase')
tree.heading('Translation', text='Translation')
tree.grid(row=4, column=0, columnspan=2, pady=20, sticky='nsew')

frame.grid_rowconfigure(4, weight=1)
frame.grid_columnconfigure(1, weight=1)

tree.bind('<<TreeviewSelect>>', on_select)

refresh_treeview()

root.mainloop()