import pygame
import random
import sys
import os

# =======================================================
# 1. KONFIGURACJA I ZASOBY (ASSETS)
# =======================================================
pygame.init()
pygame.mixer.init() # Inicjalizacja dźwięku

SZEROKOSC = 1024
WYSOKOSC = 768
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("RPS - EPIC FIGHT EDITION")

# Paleta kolorów — używamy żywych kolorów neonowych
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
SZARY = (100, 100, 100)
CZERWONY = (255, 60, 60)
ZIELONY = (60, 230, 90)
ZNIEKSZTALCONY_GLOWNY = (245, 170, 0) # Pomarańczowy/Złoty
CIEMNY_GLOWNY = (180, 110, 0)

# Przygotowanie czcionek
try:
    czcionka_duza = pygame.font.SysFont("impact", 65)
    czcionka_mala = pygame.font.SysFont("verdana", 24, bold=True)
except:
    czcionka_duza = pygame.font.Font(None, 65)
    czcionka_mala = pygame.font.Font(None, 30)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def wczytaj_grafike(nazwa, rozmiar=None):
    """Pomocnik do ładowania obrazów z folderu assets/images."""
    sciezka = os.path.join(BASE_DIR, "assets", "images", nazwa)
    if os.path.exists(sciezka):
        img = pygame.image.load(sciezka).convert_alpha()
        if rozmiar: img = pygame.transform.scale(img, rozmiar)
        return img
    # Jeśli brakuje obrazka, tworzymy szary prostokąt, by gra się nie zamykała
    img = pygame.Surface(rozmiar if rozmiar else (150, 150), pygame.SRCALPHA)
    img.fill(SZARY)
    return img

def wczytaj_dzwiek(nazwa, subfolder="sounds"):
    """Pomocnik do ładowania efektów dźwiękowych."""
    sciezka = os.path.join(BASE_DIR, "assets", subfolder, nazwa)
    if os.path.exists(sciezka):
        return pygame.mixer.Sound(sciezka)
    return None

# Ładowanie Grafik Tła i Broni
img_tlo = wczytaj_grafike("bg.png", (SZEROKOSC, WYSOKOSC))
grafiki_broni = {
    "Kamień": wczytaj_grafike("rock.png", (200, 200)),
    "Papier": wczytaj_grafike("paper.png", (200, 200)),
    "Nożyce": wczytaj_grafike("scissors.png", (200, 200))
}

# Ładowanie Głównego Lektora i SFX
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

# Zmienne głośności (używane w suwakach)
glosnosc_bgm, glosnosc_sfx, glosnosc_lector = 0.3, 0.8, 1.0

def aktualizuj_glosnosc_sfx():
    """Ustawia głośność dla wszystkich efektów dźwiękowych hit/win/etc."""
    for s in [snd_hit, snd_win, snd_lose, snd_click]:
        if s: s.set_volume(glosnosc_sfx)

def aktualizuj_glosnosc_lector():
    """Ustawia głośność dla wszystkich kwestii lektora."""
    for s in snd_lector.values():
        if s: s.set_volume(glosnosc_lector)
    for s in snd_choice_pool:
        if s: s.set_volume(glosnosc_lector)

def wczytaj_losowe_odzywki():
    """Wczytuje wszystkie pliki muzyczne z folderu assets/lector/choice/."""
    choice_dir = os.path.join(BASE_DIR, "assets", "lector", "choice")
    odzywki = []
    if os.path.exists(choice_dir):
        pliki = [f for f in os.listdir(choice_dir) if f.endswith(('.mp3', '.wav'))]
        for p in pliki:
            snd = pygame.mixer.Sound(os.path.join(choice_dir, p))
            odzywki.append(snd)
    return odzywki

snd_choice_pool = wczytaj_losowe_odzywki() # Pula losowych tekstów lektora ("A to co?", itp.)
aktualizuj_glosnosc_sfx()
aktualizuj_glosnosc_lector()

