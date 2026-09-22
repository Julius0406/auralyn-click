from __future__ import annotations

import os

# The first entry follows the operating system locale.
LANGUAGES: list[tuple[str, str]] = [
    ("system", "System / Auto"),
    ("de", "Deutsch"),
    ("en", "English"),
    ("fr", "Français"),
    ("es", "Español"),
    ("it", "Italiano"),
    ("pt", "Português"),
    ("nl", "Nederlands"),
    ("pl", "Polski"),
    ("cs", "Čeština"),
    ("sk", "Slovenčina"),
    ("hu", "Magyar"),
    ("ro", "Română"),
    ("sv", "Svenska"),
    ("no", "Norsk"),
    ("da", "Dansk"),
    ("fi", "Suomi"),
    ("tr", "Türkçe"),
    ("ru", "Русский"),
    ("uk", "Українська"),
    ("el", "Ελληνικά"),
    ("ja", "日本語"),
    ("ko", "한국어"),
    ("zh", "中文"),
    ("ar", "العربية"),
]

SUPPORTED_CODES = {code for code, _ in LANGUAGES}

EN = {
    "startup_tagline": "Smooth. Fast. Yours.",
    "display_design": "Display & Design",
    "language": "Language",
    "system_default": "System default",
    "language_note": "The default follows your operating system language.",
    "apply_restart": "Apply language & restart",
    "look": "Look",
    "theme": "Theme",
    "accent": "Accent",
    "background": "Background",
    "custom_background": "Choose custom image / GIF",
    "motion_quality": "Motion & Quality",
    "animations": "Enable animations",
    "background_fps": "Background FPS",
    "ui_size": "UI size",
    "smooth_scrolling": "Smooth scrolling mode",
    "smooth_scrolling_note": "Pauses expensive decorative animation while you scroll, then resumes automatically.",
    "start_screen": "Start Screen",
    "mode": "Mode",
    "duration": "Duration",
    "fullscreen": "Fullscreen",
    "compact": "Compact",
    "off": "Off",
    "startup_note": "The start screen automatically uses your selected theme and background.",
    "monitor": "Monitor",
    "monitor_note": "Choose which monitor shows the start screen and the main Auralyn Click window.",
    "quality": "Quality",
    "quality_note": "Native Qt 6 UI • High-DPI • animated backgrounds • single instance • local settings",
    "app_subtitle": "animated desktop auto clicker • By Julius",
    "timing": "Timing",
    "timing_subtitle": "Choose an interval or direct CPS. Minimum stays at 1 ms.",
    "interval": "Interval",
    "cps": "CPS",
    "hours": "Hours",
    "minutes": "Minutes",
    "seconds": "Seconds",
    "milliseconds": "Millisec.",
    "target_cps": "Target CPS",
    "click_style": "Click Style",
    "mouse_button": "Mouse button",
    "left": "Left",
    "right": "Right",
    "middle": "Middle",
    "click_type": "Click type",
    "hold_per_click": "Hold per click",
    "session": "Session",
    "session_subtitle": "Start delay, limits and repetition.",
    "infinite": "Infinite until F6 / F8",
    "actions": "Actions",
    "pause": "Pause",
    "start_delay": "Start delay",
    "time_limit": "Time limit",
    "position_randomness": "Position & Randomness",
    "fixed_position": "Fixed cursor position",
    "capture_position": "Capture position • F7",
    "random_delay": "Random delay ±",
    "random_radius": "Random position radius",
    "burst_mode": "Burst Mode",
    "burst_subtitle": "Clicks in batches, then pauses before continuing.",
    "burst_active": "Enable burst",
    "live_control": "Live Control",
    "start": "START • F6",
    "stop_toggle": "STOP • F6",
    "stop_emergency": "EMERGENCY STOP • F8",
    "clicks": "CLICKS",
    "time": "TIME",
    "quick_presets": "Quick Presets",
    "global_hotkeys": "Global Hotkeys",
    "hk_start_stop": "F6   Start / Stop",
    "hk_position": "F7   Capture position",
    "hk_stop": "F8   Emergency stop (stop only)",
    "status_ready": "READY",
    "status_active": "ACTIVE",
    "status_stopped": "STOPPED",
    "status_finished": "FINISHED",
    "status_error": "ERROR",
    "status_preset": "PRESET LOADED",
    "custom_dialog": "Custom Background",
    "custom_dialog_filter": "Images / GIF (*.png *.jpg *.jpeg *.webp *.gif)",
}

