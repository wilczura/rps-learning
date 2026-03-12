# Epic Rock-Paper-Scissors (RPS) Evolution 🚀

Ten projekt to podróż przez proces tworzenia gry w Pythonie — od prostej logiki w konsoli, przez podstawowe okno graficzne, aż po zaawansowaną produkcję z systemem cząsteczek, lektorem i efektami neonowymi.

Projekt został stworzony jako materiał dydaktyczny dla uczniów, aby pokazać ewolucję kodu i możliwości biblioteki `pygame`.

---

## 📂 Struktura Projektu

### [01 - Konsola](01_konsolowy/)
*   **Cel**: Zrozumienie podstaw logiki gry.
*   **Technologie**: `input()`, `random`, `if/else`.
*   **Opis**: Gra działa wyłącznie w terminalu. Gracz wpisuje swój wybór (1-3), a komputer losuje swój.

### [02 - Wizualny](02_wizualny/)
*   **Cel**: Pierwszy interfejs użytkownika (GUI).
*   **Technologie**: `pygame`, obsługa zdarzeń myszy.
*   **Opis**: Pojawia się okno gry, przyciski i tekst. Logika zostaje przeniesiona do środowiska graficznego.

### [03 - Poziom Epic](03_poziom_epic/) 🌟
*   **Cel**: Profesjonalny game-feel i zaawansowane systemy.
*   **Technologie**: Maszyna stanów, system cząsteczek, lektor, animacje delty czasu (`dt`), efekty typu "Shockwave" i "Flash".
*   **Funkcje**:
    *   **Announcer Pack**: Lektor komentujący każdy ruch.
    *   **Neon Particles**: Iskry i poświata przy każdym uderzeniu.
    *   **Health Bars**: Neonowe paski życia zamiast prostych punktów.
    *   **Combo System**: Nagradzanie serii zwycięstw.

---

## 🛠️ Jak uruchomić?

1.  Upewnij się, że masz zainstalowanego Pythona 3.
2.  Zainstaluj bibliotekę Pygame:
    ```bash
    pip install -r requirements.txt
    ```
3.  Uruchom wybraną wersję:
    ```bash
    python 03_poziom_epic/gra.py
    ```

---

---

## 💡 Czego uczy ten projekt?
1.  **Podstawy Programowania**: Typy danych, instrukcje warunkowe, pętle (patrz: `01_konsolowy`).
2.  **Modularność**: Rozdzielanie zasobów (`assets`) od logiki kodu (patrz: `03_poziom_epic`).
3.  **Animacja i VFX**: Delta time (`dt`), system cząsteczek i świecenie (patrz: `03_poziom_epic`).
4.  **Matematyka w Grach**: Praca z wektorami, randomizacja i czas fizyczny.

---
