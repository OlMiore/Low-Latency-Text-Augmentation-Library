# Модуль ruaugment.

Библиотека для аугментации русскоязычных текстов содержит базовые классы и аугменторы, используемые в пайплайне.

## Структура модуля ruaugment/

 - base.py          — базовые классы аугменторов
 - char.py          — символьные искажения (CharNoiseAugmentor)
 - deletion.py      — случайное удаление слов
 - morph.py         — морфологические преобразования
 - pipeline.py      — сборка и запуск пайплайна
 - swap.py          — перестановка слов
 - synonym.py       — замена слов на синонимы
 - validator.py     — проверка допустимых комбинаций аугменторов

---

## Пример работы пайплайна.

**Исходный текст: `кредит и деньги важны`**

### Запуск пайплайна в VS Code

<img width="959" height="562" alt="Image" src="https://github.com/user-attachments/assets/1c6f3b3d-08c1-4e0f-8f01-38b5f8027fc8" />

### Вывод результата в терминале

<img width="700" height="181" alt="Image" src="https://github.com/user-attachments/assets/a35dbc00-d49a-4537-8227-7bd25977c8c1" />

### Очистка кэша и повторный запуск

<img width="866" height="455" alt="Image" src="https://github.com/user-attachments/assets/df5cec73-33a3-4a39-b410-cfaeec1a7c05" />

### Финальный результат аугментации

<img width="867" height="158" alt="Image" src="https://github.com/user-attachments/assets/5af328e8-3832-4c09-92da-941d8f205f88" />

---

## Описание работы.

Пайплайн последовательно применяет три аугментатора:

1. **CharNoiseAugmentor** — добавляет символьный шум  
2. **SynonymAugmentor** — заменяет слова на синонимы  
3. **RandomDeletionAugmentor** — случайно удаляет слова  

Результат демонстрирует корректную работу всех модулей и валидацию последовательности.