DE = {
    "startup_tagline": "Smooth. Schnell. Deins.",
    "display_design": "Anzeige & Design",
    "language": "Sprache",
    "system_default": "Systemsprache",
    "language_note": "Standardmäßig wird automatisch die Sprache deines Systems benutzt.",
    "apply_restart": "Sprache anwenden & neu starten",
    "look": "Aussehen",
    "theme": "Theme",
    "accent": "Akzent",
    "background": "Hintergrund",
    "custom_background": "Eigenes Bild / GIF auswählen",
    "motion_quality": "Animation & Qualität",
    "animations": "Animationen aktiv",
    "background_fps": "Hintergrund-FPS",
    "ui_size": "UI-Größe",
    "smooth_scrolling": "Flüssiges Scrollen",
    "smooth_scrolling_note": "Pausiert aufwendige Deko-Animationen beim Scrollen und setzt sie danach automatisch fort.",
    "start_screen": "Startbildschirm",
    "mode": "Modus",
    "duration": "Dauer",
    "fullscreen": "Vollbild",
    "compact": "Klein",
    "off": "Aus",
    "startup_note": "Der Startbildschirm verwendet automatisch dein ausgewähltes Theme und deinen Hintergrund.",
    "monitor": "Monitor",
    "monitor_note": "Wähle, auf welchem Monitor der Startbildschirm und das Hauptfenster erscheinen.",
    "quality": "Qualität",
    "quality_note": "Native Qt-6-UI • High-DPI • animierte Hintergründe • Single-Instance • lokale Einstellungen",
    "app_subtitle": "animierter Desktop-Autoclicker • By Julius",
    "timing": "Timing",
    "timing_subtitle": "Intervall oder direkt CPS wählen. Minimum bleibt 1 ms.",
    "interval": "Intervall",
    "cps": "CPS",
    "hours": "Stunden",
    "minutes": "Minuten",
    "seconds": "Sekunden",
    "milliseconds": "Millisek.",
    "target_cps": "Ziel-CPS",
    "click_style": "Klickstil",
    "mouse_button": "Maustaste",
    "left": "Links",
    "right": "Rechts",
    "middle": "Mitte",
    "click_type": "Klicktyp",
    "hold_per_click": "Pro Klick gedrückt halten",
    "session": "Sitzung",
    "session_subtitle": "Startverzögerung, Limits und Wiederholung.",
    "infinite": "Unendlich bis F6 / F8",
    "actions": "Aktionen",
    "pause": "Pause",
    "start_delay": "Startverzögerung",
    "time_limit": "Zeitlimit",
    "position_randomness": "Position & Zufall",
    "fixed_position": "Feste Cursorposition",
    "capture_position": "Position übernehmen • F7",
    "random_delay": "Zufällige Verzögerung ±",
    "random_radius": "Zufälliger Positionsradius",
    "burst_mode": "Burst-Modus",
    "burst_subtitle": "Klickt in Paketen und macht danach eine Pause.",
    "burst_active": "Burst aktiv",
    "live_control": "Live-Steuerung",
    "start": "START • F6",
    "stop_toggle": "STOPPEN • F6",
    "stop_emergency": "NOT-AUS • F8",
    "clicks": "KLICKS",
    "time": "ZEIT",
    "quick_presets": "Schnell-Presets",
    "global_hotkeys": "Globale Hotkeys",
    "hk_start_stop": "F6   Start / Stop",
    "hk_position": "F7   Position übernehmen",
    "hk_stop": "F8   Not-Aus (nur stoppen)",
    "status_ready": "BEREIT",
    "status_active": "AKTIV",
    "status_stopped": "GESTOPPT",
    "status_finished": "FERTIG",
    "status_error": "FEHLER",
    "status_preset": "PRESET GELADEN",
    "custom_dialog": "Eigener Hintergrund",
    "custom_dialog_filter": "Bilder / GIF (*.png *.jpg *.jpeg *.webp *.gif)",
}

