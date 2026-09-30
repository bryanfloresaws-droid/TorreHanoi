# Torre de Hanoi – Juego en Python (Pygame)

Este proyecto es una implementación interactiva del clásico juego **Torre de Hanoi**, desarrollado en Python utilizando **Pygame**.  
Incluye menús, gráficos personalizados, sonidos y la lógica completa del juego.

---

# 🚀 Cómo ejecutar el proyecto

A continuación se muestran las instrucciones para ejecutar el proyecto usando **Git Bash** y **PowerShell**.

---

# 🟦 1️⃣ Ejecutar desde Git Bash

### ✔️ 1. Activar el entorno virtual

```bash
source venv/Scripts/activate
```

Debería verse así:

```
(venv)
```

---

### ✔️ 2. Instalar dependencias

```bash
pip install -r requerimientos.txt
```

Si pygame no se instala, usa:

```bash
./venv/Scripts/python -m pip install pygame
```

---

### ✔️ 3. Ejecutar el juego

```bash
python main.py
```

---

# 🟨 2️⃣ Ejecutar desde PowerShell

PowerShell bloquea la ejecución del script del entorno virtual la primera vez.  
Aquí están los pasos completos:

---

## 🔐 2.1 — Habilitar ejecución de scripts (solo una vez)

Abre PowerShell **como Administrador** y ejecuta:

```powershell
Set-ExecutionPolicy RemoteSigned
```

Luego presiona:

```
Y
Enter
```

Esto solo se hace una vez. Después puedes usar PowerShell normal.

---

## ▶️ 2.2 — Activar el entorno virtual

Dentro del proyecto:

```powershell
.\venv\Scripts\Activate.ps1
```

Debe aparecer:

```
(venv)
```

---

## 📦 2.3 — Instalar dependencias

```powershell
pip install -r requerimientos.txt
```

Si pygame falla:

```powershell
pip install pygame
```

---

## 🕹️ 2.4 — Ejecutar el juego

```powershell
python .\main.py
```

---

# 📁 Estructura del proyecto

```
Tarea Torre Hanoi/
│
├── main.py
├── requerimientos.txt
│
├── app/
│   ├── hanoi.py
│   ├── solver.py
│
└── game/
    ├── hanoi_game.py
    ├── menu.py
    └── assets/
```

---

# 🎮 Características

- Menú interactivo  
- Música y efectos de sonido  
- Animaciones  
- Lógica completa de Torre de Hanoi  
- Gráficos personalizados  

---
