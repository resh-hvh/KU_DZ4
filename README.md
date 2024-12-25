# UVM Assembler & Interpreter

Этот проект реализует два компонента: ассемблер и интерпретатор для виртуальной машины (УВМ), которые преобразуют текстовый код ассемблера в бинарный формат и выполняют его соответственно.

## Архитектура проекта

1. **Ассемблер**:
   - Принимает текстовый файл с кодом ассемблера.
   - Преобразует инструкции в бинарный формат.
   - Сохраняет бинарный файл и лог в формате JSON.

2. **Интерпретатор**:
   - Принимает бинарный файл и диапазон памяти.
   - Выполняет команды по их спецификации.
   - Записывает результаты выполнения в файл в формате JSON.

## Описание работы

### Ассемблер

Ассемблер выполняет следующие шаги:
- Читает инструкции из текстового файла.
- Преобразует их в бинарный формат согласно спецификации.
- Генерирует лог в формате JSON, где каждая инструкция представлена в удобочитаемом виде.

### Интерпретатор

Интерпретатор выполняет команды из бинарного файла:
- Поддерживает стековую модель и операции с памятью.
- Записывает содержимое указанного диапазона памяти в файл JSON.

## Тестовая программа

Пример программы для обработки массива из 7 элементов:

```asm
LOAD_CONST 7       # Загрузка длины массива
WRITE_MEM 100      # Запись длины в память
LOAD_CONST -3      # Загрузка первого элемента массива
WRITE_MEM 101      # Запись в память
LOAD_CONST 5
WRITE_MEM 102
LOAD_CONST 0
WRITE_MEM 103
LOAD_CONST -1
WRITE_MEM 104
LOAD_CONST 2
WRITE_MEM 105
LOAD_CONST 4
WRITE_MEM 106
LOAD_CONST -6
WRITE_MEM 107
READ_MEM 100       # Чтение длины массива
UNARY_SGN 200      # Применение sgn() к элементу
Эта программа преобразует массив [-3, 5, 0, -1, 2, 4, -6] в массив знаков [-1, 1, 0, -1, 1, 1, -1] и записывает результат в память.

Как запустить
1. Подготовка окружения
Убедитесь, что у вас установлен Python 3.x.

Сохраните файл с кодом в файл, например, uvm_tool.py.

2. Подготовьте входные файлы
Текстовый файл с программой ассемблера: Создайте файл, например, program.asm, с содержимым программы (см. выше).

Создайте папку для бинарных файлов и логов:

bash
Копировать код
mkdir output
3. Запуск ассемблера
Для преобразования программы в бинарный формат и генерации лога используйте следующую команду:

bash
Копировать код
python uvm_tool.py assemble program.asm output/program.bin output/log.json
Это создаст бинарный файл output/program.bin и лог output/log.json.

4. Запуск интерпретатора
Для выполнения бинарного файла и записи результатов в формате JSON используйте следующую команду:

bash
Копировать код
python uvm_tool.py interpret output/program.bin output/result.json 200 210
Здесь 200 и 210 — это диапазон памяти, в котором будут записаны результаты выполнения программы.

5. Проверка результатов
Откройте файл output/result.json, чтобы увидеть значения памяти после выполнения программы. Например, результат может выглядеть так:

json
Копировать код
[-1, 1, 0, -1, 1, 1, -1]
Пример команд
bash
Копировать код
# 1. Ассемблируем программу
python uvm_tool.py assemble program.asm output/program.bin output/log.json

# 2. Интерпретируем бинарный файл
python uvm_tool.py interpret output/program.bin output/result.json 200 210

# 3. Открываем результаты
cat output/result.json
Устранение неполадок
Если возникнут ошибки при запуске, не стесняйтесь сообщить об этом — мы поможем вам отладить процесс!

Лицензия
Этот проект лицензирован на условиях MIT License.