# Additional language packs intentionally reuse English for technical terms that are
# commonly used as-is (CPS, FPS, Burst, Theme). Every pack still translates the
# navigation, settings, main controls and the most visible labels.
PACKS = {
    "fr": {"display_design":"Affichage & design","language":"Langue","system_default":"Langue du système","apply_restart":"Appliquer la langue et redémarrer","look":"Apparence","accent":"Accent","background":"Arrière-plan","custom_background":"Choisir une image / GIF","motion_quality":"Animation & qualité","animations":"Activer les animations","ui_size":"Taille de l’interface","smooth_scrolling":"Défilement fluide","start_screen":"Écran de démarrage","fullscreen":"Plein écran","compact":"Compact","off":"Désactivé","timing":"Temporisation","interval":"Intervalle","hours":"Heures","minutes":"Minutes","seconds":"Secondes","milliseconds":"Millisecondes","click_style":"Style de clic","mouse_button":"Bouton de souris","left":"Gauche","right":"Droite","middle":"Milieu","click_type":"Type de clic","session":"Session","infinite":"Infini jusqu’à F6 / F8","actions":"Actions","start_delay":"Délai de démarrage","time_limit":"Limite de temps","fixed_position":"Position fixe du curseur","capture_position":"Capturer la position • F7","live_control":"Contrôle en direct","start":"DÉMARRER • F6","stop_emergency":"ARRÊT D’URGENCE • F8","quick_presets":"Préréglages rapides","global_hotkeys":"Raccourcis globaux","status_ready":"PRÊT","status_active":"ACTIF","status_stopped":"ARRÊTÉ","status_finished":"TERMINÉ","status_error":"ERREUR"},
    "es": {"display_design":"Pantalla y diseño","language":"Idioma","system_default":"Idioma del sistema","apply_restart":"Aplicar idioma y reiniciar","look":"Apariencia","accent":"Acento","background":"Fondo","custom_background":"Elegir imagen / GIF","motion_quality":"Movimiento y calidad","animations":"Activar animaciones","ui_size":"Tamaño de interfaz","smooth_scrolling":"Desplazamiento fluido","start_screen":"Pantalla de inicio","fullscreen":"Pantalla completa","compact":"Compacto","off":"Desactivado","timing":"Temporización","interval":"Intervalo","hours":"Horas","minutes":"Minutos","seconds":"Segundos","milliseconds":"Miliseg.","click_style":"Estilo de clic","mouse_button":"Botón del ratón","left":"Izquierdo","right":"Derecho","middle":"Central","click_type":"Tipo de clic","session":"Sesión","infinite":"Infinito hasta F6 / F8","actions":"Acciones","start_delay":"Retraso de inicio","time_limit":"Límite de tiempo","fixed_position":"Posición fija del cursor","capture_position":"Capturar posición • F7","live_control":"Control en vivo","start":"INICIAR • F6","stop_emergency":"PARADA DE EMERGENCIA • F8","quick_presets":"Ajustes rápidos","global_hotkeys":"Atajos globales","status_ready":"LISTO","status_active":"ACTIVO","status_stopped":"DETENIDO","status_finished":"FINALIZADO","status_error":"ERROR"},
    "it": {"display_design":"Schermo e design","language":"Lingua","system_default":"Lingua di sistema","apply_restart":"Applica lingua e riavvia","look":"Aspetto","accent":"Accento","background":"Sfondo","custom_background":"Scegli immagine / GIF","motion_quality":"Movimento e qualità","animations":"Abilita animazioni","ui_size":"Dimensione UI","smooth_scrolling":"Scorrimento fluido","start_screen":"Schermata iniziale","fullscreen":"Schermo intero","compact":"Compatto","off":"Disattivato","timing":"Temporizzazione","interval":"Intervallo","hours":"Ore","minutes":"Minuti","seconds":"Secondi","milliseconds":"Millisecondi","click_style":"Stile clic","mouse_button":"Pulsante mouse","left":"Sinistro","right":"Destro","middle":"Centrale","click_type":"Tipo di clic","session":"Sessione","infinite":"Infinito fino a F6 / F8","actions":"Azioni","start_delay":"Ritardo avvio","time_limit":"Limite di tempo","fixed_position":"Posizione fissa cursore","capture_position":"Cattura posizione • F7","live_control":"Controllo live","start":"AVVIA • F6","stop_emergency":"ARRESTO DI EMERGENZA • F8","quick_presets":"Preset rapidi","global_hotkeys":"Scorciatoie globali","status_ready":"PRONTO","status_active":"ATTIVO","status_stopped":"FERMATO","status_finished":"FINITO","status_error":"ERRORE"},
    "pt": {"display_design":"Ecrã e design","language":"Idioma","system_default":"Idioma do sistema","apply_restart":"Aplicar idioma e reiniciar","look":"Aparência","accent":"Destaque","background":"Fundo","custom_background":"Escolher imagem / GIF","motion_quality":"Movimento e qualidade","animations":"Ativar animações","ui_size":"Tamanho da interface","smooth_scrolling":"Rolagem suave","start_screen":"Ecrã inicial","fullscreen":"Ecrã inteiro","compact":"Compacto","off":"Desligado","timing":"Temporização","interval":"Intervalo","hours":"Horas","minutes":"Minutos","seconds":"Segundos","milliseconds":"Milisseg.","click_style":"Estilo de clique","mouse_button":"Botão do rato","left":"Esquerdo","right":"Direito","middle":"Meio","click_type":"Tipo de clique","session":"Sessão","infinite":"Infinito até F6 / F8","actions":"Ações","start_delay":"Atraso de início","time_limit":"Limite de tempo","fixed_position":"Posição fixa do cursor","capture_position":"Capturar posição • F7","live_control":"Controlo ao vivo","start":"INICIAR • F6","stop_emergency":"PARAGEM DE EMERGÊNCIA • F8","quick_presets":"Predefinições rápidas","global_hotkeys":"Atalhos globais","status_ready":"PRONTO","status_active":"ATIVO","status_stopped":"PARADO","status_finished":"CONCLUÍDO","status_error":"ERRO"},
    "nl": {"display_design":"Weergave & ontwerp","language":"Taal","system_default":"Systeemtaal","apply_restart":"Taal toepassen en herstarten","look":"Uiterlijk","accent":"Accent","background":"Achtergrond","custom_background":"Eigen afbeelding / GIF kiezen","motion_quality":"Animatie & kwaliteit","animations":"Animaties inschakelen","ui_size":"UI-grootte","smooth_scrolling":"Vloeiend scrollen","start_screen":"Startscherm","fullscreen":"Volledig scherm","compact":"Compact","off":"Uit","timing":"Timing","interval":"Interval","hours":"Uren","minutes":"Minuten","seconds":"Seconden","milliseconds":"Milliseconden","click_style":"Klikstijl","mouse_button":"Muisknop","left":"Links","right":"Rechts","middle":"Midden","click_type":"Kliktype","session":"Sessie","infinite":"Oneindig tot F6 / F8","actions":"Acties","start_delay":"Startvertraging","time_limit":"Tijdslimiet","fixed_position":"Vaste cursorpositie","capture_position":"Positie opslaan • F7","live_control":"Live bediening","start":"START • F6","stop_emergency":"NOODSTOP • F8","quick_presets":"Snelle presets","global_hotkeys":"Globale sneltoetsen","status_ready":"GEREED","status_active":"ACTIEF","status_stopped":"GESTOPT","status_finished":"KLAAR","status_error":"FOUT"},
    "pl": {"display_design":"Wygląd i ekran","language":"Język","system_default":"Język systemu","apply_restart":"Zastosuj język i uruchom ponownie","look":"Wygląd","accent":"Akcent","background":"Tło","custom_background":"Wybierz obraz / GIF","motion_quality":"Animacje i jakość","animations":"Włącz animacje","ui_size":"Rozmiar interfejsu","smooth_scrolling":"Płynne przewijanie","start_screen":"Ekran startowy","fullscreen":"Pełny ekran","compact":"Kompaktowy","off":"Wyłączony","timing":"Czas","interval":"Interwał","hours":"Godziny","minutes":"Minuty","seconds":"Sekundy","milliseconds":"Milisek.","click_style":"Styl kliknięcia","mouse_button":"Przycisk myszy","left":"Lewy","right":"Prawy","middle":"Środkowy","click_type":"Typ kliknięcia","session":"Sesja","infinite":"Bez końca do F6 / F8","actions":"Akcje","start_delay":"Opóźnienie startu","time_limit":"Limit czasu","fixed_position":"Stała pozycja kursora","capture_position":"Pobierz pozycję • F7","live_control":"Sterowanie na żywo","start":"START • F6","stop_emergency":"STOP AWARYJNY • F8","quick_presets":"Szybkie ustawienia","global_hotkeys":"Globalne skróty","status_ready":"GOTOWY","status_active":"AKTYWNY","status_stopped":"ZATRZYMANY","status_finished":"GOTOWE","status_error":"BŁĄD"},
    "cs": {"display_design":"Vzhled a zobrazení","language":"Jazyk","system_default":"Jazyk systému","apply_restart":"Použít jazyk a restartovat","look":"Vzhled","background":"Pozadí","animations":"Povolit animace","ui_size":"Velikost UI","smooth_scrolling":"Plynulé posouvání","start_screen":"Úvodní obrazovka","fullscreen":"Celá obrazovka","compact":"Kompaktní","off":"Vypnuto","timing":"Časování","interval":"Interval","hours":"Hodiny","minutes":"Minuty","seconds":"Sekundy","milliseconds":"Milisek.","mouse_button":"Tlačítko myši","left":"Levé","right":"Pravé","middle":"Prostřední","session":"Relace","actions":"Akce","start":"START • F6","stop_emergency":"NOUZOVÉ ZASTAVENÍ • F8","global_hotkeys":"Globální klávesy","status_ready":"PŘIPRAVENO","status_active":"AKTIVNÍ","status_stopped":"ZASTAVENO","status_error":"CHYBA"},
    "sk": {"display_design":"Vzhľad a zobrazenie","language":"Jazyk","system_default":"Jazyk systému","apply_restart":"Použiť jazyk a reštartovať","look":"Vzhľad","background":"Pozadie","animations":"Zapnúť animácie","ui_size":"Veľkosť UI","smooth_scrolling":"Plynulé posúvanie","start_screen":"Úvodná obrazovka","fullscreen":"Celá obrazovka","compact":"Kompaktné","off":"Vypnuté","timing":"Časovanie","interval":"Interval","hours":"Hodiny","minutes":"Minúty","seconds":"Sekundy","mouse_button":"Tlačidlo myši","left":"Ľavé","right":"Pravé","middle":"Stredné","session":"Relácia","actions":"Akcie","start":"ŠTART • F6","stop_emergency":"NÚDZOVÉ ZASTAVENIE • F8","status_ready":"PRIPRAVENÉ","status_active":"AKTÍVNE","status_stopped":"ZASTAVENÉ","status_error":"CHYBA"},
    "hu": {"display_design":"Kijelző és dizájn","language":"Nyelv","system_default":"Rendszernyelv","apply_restart":"Nyelv alkalmazása és újraindítás","look":"Megjelenés","background":"Háttér","animations":"Animációk engedélyezése","ui_size":"Felület mérete","smooth_scrolling":"Folyamatos görgetés","start_screen":"Kezdőképernyő","fullscreen":"Teljes képernyő","compact":"Kompakt","off":"Ki","timing":"Időzítés","interval":"Intervallum","hours":"Óra","minutes":"Perc","seconds":"Másodperc","mouse_button":"Egérgomb","left":"Bal","right":"Jobb","middle":"Középső","session":"Munkamenet","actions":"Műveletek","start":"INDÍTÁS • F6","stop_emergency":"VÉSZLEÁLLÍTÁS • F8","status_ready":"KÉSZ","status_active":"AKTÍV","status_stopped":"LEÁLLÍTVA","status_error":"HIBA"},
    "ro": {"display_design":"Afișare și design","language":"Limbă","system_default":"Limba sistemului","apply_restart":"Aplică limba și repornește","look":"Aspect","background":"Fundal","animations":"Activează animațiile","ui_size":"Dimensiune UI","smooth_scrolling":"Derulare fluidă","start_screen":"Ecran de pornire","fullscreen":"Ecran complet","compact":"Compact","off":"Oprit","timing":"Temporizare","interval":"Interval","hours":"Ore","minutes":"Minute","seconds":"Secunde","mouse_button":"Buton mouse","left":"Stânga","right":"Dreapta","middle":"Mijloc","session":"Sesiune","actions":"Acțiuni","start":"START • F6","stop_emergency":"OPRIRE DE URGENȚĂ • F8","status_ready":"GATA","status_active":"ACTIV","status_stopped":"OPRIT","status_error":"EROARE"},
    "sv": {"display_design":"Skärm och design","language":"Språk","system_default":"Systemspråk","apply_restart":"Använd språk och starta om","look":"Utseende","background":"Bakgrund","animations":"Aktivera animationer","ui_size":"UI-storlek","smooth_scrolling":"Mjuk rullning","start_screen":"Startskärm","fullscreen":"Helskärm","compact":"Kompakt","off":"Av","timing":"Timing","interval":"Intervall","hours":"Timmar","minutes":"Minuter","seconds":"Sekunder","mouse_button":"Musknapp","left":"Vänster","right":"Höger","middle":"Mitten","session":"Session","actions":"Åtgärder","start":"START • F6","stop_emergency":"NÖDSTOPP • F8","status_ready":"KLAR","status_active":"AKTIV","status_stopped":"STOPPAD","status_error":"FEL"},
    "no": {"display_design":"Skjerm og design","language":"Språk","system_default":"Systemspråk","apply_restart":"Bruk språk og start på nytt","look":"Utseende","background":"Bakgrunn","animations":"Aktiver animasjoner","ui_size":"UI-størrelse","smooth_scrolling":"Jevn rulling","start_screen":"Startskjerm","fullscreen":"Fullskjerm","compact":"Kompakt","off":"Av","timing":"Timing","interval":"Intervall","hours":"Timer","minutes":"Minutter","seconds":"Sekunder","mouse_button":"Museknapp","left":"Venstre","right":"Høyre","middle":"Midten","session":"Økt","actions":"Handlinger","start":"START • F6","stop_emergency":"NØDSTOPP • F8","status_ready":"KLAR","status_active":"AKTIV","status_stopped":"STOPPET","status_error":"FEIL"},
    "da": {"display_design":"Skærm og design","language":"Sprog","system_default":"Systemsprog","apply_restart":"Anvend sprog og genstart","look":"Udseende","background":"Baggrund","animations":"Aktiver animationer","ui_size":"UI-størrelse","smooth_scrolling":"Jævn rulning","start_screen":"Startskærm","fullscreen":"Fuld skærm","compact":"Kompakt","off":"Fra","timing":"Timing","interval":"Interval","hours":"Timer","minutes":"Minutter","seconds":"Sekunder","mouse_button":"Museknap","left":"Venstre","right":"Højre","middle":"Midt","session":"Session","actions":"Handlinger","start":"START • F6","stop_emergency":"NØDSTOP • F8","status_ready":"KLAR","status_active":"AKTIV","status_stopped":"STOPPET","status_error":"FEJL"},
    "fi": {"display_design":"Näyttö ja ulkoasu","language":"Kieli","system_default":"Järjestelmän kieli","apply_restart":"Käytä kieltä ja käynnistä uudelleen","look":"Ulkoasu","background":"Tausta","animations":"Ota animaatiot käyttöön","ui_size":"Käyttöliittymän koko","smooth_scrolling":"Sulava vieritys","start_screen":"Aloitusnäyttö","fullscreen":"Koko näyttö","compact":"Kompakti","off":"Pois","timing":"Ajoitus","interval":"Väli","hours":"Tunnit","minutes":"Minuutit","seconds":"Sekunnit","mouse_button":"Hiiren painike","left":"Vasen","right":"Oikea","middle":"Keskimmäinen","session":"Istunto","actions":"Toiminnot","start":"KÄYNNISTÄ • F6","stop_emergency":"HÄTÄPYSÄYTYS • F8","status_ready":"VALMIS","status_active":"AKTIIVINEN","status_stopped":"PYSÄYTETTY","status_error":"VIRHE"},
    "tr": {"display_design":"Ekran ve tasarım","language":"Dil","system_default":"Sistem dili","apply_restart":"Dili uygula ve yeniden başlat","look":"Görünüm","background":"Arka plan","animations":"Animasyonları etkinleştir","ui_size":"Arayüz boyutu","smooth_scrolling":"Akıcı kaydırma","start_screen":"Başlangıç ekranı","fullscreen":"Tam ekran","compact":"Kompakt","off":"Kapalı","timing":"Zamanlama","interval":"Aralık","hours":"Saat","minutes":"Dakika","seconds":"Saniye","mouse_button":"Fare düğmesi","left":"Sol","right":"Sağ","middle":"Orta","session":"Oturum","actions":"İşlemler","start":"BAŞLAT • F6","stop_emergency":"ACİL DURDUR • F8","status_ready":"HAZIR","status_active":"AKTİF","status_stopped":"DURDU","status_error":"HATA"},
    "ru": {"display_design":"Экран и дизайн","language":"Язык","system_default":"Язык системы","apply_restart":"Применить язык и перезапустить","look":"Внешний вид","background":"Фон","custom_background":"Выбрать изображение / GIF","animations":"Включить анимации","ui_size":"Размер интерфейса","smooth_scrolling":"Плавная прокрутка","start_screen":"Стартовый экран","fullscreen":"Полный экран","compact":"Компактный","off":"Выкл.","timing":"Тайминг","interval":"Интервал","hours":"Часы","minutes":"Минуты","seconds":"Секунды","mouse_button":"Кнопка мыши","left":"Левая","right":"Правая","middle":"Средняя","session":"Сессия","actions":"Действия","start":"СТАРТ • F6","stop_emergency":"АВАРИЙНАЯ ОСТАНОВКА • F8","status_ready":"ГОТОВО","status_active":"АКТИВНО","status_stopped":"ОСТАНОВЛЕНО","status_error":"ОШИБКА"},
    "uk": {"display_design":"Екран і дизайн","language":"Мова","system_default":"Мова системи","apply_restart":"Застосувати мову й перезапустити","look":"Вигляд","background":"Фон","animations":"Увімкнути анімації","ui_size":"Розмір інтерфейсу","smooth_scrolling":"Плавне прокручування","start_screen":"Стартовий екран","fullscreen":"На весь екран","compact":"Компактний","off":"Вимкнено","timing":"Таймінг","interval":"Інтервал","hours":"Години","minutes":"Хвилини","seconds":"Секунди","mouse_button":"Кнопка миші","left":"Ліва","right":"Права","middle":"Середня","session":"Сесія","actions":"Дії","start":"СТАРТ • F6","stop_emergency":"АВАРІЙНА ЗУПИНКА • F8","status_ready":"ГОТОВО","status_active":"АКТИВНО","status_stopped":"ЗУПИНЕНО","status_error":"ПОМИЛКА"},
    "el": {"display_design":"Οθόνη & σχεδίαση","language":"Γλώσσα","system_default":"Γλώσσα συστήματος","apply_restart":"Εφαρμογή γλώσσας και επανεκκίνηση","look":"Εμφάνιση","background":"Φόντο","animations":"Ενεργοποίηση κινούμενων εφέ","ui_size":"Μέγεθος UI","smooth_scrolling":"Ομαλή κύλιση","start_screen":"Οθόνη έναρξης","fullscreen":"Πλήρης οθόνη","compact":"Συμπαγές","off":"Ανενεργό","timing":"Χρονισμός","interval":"Διάστημα","hours":"Ώρες","minutes":"Λεπτά","seconds":"Δευτερόλεπτα","mouse_button":"Κουμπί ποντικιού","left":"Αριστερό","right":"Δεξί","middle":"Μεσαίο","session":"Συνεδρία","actions":"Ενέργειες","start":"ΕΝΑΡΞΗ • F6","stop_emergency":"ΕΠΕΙΓΟΥΣΑ ΔΙΑΚΟΠΗ • F8","status_ready":"ΕΤΟΙΜΟ","status_active":"ΕΝΕΡΓΟ","status_stopped":"ΣΤΑΜΑΤΗΜΕΝΟ","status_error":"ΣΦΑΛΜΑ"},
    "ja": {"display_design":"表示とデザイン","language":"言語","system_default":"システム言語","apply_restart":"言語を適用して再起動","look":"外観","accent":"アクセント","background":"背景","custom_background":"画像 / GIF を選択","motion_quality":"モーションと品質","animations":"アニメーションを有効化","ui_size":"UI サイズ","smooth_scrolling":"スムーズスクロール","start_screen":"スタート画面","fullscreen":"全画面","compact":"コンパクト","off":"オフ","timing":"タイミング","interval":"間隔","hours":"時間","minutes":"分","seconds":"秒","milliseconds":"ミリ秒","click_style":"クリックスタイル","mouse_button":"マウスボタン","left":"左","right":"右","middle":"中央","click_type":"クリック種類","session":"セッション","infinite":"F6 / F8 まで無制限","actions":"アクション","start_delay":"開始遅延","time_limit":"時間制限","fixed_position":"固定カーソル位置","capture_position":"位置を取得 • F7","live_control":"ライブ操作","start":"開始 • F6","stop_emergency":"緊急停止 • F8","quick_presets":"クイックプリセット","global_hotkeys":"グローバルホットキー","status_ready":"準備完了","status_active":"動作中","status_stopped":"停止","status_finished":"完了","status_error":"エラー"},
    "ko": {"display_design":"디스플레이 및 디자인","language":"언어","system_default":"시스템 언어","apply_restart":"언어 적용 후 재시작","look":"모양","background":"배경","custom_background":"이미지 / GIF 선택","animations":"애니메이션 사용","ui_size":"UI 크기","smooth_scrolling":"부드러운 스크롤","start_screen":"시작 화면","fullscreen":"전체 화면","compact":"컴팩트","off":"끔","timing":"타이밍","interval":"간격","hours":"시간","minutes":"분","seconds":"초","mouse_button":"마우스 버튼","left":"왼쪽","right":"오른쪽","middle":"가운데","session":"세션","actions":"동작","start":"시작 • F6","stop_emergency":"긴급 정지 • F8","global_hotkeys":"전역 단축키","status_ready":"준비","status_active":"활성","status_stopped":"정지","status_error":"오류"},
    "zh": {"display_design":"显示与设计","language":"语言","system_default":"系统语言","apply_restart":"应用语言并重启","look":"外观","accent":"强调色","background":"背景","custom_background":"选择图片 / GIF","animations":"启用动画","ui_size":"界面大小","smooth_scrolling":"流畅滚动","start_screen":"启动画面","fullscreen":"全屏","compact":"紧凑","off":"关闭","timing":"计时","interval":"间隔","hours":"小时","minutes":"分钟","seconds":"秒","milliseconds":"毫秒","click_style":"点击样式","mouse_button":"鼠标按键","left":"左键","right":"右键","middle":"中键","click_type":"点击类型","session":"会话","infinite":"直到 F6 / F8 一直运行","actions":"操作次数","start_delay":"启动延迟","time_limit":"时间限制","fixed_position":"固定光标位置","capture_position":"获取位置 • F7","live_control":"实时控制","start":"开始 • F6","stop_emergency":"紧急停止 • F8","quick_presets":"快速预设","global_hotkeys":"全局快捷键","status_ready":"就绪","status_active":"运行中","status_stopped":"已停止","status_finished":"已完成","status_error":"错误"},
    "ar": {"display_design":"العرض والتصميم","language":"اللغة","system_default":"لغة النظام","apply_restart":"تطبيق اللغة وإعادة التشغيل","look":"المظهر","accent":"لون التمييز","background":"الخلفية","custom_background":"اختيار صورة / GIF","animations":"تفعيل الرسوم المتحركة","ui_size":"حجم الواجهة","smooth_scrolling":"تمرير سلس","start_screen":"شاشة البدء","fullscreen":"ملء الشاشة","compact":"مضغوط","off":"إيقاف","timing":"التوقيت","interval":"الفاصل","hours":"ساعات","minutes":"دقائق","seconds":"ثوانٍ","milliseconds":"مللي ثانية","click_style":"نمط النقر","mouse_button":"زر الفأرة","left":"يسار","right":"يمين","middle":"وسط","click_type":"نوع النقر","session":"الجلسة","infinite":"مستمر حتى F6 / F8","actions":"الإجراءات","start_delay":"تأخير البدء","time_limit":"حد الوقت","fixed_position":"موضع مؤشر ثابت","capture_position":"التقاط الموضع • F7","live_control":"التحكم المباشر","start":"بدء • F6","stop_emergency":"إيقاف طارئ • F8","quick_presets":"إعدادات سريعة","global_hotkeys":"اختصارات عامة","status_ready":"جاهز","status_active":"نشط","status_stopped":"متوقف","status_finished":"اكتمل","status_error":"خطأ"},
}

TRANSLATIONS = {"en": EN, "de": {**EN, **DE}}
for code, pack in PACKS.items():
    TRANSLATIONS[code] = {**EN, **pack}


def detect_system_language() -> str:
    raw = (
        os.environ.get("LC_ALL")
        or os.environ.get("LC_MESSAGES")
        or os.environ.get("LANGUAGE")
        or os.environ.get("LANG")
        or "en"
    )
    # LANGUAGE can contain a colon-separated preference list.
    raw = raw.split(":", 1)[0]
    code = raw.split(".", 1)[0].replace("-", "_").split("_", 1)[0].lower()
    return code if code in TRANSLATIONS else "en"


def resolve_language(setting: str | None) -> str:
    if not setting or setting == "system":
        return detect_system_language()
    return setting if setting in TRANSLATIONS else "en"


def tr(language_setting: str | None, key: str, **kwargs) -> str:
    code = resolve_language(language_setting)
    text = TRANSLATIONS.get(code, EN).get(key, EN.get(key, key))
    try:
        return text.format(**kwargs)
    except Exception:
        return text


def language_options() -> list[tuple[str, str]]:
    return list(LANGUAGES)
