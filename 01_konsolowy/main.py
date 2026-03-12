import pygame
import random
import asyncio

# =======================================================
# WERSJA PRZEGLĄDARKOWA (01_konsola - Symulacja)
# =======================================================
# Ponieważ 'input()' blokuje przeglądarkę, symulujemy konsolę w Pygame.

async def main():
    pygame.init()
    ekran = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("KPN: Poziom Konsolowy (Symulacja Web)")
    czcionka = pygame.font.SysFont("monospace", 20)
    
    log = [
        "Witaj w grze Kamień, Papier, Nożyce! ✊ ✋ ✌️",
        "Gramy do 5 wygranych!",
        "---------------------------------------",
        "KLIKNIJ PRZYCISK NA KLAWIATURZE:",
        "[1] Kamień, [2] Papier, [3] Nożyce",
        "---------------------------------------"
    ]
    
    punkty_gracza = 0
    punkty_komputera = 0
    opcje = ["kamien", "papier", "nozyce"]
    gra_trwa = True

    def add_to_log(msg):
        log.append(msg)
        if len(log) > 20: log.pop(0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            
            if gra_trwa and event.type == pygame.KEYDOWN:
                wybor_g = ""
                if event.key == pygame.K_1: wybor_g = "kamien"
                if event.key == pygame.K_2: wybor_g = "papier"
                if event.key == pygame.K_3: wybor_g = "nozyce"
                
                if wybor_g:
                    wybor_k = random.choice(opcje)
                    add_to_log(f"> Wybrałeś: {wybor_g.upper()}")
                    add_to_log(f"🤖 Komputer wybrał: {wybor_k.upper()}")
                    
                    if wybor_g == wybor_k:
                        add_to_log("REMIS! 🤝")
                    elif (wybor_g == "kamien" and wybor_k == "nozyce") or \
                         (wybor_g == "papier" and wybor_k == "kamien") or \
                         (wybor_g == "nozyce" and wybor_k == "papier"):
                        add_to_log("Punkt dla Ciebie! 🎉")
                        punkty_gracza += 1
                    else:
                        add_to_log("Punkt dla komputera! 💀")
                        punkty_komputera += 1
                    
                    add_to_log(f"WYNIK: Ty {punkty_gracza} - Komputer {punkty_komputera}")
                    add_to_log("-" * 30)
                    
                    if punkty_gracza >= 5 or punkty_komputera >= 5:
                        msg = "🎉 GRATULACJE! WYGRAŁEŚ MECZ! 🎉" if punkty_gracza >= 5 else "💻 KOMPUTER WYGRAŁ MECZ! 💻"
                        add_to_log(msg)
                        add_to_log("Naciśnij [SPACE] aby zagrać ponownie.")
                        gra_trwa = False
            
            elif not gra_trwa and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    punkty_gracza = 0; punkty_komputera = 0; gra_trwa = True
                    log.clear(); add_to_log("Nowy mecz rozpoczęty! Wybierz [1, 2, 3]")

        ekran.fill((20, 20, 25))
        for i, linia in enumerate(log):
            kolor = (0, 255, 0) if "WYGRAŁEŚ" in linia or "Ciebie" in linia else (255, 255, 255)
            if "KOMPUTER" in linia or "komputera" in linia: kolor = (255, 100, 100)
            surf = czcionka.render(linia, True, kolor)
            ekran.blit(surf, (20, 20 + i * 25))

        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
