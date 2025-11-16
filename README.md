# Решись!

Ниже — инструкция, которая поможет тебе начать работу над кейсом и запустить проект на своём компьютере.
Пожалуйста, следуй шагам внимательно — это избавит тебя от ошибок и ускорит работу.

# Как начать работать над кейсом

1. Начни с задач **ревью кода** — это поможет разобраться в проекте.  
   Инструкция: https://github.com/MikD1/reshis-2025/blob/main/codereview.md

2. После этого переходи к задачам **по реализации функциональности**.  
   Инструкция: https://github.com/MikD1/reshis-2025/blob/main/issues.md


# Как скачать (склонировать) репозиторий с GitHub

Чтобы начать работать с проектом локально, тебе нужно склонировать свой репозиторий — то есть скачать его на компьютер.

### 1. Скопируй ссылку на репозиторий

1. Открой свой репозиторий на GitHub.
2. Нажми зелёную кнопку **Code**.  
3. Скопируй ссылку под пунктом **HTTPS**.

### 2. Открой терминал в той папке, где хочешь хранить проект

Например, на рабочем столе или в папке `projects`.

### 3. Выполни команду клонирования

```bash
git clone <вставь_сюда_скопированную_ссылку>
```

После выполнения команды у тебя появится папка с твоим проектом.

# Запуск проекта

Ниже — подробная инструкция по настройке и запуску проекта на Python.  
Выполняй команды в терминале **в папке проекта**.

## 1. Проверь, установлен ли Python

```bash
# Windows
python --version

# macOS / Linux
python3 --version
```

Если команда не найдена:

1. Установи Python с [https://www.python.org](https://www.python.org)
2. На Windows обязательно поставь галочку **"Add to PATH"**

## 2. Создай виртуальное окружение

### Windows (CMD, PowerShell или терминал PyCharm)

```powershell
python -m venv .venv
```

### macOS / Linux (bash/zsh)

```bash
python3 -m venv .venv
```

## 3. Активируй окружение

### Windows

**PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

Если появится ошибка про Execution Policy:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**CMD:**

```cmd
.\.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
source .venv/bin/activate
```

## 4. Обнови `pip` и установи зависимости

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Запусти проект

```bash
# если ты не в папке src/
cd src

# запуск проекта
python run.py
```

## 6. Открой сайт

После запуска проекта перейди в браузере по ссылке:

**[http://localhost:5001](http://localhost:5001)**
