import tkinter as tk
from tkinter import messagebox
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

# Создание графического интерфейса
def add_word():
    german_word = german_word_entry.get()
    translation = translation_entry.get()
    if german_word and translation:
        new_word = Word(german_word=german_word, translation=translation)
        session.add(new_word)
        session.commit()
        messagebox.showinfo("Success", "Word added successfully!")
        german_word_entry.delete(0, tk.END)
        translation_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Both fields are required.")

root = tk.Tk()
root.title("Language Learning")

tk.Label(root, text="German Word:").grid(row=0, column=0, padx=10, pady=10)
german_word_entry = tk.Entry(root, width=50)
german_word_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Translation:").grid(row=1, column=0, padx=10, pady=10)
translation_entry = tk.Entry(root, width=50)
translation_entry.grid(row=1, column=1, padx=10, pady=10)

add_button = tk.Button(root, text="Add Word", command=add_word)
add_button.grid(row=2, columnspan=2, pady=20)

root.mainloop()
