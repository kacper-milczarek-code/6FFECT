# 6FFECT

[![Language: EN](https://img.shields.io/badge/Language-EN-blue.svg)](README.md)

**6FFECT** to aplikacja desktopowa służąca do nakładania sześciu autorskich, dynamicznych efektów wizualnych na dowolny obraz. 
Program oferuje regulację parametrów w czasie rzeczywistym, co pozwala użytkownikom na bieżąco dostosowywać właściwości obrazu i zachowanie efektów. 
Całość została zamknięta w dopracowanym interfejsie inspirowanym stylem sci-fi, wzbogaconym o autorską grafikę i interaktywne efekty dźwiękowe.

<p align="center">
  <img width="49%" alt="Przegląd menu 6FFECT" src="https://github.com/user-attachments/assets/ac532882-e6d4-48b0-a93c-25de32d0cffb" />
  <img width="49%" alt="Ustawienia interfejsu 6FFECT" src="https://github.com/user-attachments/assets/cf40b658-17ea-4e2d-8bc0-d2f9b7b38eb5" />
</p>

## ℹ️️ O projekcie
6FFECT to mój pierwszy projekt opublikowany na GitHubie. Stworzyłem go, aby rozwinąć swoje umiejętności programowania w języku Python — skupiając się w szczególności na programowaniu obiektowym (OOP), 
projektowaniu wielomodułowej architektury aplikacji, zarządzaniu wielowątkowością oraz wdrażaniu przepływu pracy opartego na Git/GitHub. Graficzny interfejs użytkownika został zbudowany przy użyciu frameworka PySide6. 
Autorskie efekty wizualne stworzyłem od podstaw, wykorzystując bibliotekę NumPy do wysokowydajnych, wektorowych operacji na macierzach, przy częściowym wsparciu biblioteki Pillow.

## ✨ Główne funkcje
- **6 Autorskich Efektów**: FLIPPER, FADER, NUKER, PUZZLER, LINER oraz RAINBOWER.
- **Regulacja w czasie rzeczywistym**: Płynna zmiana parametrów obrazu (jasność, nasycenie, kontrast) oraz właściwości efektów za pomocą prostych suwaków.
- **Eksport do wideo MP4**: Renderowanie niestandardowych animacji bezpośrednio do formatu MP4 z widocznym paskiem postępu.
- **Interfejs Sci-Fi i Dźwięk**: Oparty na frameworku Qt interfejs w stylu sci-fi z interaktywnymi efektami dźwiękowymi.
- **Przeciągnij i upuść (Drag & Drop)**: Szybkie wczytywanie obrazów z inteligentnym dopasowaniem do proporcji 16:9 / 9:16.

## ⚡ Efekty wizualne
- **FLIPPER**: Dzieli obraz na kwadraty i obraca każdy z nich o 90 stopni w lewo.
- **FADER**: Nakłada na obraz nieregularne, przypominające plamy, zaczerniając grupy pikseli.
- **NUKER**: Rozjaśnia wszystkie piksele obrazu, powodując degradację w stylu glitch-art poprzez przepełnienie kanałów RGB.
- **PUZZLER**: Dzieli obraz na kwadraty i losowo zamienia ich pozycje.
- **LINER**: Zaciemnia lub zniekształca rzędy pikseli. Po zakończeniu wykonuje proces odwrotny, przywracając oryginalne linie.
- **RAINBOWER**: Dzieli obraz na kwadraty i zabarwia każdy z nich losowym kanałem koloru.

## 🎬 Prezentacja wideo (Showcase)
https://github.com/user-attachments/assets/d456d1c8-99a9-4497-ae2f-ad347bad72f0

## 🛠️ Stos technologiczny
- **[Python](https://www.python.org/)** — Główny język programowania
- **[PySide6 / Qt](https://doc.qt.io/qtforpython-6/)** — Framework interfejsu graficznego (GUI) oraz komponenty UI
- **[NumPy](https://numpy.org/)** — Wydajne operacje wektorowe na macierzach (silnik efektów wizualnych)
- **[OpenCV](https://opencv.org/)** — Przetwarzanie obrazu i analiza wizualna w czasie rzeczywistym
- **[Pillow (PIL)](https://python-pillow.org/)** — Wczytywanie, konwersja i podstawowa edycja plików graficznych
- **[Pytest](https://docs.pytest.org/)** — Narzędzie do automatycznych testów jednostkowych i integracyjnych

## 📋 Wymagania systemowe

| Wymaganie | Szczegóły |
| :--- | :--- |
| **System operacyjny** | 💻 **Windows** (testowano na Windows 10 / 11) |
| **Wersja Pythona** | 🐍 **Python 3.12 – 3.14** (zalecana) |
| **Zależności** | 📦 Zarządzane przez plik `requirements.txt` (PySide6, NumPy, OpenCV, Pillow, Pytest) |

> ⚠️ **Uwaga:** Aplikacja **6FFECT** jest obecnie zaprojektowana i przetestowana wyłącznie dla systemu **Windows**. Wsparcie dla systemów macOS oraz Linux nie jest na ten moment dostępne.

### 📦 Opcje instalacji i uruchomienia

#### Opcja 1: Samodzielny plik wykonywalny (Najszybsza)
1. Pobierz plik `6FFECT.exe` z sekcji **Assets** poniżej.
2. *(Opcjonalnie)* Tymczasowo wyłącz lub dostosuj swój program antywirusowy, jeśli blokuje nieznane pliki wykonywalne.
3. Uruchom `6FFECT.exe` bezpośrednio — instalacja środowiska Python nie jest wymagana!

#### Opcja 2: Skrypt instalacyjny (Ze źródeł)
1. Pobierz i wypakuj archiwum **Source code (zip)** z sekcji Assets.
2. Uruchom plik `setup.bat`, aby automatycznie zainstalować zależności i otworzyć aplikację.

#### Opcja 3: Ręcznie przez terminal (Dla deweloperów)
1. Pobierz kod źródłowy:
   * **Przez Git:**
     ```bash
     git clone [https://github.com/kacper-milczarek-code/6FFECT.git](https://github.com/kacper-milczarek-code/6FFECT.git)
     ```
   * **Lub jako ZIP:** Pobierz i wypakuj **Source code (zip)** z sekcji Assets poniżej, a następnie otwórz wypakowany folder w terminalu.

2. Przejdź do folderu projektu w terminalu / PowerShellu:
   ```bash
   cd 6FFECT
      ```

3. Utwórz i aktywuj środowisko wirtualne:
   ```bash
   python -m venv venv
   ```
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

4. Zainstaluj wymagane zależności:
   ```bash
   pip install -r requirements.txt
   ```

5. Uruchom aplikację:
   ```bash
   python main.py
   ```

### 🔧 Rozwiązywanie problemów z uruchomieniem
1. Opóźnienie antywirusa: Jeśli Twój program antywirusowy zacznie skanować plik wykonywalny przy pierwszym uruchomieniu, poczekaj kilka sekund na zakończenie procesu.
2. Zablokowany plik: Jeśli aplikacja zostanie zablokowana lub poddana kwarantannie, znajdź ją w ustawieniach oprogramowania antywirusowego i wybierz "Przywróć / Dodaj do wyjątków".
3. Uruchomienie ręczne: Jeśli samodzielny plik wykonywalny (Opcja 1) nadal nie chce się uruchomić, spróbuj skonfigurować środowisko Pythona manualnie, zgodnie z krokami w Opcji 2 lub Opcji 3.