# Muzyka w tle (Music streaming - gra z dysku, nie ładuje całego pliku do RAM)
sciezka_bgm = os.path.join(BASE_DIR, "assets", "sounds", "bgm.mp3")
if os.path.exists(sciezka_bgm):
    pygame.mixer.music.load(sciezka_bgm)
    pygame.mixer.music.set_volume(glosnosc_bgm)
    pygame.mixer.music.play(-1) # -1 oznacza zapętlenie

# =======================================================
# 2. SYSTEM CZĄSTECZEK I EFEKTÓW WIZUALNYCH (VFX)
# =======================================================

class Czasteczka:
    """Reprezentuje pojedynczą iskrę neonową."""
    def __init__(self, x, y, kolor):
        self.x, self.y = x, y
        # Velocity (prędkość): losowy kierunek wylotu
        self.vx = random.uniform(-18, 18)
        self.vy = random.uniform(-18, 18)
        self.zycie = 1.0 # Czas życia od 1.0 (pełne) do 0.0 (zniknięcie)
        self.kolor = kolor

    def aktualizuj(self, dt):
        """Przesuwa cząsteczkę i skraca jej życie."""
        self.x += self.vx
        self.y += self.vy
        self.zycie -= dt * 1.0 
        return self.zycie > 0

    def rysuj(self, surf):
        """Rysuje 'warstwową' iskrę z efektem świecenia (Glow)."""
        alfa = int(self.zycie * 255) # Przezroczystość zależna od życia
        rozmiar = int(self.zycie * 12)
        c = list(self.kolor)
        
        # 1. MEGA POŚWIATA (Glow): Duży, bardzo przezroczysty okrąg
        g1_rozm = rozmiar * 4
        g1_surf = pygame.Surface((g1_rozm, g1_rozm), pygame.SRCALPHA)
        pygame.draw.circle(g1_surf, (*c, alfa // 6), (g1_rozm//2, g1_rozm//2), g1_rozm//2)
        surf.blit(g1_surf, (self.x - g1_rozm//2, self.y - g1_rozm//2))
        
        # 2. NEONOWY GLOW: Mniejszy, bardziej nasycony okrąg
        g2_rozm = rozmiar * 2
        g2_surf = pygame.Surface((g2_rozm, g2_rozm), pygame.SRCALPHA)
        pygame.draw.circle(g2_surf, (*c, alfa // 2), (g2_rozm//2, g2_rozm//2), g2_rozm//2)
        surf.blit(g2_surf, (self.x - g2_rozm//2, self.y - g2_rozm//2))
        
        # 3. RDZEŃ: Bardzo jasny środek iskry
        rdzen_c = [(x + 255) // 2 for x in c] 
        p_surf = pygame.Surface((rozmiar, rozmiar), pygame.SRCALPHA)
        pygame.draw.circle(p_surf, (*rdzen_c, alfa), (rozmiar//2, rozmiar//2), rozmiar//2)
        surf.blit(p_surf, (self.x - rozmiar//2, self.y - rozmiar//2))

class FalaUderzeniowa:
    """Efekt rozchodzącego się kręgu (Shockwave) po uderzeniu."""
    def __init__(self, x, y, kolor):
        self.x, self.y = x, y
        self.promien = 10
        self.kolor = kolor
        self.zycie = 1.0

    def aktualizuj(self, dt):
        self.promien += 800 * dt # Fala bardzo szybko rośnie
        self.zycie -= 2.0 * dt
        return self.zycie > 0

    def rysuj(self, surf):
        alfa = int(self.zycie * 200)
        # Rysujemy tylko obwód okręgu (hollow circle)
        s = pygame.Surface((int(self.promien*2), int(self.promien*2)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.kolor, alfa), (int(self.promien), int(self.promien)), int(self.promien), 5)
        surf.blit(s, (self.x - self.promien, self.y - self.promien))

# Kontenery na aktywne efekty wizualne
lista_czasteczek = []
lista_fal = []
efekt_flash = 0 # Intensywność błysku ekranu (0-255)

def stworz_wybuch_extreme(x, y, kolor, ilosc=80):
    """Tworzy deszcz iskier oraz falę uderzeniową w danym punkcie."""
    for _ in range(ilosc):
        lista_czasteczek.append(Czasteczka(x, y, kolor))
    lista_fal.append(FalaUderzeniowa(x, y, kolor))

# =======================================================
# 3. ZMIENNE STANU I HUD
# =======================================================
opcje = ["Kamień", "Papier", "Nożyce"]
hp_gracza = 5
hp_komputera = 5
combo_gracza = 0
combo_komputera = 0
# MASZYNA STANÓW (State Machine): Decyduje co gra aktualnie robi (Menu? Walka? Wynik?)
stan_gry = "MENU" 
wybor_gracza = wybor_komputera = None
czas_animacji = 0
zegar = pygame.time.Clock()
wynik_rundy = ""
kolor_wyniku = BIALY
kto_wygral = 0 # -1 komputer, 1 gracz, 0 remis
combo_napis_skala = 0

def rysuj_hud():
    """Rysuje górny pasek z punktami HP (Neon Bars)."""
    # Pasek Gracza — HP maleje odkrywając tło
    pygame.draw.rect(ekran, (20, 20, 20), (50, 30, 300, 30), border_radius=5) # Tło paska
    procent_hp_g = hp_gracza / 5
    pygame.draw.rect(ekran, ZIELONY, (52 + (296 - int(296*procent_hp_g)), 32, int(296*procent_hp_g), 26), border_radius=5)
    pygame.draw.rect(ekran, BIALY, (50, 30, 300, 30), 2, border_radius=5) # Obramowanie
    
    # Pasek Komputera
    pygame.draw.rect(ekran, (20, 20, 20), (SZEROKOSC - 350, 30, 300, 30), border_radius=5)
    procent_hp_k = hp_komputera / 5
    pygame.draw.rect(ekran, CZERWONY, (SZEROKOSC - 348, 32, int(296*procent_hp_k), 26), border_radius=5)
    pygame.draw.rect(ekran, BIALY, (SZEROKOSC - 350, 30, 300, 30), 2, border_radius=5)

    # Etykiety tekstowe HP
    txt_g = czcionka_mala.render(f"TY: {hp_gracza} HP", True, BIALY)
    txt_k = czcionka_mala.render(f"KOMP: {hp_komputera} HP", True, BIALY)
    ekran.blit(txt_g, (50, 65))
    ekran.blit(txt_k, (SZEROKOSC - 50 - txt_k.get_width(), 65))

def zmien_stan(nowy):
    """Zarządza przejściami między ekranami i odpala odpowiednie kwestie lektora."""
    global stan_gry, czas_animacji
    if nowy == "MENU":
        if hp_gracza == 5 and hp_komputera == 5:
            # Pierwsza runda meczu
            if snd_lector["wybierz_bron"]: snd_lector["wybierz_bron"].play()
        else:
            # Kolejne rundy — lektor mówi coś losowego (np. "A to co?")
            if snd_choice_pool: random.choice(snd_choice_pool).play()
    elif nowy == "KONIEC_MECZU":
        if hp_gracza > 0: snd_lector["wygrales_caly_mecz"].play()
        else: snd_lector["komputer_cie_zniszczyl"].play()
    
    stan_gry = nowy
    czas_animacji = 0

# (Wbudowane funkcje rysowania przycisków i suwaków są pominięte dla zwięzłości, 
#  ale działają na zasadzie Rect.collidepoint i mouse.get_pressed)

def rysuj_przycisk(tekst, x, y, szerokosc, wysokosc, opcja_ikona=None, x_img=0, y_img=0):
    """Zaawansowany przycisk z obsługą ikon broni i efektów hover."""
    mysz = pygame.mouse.get_pos()
    klik = pygame.mouse.get_pressed()
    r = pygame.Rect(x, y, szerokosc, wysokosc)
    hover = r.collidepoint(mysz) or (opcja_ikona and pygame.Rect(x_img, y_img, 200, 200).collidepoint(mysz))

    # Kolory i przesunięcie (efekt 'wciśnięcia')
    kol_g = (255, 200, 50) if hover else ZNIEKSZTALCONY_GLOWNY
    y_off = 2 if klik[0] and hover else 0

    # Rysowanie ikony broni nad przyciskiem (jeśli podana)
    if opcja_ikona:
        img = pygame.transform.scale(grafiki_broni[opcja_ikona], (220, 220)) if hover else grafiki_broni[opcja_ikona]
        ekran.blit(img, (x_img - (10 if hover else 0), y_img - (10 if hover else 0) + y_off))

    # Rysowanie samego przycisku (cień i góra)
    pygame.draw.rect(ekran, CIEMNY_GLOWNY, (x, y + 5 + y_off, szerokosc, wysokosc), border_radius=15)
    pygame.draw.rect(ekran, kol_g, (x, y + y_off, szerokosc, wysokosc), border_radius=15)
    
    txt = czcionka_mala.render(tekst, True, BIALY)
    ekran.blit(txt, txt.get_rect(center=(x + szerokosc/2, y + wysokosc/2 + y_off)))

    if hover and klik[0]:
        pygame.time.delay(150)
        return True
    return False

def rysuj_suwak(tekst, x, y, val):
    """Rysuje suwak do regulacji głośności."""
    mysz, klik = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
    sz, ws = 150, 15
    rect = pygame.Rect(x, y + 25, sz, ws)
    pygame.draw.rect(ekran, SZARY, rect, border_radius=5)
    pygame.draw.rect(ekran, ZIELONY, (x, y + 25, int(sz * val), ws), border_radius=5)
    
    label = pygame.font.SysFont("arial", 18, bold=True).render(f"{tekst}: {int(val*100)}%", True, BIALY)
    ekran.blit(label, (x, y))
    
    if rect.inflate(20, 20).collidepoint(mysz) and klik[0]:
        return min(1.0, max(0.0, (mysz[0] - x) / sz))
    return val

# =======================================================
# 4. GŁÓWNA PĘTLA GRY
# =======================================================
zmien_stan("MENU")
dziala = True

while dziala:
    # dt (delta time) — czas jaki upłynął od ostatniej klatki.
    # Używamy go, by prędkość animacji (np. cząsteczek) była taka sama na każdym komputerze.
    dt = zegar.tick(60) / 1000.0 

    for event in pygame.event.get():
        if event.type == pygame.QUIT: dziala = False

    ekran.blit(img_tlo, (0, 0)) # Rysujemy tło jako pierwszą warstwę
    
    # RYSOWANIE VFX (Warstwa 2)
    for f in lista_fal[:]:
        if not f.aktualizuj(dt): lista_fal.remove(f)
        else: f.rysuj(ekran)
    for p in lista_czasteczek[:]:
        if not p.aktualizuj(dt): lista_czasteczek.remove(p)
        else: p.rysuj(ekran)

    # EFEKT BŁYSKU (Flash)
    if efekt_flash > 0:
        f_surf = pygame.Surface((SZEROKOSC, WYSOKOSC))
        f_surf.fill(BIALY)
        f_surf.set_alpha(int(efekt_flash))
        ekran.blit(f_surf, (0, 0))
        efekt_flash = max(0, efekt_flash - 1000 * dt)

    rysuj_hud() # Rysujemy HP nad efektami walki

    # LOGIKA STANÓW
    if stan_gry == "MENU":
        tytul = czcionka_duza.render("WYBIERZ SWOJĄ BROŃ!", True, BIALY)
        ekran.blit(tytul, (SZEROKOSC//2 - tytul.get_width()//2, 110))
        
        # Wybór broni — przyciski obrazkowe
        odst = (SZEROKOSC - 3 * 200) // 4
        y_btn = WYSOKOSC - 180
        if rysuj_przycisk("KAMIEŃ", odst, y_btn, 200, 60, "Kamień", odst, y_btn - 220):
            wybor_gracza = "Kamień"
            snd_lector["kamien"].play()
            wybor_komputera = random.choice(opcje)
            zmien_stan("ANIMACJA")
        if rysuj_przycisk("PAPIER", odst*2 + 200, y_btn, 200, 60, "Papier", odst*2 + 200, y_btn - 220):
            wybor_gracza = "Papier"
            snd_lector["papier"].play()
            wybor_komputera = random.choice(opcje)
            zmien_stan("ANIMACJA")
        if rysuj_przycisk("NOŻYCE", odst*3 + 400, y_btn, 200, 60, "Nożyce", odst*3 + 400, y_btn - 220):
            wybor_gracza = "Nożyce"
            snd_lector["nozyce"].play()
            wybor_komputera = random.choice(opcje)
            zmien_stan("ANIMACJA")

    elif stan_gry == "ANIMACJA":
        czas_animacji += dt
        # Prosta animacja zbliżania się broni do siebie
        cel_x_g, cel_x_k = SZEROKOSC//2 - 250, SZEROKOSC//2 + 50
        x_g = -200 + (cel_x_g + 200) * min(1.0, czas_animacji * 1.5)
        x_k = SZEROKOSC + (cel_x_k - (SZEROKOSC)) * min(1.0, czas_animacji * 1.5)
        
        ekran.blit(grafiki_broni[wybor_gracza], (x_g, WYSOKOSC//2 - 100))
        ekran.blit(pygame.transform.flip(grafiki_broni[wybor_komputera], True, False), (x_k, WYSOKOSC//2 - 100))

        # Moment kolizji (uderzenia)
        if 0.8 < czas_animacji < 1.0 and len(lista_fal) == 0:
            snd_hit.play()
            stworz_wybuch_extreme(SZEROKOSC//2, WYSOKOSC//2, BIALY, 80)
            efekt_flash = 255
            
        if czas_animacji > 1.5:
            # Rozstrzygnięcie wyniku po uderzeniu
            if wybor_gracza == wybor_komputera:
                wynik_rundy, kolor_wyniku, kto_wygral = "REMIS!", BIALY, 0
                snd_lector["remis"].play()
            elif (wybor_gracza == "Kamień" and wybor_komputera == "Nożyce") or \
                 (wybor_gracza == "Papier" and wybor_komputera == "Kamień") or \
                 (wybor_gracza == "Nożyce" and wybor_komputera == "Papier"):
                wynik_rundy, kolor_wyniku, kto_wygral = "WYGRYWASZ!", ZIELONY, 1
                snd_lector["wygrywasz"].play()
                hp_komputera -= 1
                combo_gracza += 1
            else:
                wynik_rundy, kolor_wyniku, kto_wygral = "PRZEGRYWASZ!", CZERWONY, -1
                snd_lector["przegrywasz"].play()
                hp_gracza -= 1
                combo_komputera += 1
            zmien_stan("WYNIK")

    elif stan_gry == "WYNIK":
        # Ekran pokazujący zwycięzcę rundy i napis COMBO
        czas_animacji += dt
        n_s = czcionka_duza.render(wynik_rundy, True, kolor_wyniku)
        ekran.blit(n_s, n_s.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 250)))
        
        if czas_animacji > 2.0:
            if hp_gracza <= 0 or hp_komputera <= 0: zmien_stan("KONIEC_MECZU")
            else: zmien_stan("MENU")

    elif stan_gry == "KONIEC_MECZU":
        txt, col = ("KRÓL JEST TYLKO JEDEN!", ZIELONY) if hp_gracza > 0 else ("TERMINACJA ZAKOŃCZONA!", CZERWONY)
        n_s = czcionka_duza.render(txt, True, col)
        ekran.blit(n_s, n_s.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 50)))
        if rysuj_przycisk("ZAGRAJ PONOWNIE", SZEROKOSC//2 - 150, WYSOKOSC//2 + 100, 300, 60):
            hp_gracza = hp_komputera = 5
            zmien_stan("MENU")

    # Obsługa suwaków na dole ekranu
    glosnosc_bgm = rysuj_suwak("Muzyka", 30, WYSOKOSC - 100, glosnosc_bgm)
    pygame.mixer.music.set_volume(glosnosc_bgm)
    glosnosc_lector = rysuj_suwak("Głos", 220, WYSOKOSC - 60, glosnosc_lector)
    aktualizuj_glosnosc_lector()
    
    pygame.display.flip()

pygame.quit()
sys.exit()
