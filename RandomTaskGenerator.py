import tkinter as tk
import random
import json
from tkinter.messagebox import showerror, showinfo

#Создание окна
window = tk.Tk()
window.title("Random Task Generator")
window.geometry("750x400")

#label приветсвие
welcome_label = tk.Label(window, text="Добро пожаловать в генератор случайных задач.")
welcome_label.pack(pady=20)

#frame для инструментов добавления
add_frame = tk.Frame(window, height=200, width=200)
add_frame.place(x=20, y=60)

#label для добавления задачи
add_label = tk.Label(add_frame, text="Добавление задачи")
add_label.pack()

#entry для ввода задачи
add_entry = tk.Entry(add_frame, width=20)
add_entry.pack()

#label для выбора категории
choose_label = tk.Label(add_frame, text="Выберите категорию")
choose_label.pack()

#listbox с категориями
category_lb = tk.Listbox(add_frame, height=4)
category_lb.pack()

#Функция добавления новой задачи
def add_task():
    global tasks #Глобальная переменная - список задач
    try:
        task = add_entry.get() #получение задачи
        if task == "": #Если задача пустая выдает сообщение об ошибке и останавлиавет процесс
            showerror(title="Ошибка", message="Поле для добавления новой задачи пустое")
            return 
        category_indx = category_lb.curselection() #Получает идекс категории для дальнейшего добавления
        if not category_indx: #Если категория не выбрана выдает сообщение об ошибке и останавливает процесс
            showerror(title="Ошибка", message="Не выбрана категория для добавления")
            return
        else:        
            category = category_lb.get(category_indx[0])
        new_task = {"category": category, "task": task} #формирование новой задачи из категории и задачи
        tasks.append(new_task) #добавление новой задачи в список
        save_file(tasks) #Сохранение в файл задач
        showinfo(title="Добавленно", message="Задача успешно добавлена")
    except ValueError:
        showerror(title="Ошибка", message="Ошибка работы с данными)
        
        
#Кнопка добавления
add_btn = tk.Button(window, text="Добавить", command=add_task)
add_btn.place(x=40, y=190)

#frame для результата
result_frame = tk.Frame(window, height=200, width=200)
result_frame.place(x=250, y=60)

#Функция генерации задания
def generate_task():
    global tasks
    global history
    #Проверка на наличие фильтрации по категориям
    category_indx = category_lb.curselection()
    #Если каитегория для фильтрации включена
    if category_indx:
        category_filter = category_lb.get(category_indx[0])
        filtered_tasks = [] #Список для фильтрации категорий
        for task in tasks: #Фильтрация по категории
            if task["category"] == category_filter:
                filtered_tasks.append(task)
        if filtered_tasks == []: #Проверка на наличие задч в выбранной категории
            showerror(title="Ошибка", message="Задач в выбранной категории не существует") 
            return
        else:
            chosen_task = random.choice(filtered_tasks) #Выбор задачи из отфильтрованого списка
    #Если фильтрация не выбрана
    else:
        chosen_task = random.choice(tasks) #Выбор задачи из всего списка
        
    result_label.config(text=f"{chosen_task['category']}: {chosen_task['task']}") #Вывод результата в нужный label
    add_history_label = tk.Label(history_frame, text=f"{chosen_task['category']}: {chosen_task['task']}").pack() #Создание новго lable для показа истории генераций
    history.append(f"{chosen_task['category']}: {chosen_task['task']}") #Добавление в список для сохранения в файл
    save_history(history) #Сохранение истории

#кнопка для вывода результата
result_btn = tk.Button(result_frame, text="Сгенерировать", command=generate_task)
result_btn.pack()

#label отметка зоны для результата
result_message_label = tk.Label(result_frame, text="Результат:")
result_message_label.pack()

#label результата
result_label = tk.Label(result_frame, text="", fg="blue") #изначальное пустое, будет меняться исходя из выполнения генерации
result_label.pack()

#frame для истории генераций
history_frame = tk.Frame(window, height=200, width=200)
history_frame.place(x=500, y=60)

#label истории
history_label = tk.Label(history_frame, text="История генераций:")
history_label.pack()

#Загрузка данных из файла json
def load_file():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

#Сохранение новых заданий
def save_file(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

#Загрузка истории
def load_history():
    try:
        with open("history.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

#Сохранение истории в файл
def save_history(history):
    with open("history.json", "w") as file:
        json.dump(history, file)

#Стандартные задачи, которые всегда будут в приложении
standart_tasks = [{"category": "спорт", "task": "Сделать зарядку"}, {"category": "отдых", "task": "Почитать книгу"}, {"category": "работа", "task": "Написать приложение на Python"}, {"category": "учёба", "task": "Написать сочинение"}]
tasks = load_file()
if tasks == []: #Приравнивание пустого списка задач к стандартному
    tasks = standart_tasks

history = load_history() #Список для сохранения истории
for part in history: #Загрузка истории из файла на старте
    add_history_label = tk.Label(history_frame, text=part).pack()


#список категорий для listbox
category_list = ["спорт", "работа", "учёба", "отдых"]
for category in category_list: #Помещение категорий в listbox
    category_lb.insert(tk.END, category)

#Запуск программы
window.mainloop()
