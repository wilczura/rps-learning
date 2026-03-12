import pygame
import random
import sys
import os
import asyncio # Wymagane dla wersji przeglądarkowej (pygbag)

# =======================================================
# WERSJA PRZEGLĄDARKOWA (WEB) — main.py
# =======================================================
# Aby gra działała w przeglądarce, musimy użyć biblioteki 'asyncio'
# i upewnić się, że pętla gry nie blokuje przeglądarki.

async def main():
    pygame.init()
    pygame.mixer.init()

    SZEROKOSC = 1024
    WYSOKOSC = 768
    ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
    pygame.display.set_caption("RPS - EPIC FIGHT (WEB EDITION)")

    # --- KOLORY ---
    BIALY = (255, 255, 255)
    CZARNY = (0, 0, 0)
    SZARY = (100, 100, 100)
    CZERWONY = (255, 60, 60)
    ZIELONY = (60, 230, 90)
    ZNIEKSZTALCONY_GLOWNY = (245, 170, 0)
    CIEMNY_GLOWNY = (180, 110, 0)

    # --- CZCIONKI ---
    try:
        czcionka_duza = pygame.font.SysFont("impact", 65)
        czcionka_mala = pygame.font.SysFont("verdana", 24, bold=True)
    except:
        czcionka_duza = pygame.font.Font(None, 65)
        czcionka_mala = pygame.font.Font(None, 30)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def wczytaj_grafike(nazwa, rozmiar=None):
        sciezka = os.path.join(BASE_DIR, "assets", "images", nazwa)
        if os.path.exists(sciezka):
            img = pygame.image.load(sciezka).convert_alpha()
            if rozmiar: img = pygame.transform.scale(img, rozmiar)
            return img
        img = pygame.Surface(rozmiar if rozmiar else (150, 150), pygame.SRCALPHA)
        img.fill(SZARY)
        return img

    def wczytaj_dzwiek(nazwa, subfolder="sounds"):
        sciezka = os.path.join(BASE_DIR, "assets", subfolder, nazwa)
        if os.path.exists(sciezka):
            return pygame.mixer.Sound(sciezka)
        return None

    # Ładowanie Grafik
    img_tlo = wczytaj_grafike("bg.png", (SZEROKOSC, WYSOKOSC))
    grafiki_broni = {
        "Kamień": wczytaj_grafike("rock.png", (200, 200)),
        "Papier": wczytaj_grafike("paper.png", (200, 200)),
        "Nożyce": wczytaj_grafike("scissors.png", (200, 200))
    }

    # Ładowanie Dźwięków
    snd_hit = wczytaj_dzwiek("hit.wav")
    snd_win = wczytaj_dzwiek("win.wav")
    snd_lose = wczytaj_dzwiek("lose.wav")
    snd_click = wczytaj_dzwiek("click.wav")

    snd_lector = {
        "wybierz_bron": wczytaj_dzwiek("wybierz_bron.mp3", "lector"),
        "kamien": wczytaj_dzwiek("kamien.mp3", "lector"),
        "papier": wczytaj_dzwiek("papier.mp3", "lector"),
        "nozyce": wczytaj_dzwiek("nozyce.mp3", "lector"),
        "wygrywasz": wczytaj_dzwiek("wygrywasz.mp3", "lector"),
        "przegrywasz": wczytaj_dzwiek("przegrywasz.mp3", "lector"),
        "remis": wczytaj_dzwiek("remis.mp3", "lector"),
        "wygrales_caly_mecz": wczytaj_dzwiek("wygrales_caly_mecz.mp3", "lector"),
        "komputer_cie_zniszczyl": wczytaj_dzwiek("komputer_cie_zniszczyl.mp3", "lector")
    }

    glosnosc_bgm, glosnosc_sfx, glosnosc_lector = 0.3, 0.8, 1.0

    def aktualizuj_glosnosc_sfx():
        for s in [snd_hit, snd_win, snd_lose, snd_click]:
            if s: s.set_volume(glosnosc_sfx)

    def aktualizuj_glosnosc_lector():
        for s in snd_lector.values():
            if s: s.set_volume(glosnosc_lector)

    def wczytaj_losowe_odzywki():
        choice_dir = os.path.join(BASE_DIR, "assets", "lector", "choice")
        odzywki = []
        if os.path.exists(choice_dir):
            pliki = [f for f in os.listdir(choice_dir) if f.endswith(('.mp3', '.wav'))]
            for p in pliki:
                snd = pygame.mixer.Sound(os.path.join(choice_dir, p))
                odzywki.append(snd)
        return odzywki

    snd_choice_pool = wczytaj_losowe_odzywki()
    aktualizuj_glosnosc_sfx()
    aktualizuj_glosnosc_lector()

    sciezka_bgm = os.path.join(BASE_DIR, "assets", "sounds", "bgm.mp3")
    if os.path.exists(sciezka_bgm):
        pygame.mixer.music.load(sciezka_bgm)
        pygame.mixer.music.set_volume(glosnosc_bgm)
        pygame.mixer.music.play(-1)

    # --- KLASY EFEKTÓW ---
    class Czasteczka:
        def __init__(self, x, y, kolor):
            self.x, self.y = x, y
            self.vx, self.vy = random.uniform(-18, 18), random.uniform(-18, 18)
            self.zycie = 1.0
            self.kolor = kolor
        def aktualizuj(self, dt):
            self.x += self.vx
            self.y += self.vy
            self.zycie -= dt * 1.0
            return self.zycie > 0
        def rysuj(self, surf):
            alfa = int(self.zycie * 255)
            rozmiar = int(self.zycie * 12)
            c = list(self.kolor)
            g_surf = pygame.Surface((rozmiar*4, rozmiar*4), pygame.SRCALPHA)
            pygame.draw.circle(g_surf, (*c, alfa // 6), (rozmiar*2, rozmiar*2), rozmiar*2)
            surf.blit(g_surf, (self.x - rozmiar*2, self.y - rozmiar*2))
            p_surf = pygame.Surface((rozmiar, rozmiar), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*[(x+255)//2 for x in c], alfa), (rozmiar//2, rozmiar//2), rozmiar//2)
            surf.blit(p_surf, (self.x - rozmiar//2, self.y - rozmiar//2))

    class FalaUderzeniowa:
        def __init__(self, x, y, kolor):
            self.x, self.y = x, y
            self.promien = 10
            self.kolor = kolor
            self.zycie = 1.0
        def aktualizuj(self, dt):
            self.promien += 800 * dt
            self.zycie -= 2.0 * dt
            return self.zycie > 0
        def rysuj(self, surf):
            alfa = int(self.zycie * 200)
            s = pygame.Surface((int(self.promien*2), int(self.promien*2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.kolor, alfa), (int(self.promien), int(self.promien)), int(self.promien), 5)
            surf.blit(s, (self.x - self.promien, self.y - self.promien))

    lista_czasteczek = []
    lista_fal = []
    efekt_flash = 0

    def stworz_wybuch(x, y, kolor):
        for _ in range(80): lista_czasteczek.append(Czasteczka(x, y, kolor))
        lista_fal.append(FalaUderzeniowa(x, y, kolor))

    # --- LOGIKA GRY ---
    hp_gracza = hp_komputera = 5
    stan_gry = "MENU"
    wybor_gracza = wybor_komputera = None
    czas_animacji = 0
    zegar = pygame.time.Clock()
    wynik_rundy = ""
    kolor_wyniku = BIALY

    def rysuj_hud():
        pygame.draw.rect(ekran, (20, 20, 20), (50, 30, 300, 30), border_radius=5)
        pygame.draw.rect(ekran, ZIELONY, (52 + (296 - int(296*(hp_gracza/5))), 32, int(296*(hp_gracza/5)), 26), border_radius=5)
        pygame.draw.rect(ekran, (20, 20, 20), (SZEROKOSC - 350, 30, 300, 30), border_radius=5)
        pygame.draw.rect(ekran, CZERWONY, (SZEROKOSC - 348, 32, int(296*(hp_komputera/5)), 26), border_radius=5)

    def rysuj_przycisk(tekst, x, y, szer, wys):
        mysz, klik = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        r = pygame.Rect(x, y, szer, wys)
        h = r.collidepoint(mysz)
        pygame.draw.rect(ekran, (255, 200, 50) if h else ZNIEKSZTALCONY_GLOWNY, r, border_radius=15)
        t = czcionka_mala.render(tekst, True, BIALY)
        ekran.blit(t, t.get_rect(center=r.center))
        if h and klik[0]:
            pygame.time.delay(100)
            return True
        return False

    if snd_lector["wybierz_bron"]: snd_lector["wybierz_bron"].play()

    # --- PĘTLA GŁÓWNA (ASYNC) ---
    while True:
        # DT musi być obliczane w każdej klatce
        dt = zegar.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return

        ekran.fill((30, 40, 50))
        ekran.blit(img_tlo, (0, 0))

        # Efekty
        for f in lista_fal[:]:
            if not f.aktualizuj(dt): lista_fal.remove(f)
            else: f.rysuj(ekran)
        for p in lista_czasteczek[:]:
            if not p.aktualizuj(dt): lista_czasteczek.remove(p)
            else: p.rysuj(ekran)
        
        if efekt_flash > 0:
            s_f = pygame.Surface((SZEROKOSC, WYSOKOSC))
            s_f.fill(BIALY); s_f.set_alpha(int(efekt_flash))
            ekran.blit(s_f, (0, 0))
            efekt_flash = max(0, efekt_flash - 1000 * dt)

        rysuj_hud()

        if stan_gry == "MENU":
            label = czcionka_duza.render("WYBIERZ SWOJĄ BROŃ!", True, BIALY)
            ekran.blit(label, (SZEROKOSC//2 - label.get_width()//2, 110))
            if rysuj_przycisk("KAMIEŃ", 100, 500, 200, 60):
                wybor_gracza, wybor_komputera = "Kamień", random.choice(opcje)
                snd_lector["kamien"].play(); stan_gry = "ANIMACJA"; czas_animacji = 0
            if rysuj_przycisk("PAPIER", 412, 500, 200, 60):
                wybor_gracza, wybor_komputera = "Papier", random.choice(opcje)
                snd_lector["papier"].play(); stan_gry = "ANIMACJA"; czas_animacji = 0
            if rysuj_przycisk("NOŻYCE", 724, 500, 200, 60):
                wybor_gracza, wybor_komputera = "Nożyce", random.choice(opcje)
                snd_lector["nozyce"].play(); stan_gry = "ANIMACJA"; czas_animacji = 0

        elif stan_gry == "ANIMACJA":
            czas_animacji += dt
            ekran.blit(grafiki_broni[wybor_gracza], (SZEROKOSC//2 - 250, WYSOKOSC//2 - 100))
            ekran.blit(pygame.transform.flip(grafiki_broni[wybor_komputera], True, False), (SZEROKOSC//2 + 50, WYSOKOSC//2 - 100))
            if 0.8 < czas_animacji < 1.0 and len(lista_fal) == 0:
                snd_hit.play(); stworz_wybuch(SZEROKOSC//2, WYSOKOSC//2, BIALY); efekt_flash = 255
            if czas_animacji > 1.5:
                # Wynik
                if wybor_gracza == wybor_komputera: 
                    wynik_rundy, kolor_wyniku = "REMIS!", BIALY; snd_lector["remis"].play()
                elif (wybor_gracza == "Kamień" and wybor_komputera == "Nożyce") or \
                     (wybor_gracza == "Papier" and wybor_komputera == "Kamień") or \
                     (wybor_gracza == "Nożyce" and wybor_komputera == "Papier"):
                    wynik_rundy, kolor_wyniku = "WYGRANA!", ZIELONY; snd_lector["wygrywasz"].play(); hp_komputera -= 1
                else:
                    wynik_rundy, kolor_wyniku = "PRZEGRANA...", CZERWONY; snd_lector["przegrywasz"].play(); hp_gracza -= 1
                stan_gry = "WYNIK"; czas_animacji = 0

        elif stan_gry == "WYNIK":
            czas_animacji += dt
            txt = czcionka_duza.render(wynik_rundy, True, kolor_wyniku)
            ekran.blit(txt, txt.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 250)))
            if czas_animacji > 2.0:
                if hp_gracza <= 0 or hp_komputera <= 0: stan_gry = "KONIEC"
                else: 
                    stan_gry = "MENU"
                    if snd_choice_pool: random.choice(snd_choice_pool).play()
                    else: snd_lector["wybierz_bron"].play()

        elif stan_gry == "KONIEC":
            msg = "KONIEC WALKI!"
            txt = czcionka_duza.render(msg, True, ZIELONY if hp_gracza > 0 else CZERWONY)
            ekran.blit(txt, txt.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2)))
            if rysuj_przycisk("OD NOWA", SZEROKOSC//2 - 100, WYSOKOSC//2 + 100, 200, 60):
                hp_gracza = hp_komputera = 5; stan_gry = "MENU"

        pygame.display.flip()
        
        # BARDZO WAŻNE: To pozwala przeglądarce "odetchnąć" i obsłużyć inne rzeczy.
        # Bez tego gra by się zamroziła.
        await asyncio.sleep(0)

# Uruchomienie wersji Web
asyncio.run(main())
