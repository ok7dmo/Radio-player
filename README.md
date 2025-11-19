# FT-897 Memory Manager

Kompletní sada nástrojů pro správu pamětí radiostanice **Yaesu FT-897** - dostupná v příkazové řádce i s grafickým rozhraním.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-Optional-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🎯 Dva způsoby použití

### 1️⃣ GUI Aplikace (Doporučeno)

**Dvě verze grafického rozhraní:**

#### 🪟 **Tkinter GUI** (DOPORUČENO pro Windows)

```bash
# ŽÁDNÁ instalace není potřeba!
python3 ft897_gui_tkinter.py

# Nebo na Windows:
run_gui.bat
```

✅ **Výhody Tkinter:**
- **Žádné závislosti** - součást Pythonu!
- Funguje hned po instalaci Pythonu
- Ideální pro Windows
- Malé, rychlé, spolehlivé

👉 **Windows uživatelé:** [README_WINDOWS.md](README_WINDOWS.md)

#### 🐧 **PyQt6 GUI** (volitelné, modernější)

```bash
# Instalace závislostí
pip install PyQt6

# Spuštění GUI
python3 ft897_gui.py
```

✨ **Funkce GUI (obě verze):**
- 📂 Načítání/ukládání image souborů
- 📊 Tabulkový přehled všech kanálů
- ✏️ Vizuální editor kanálů
- 🔄 Batch operace (konverze na PKT)
- 📈 Statistiky a grafy
- 🎨 Barevné zvýraznění (2m repeatery, PKT mód)

👉 **Více informací:** [README_GUI.md](README_GUI.md)

---

### 2️⃣ CLI Aplikace (Bez závislostí)

**Příkazová řádka** - jednoduché, rychlé, bez instalace:

```bash
# Analýza image
python3 ft897_analyze.py ft897_backup.dat

# Konverze 2m repeaterů na PKT
python3 ft897_packet_converter.py input.dat output.dat
```

✨ **Funkce CLI:**
- 🔍 Analýza image s statistikami
- 🔄 Automatická konverze 2m→PKT
- ⚡ Žádné závislosti (pouze Python 3)
- 📜 Skriptovatelné

👉 **Více informací:** [README_FT897_CONVERTER.md](README_FT897_CONVERTER.md)

---

## 🚀 Rychlý start

### Option A: GUI (s PyQt6)

```bash
# 1. Nainstalovat PyQt6
pip install PyQt6

# 2. Spustit GUI aplikaci
python3 ft897_gui.py

# Nebo použít pomocný skript
./run_gui.sh
```

### Option B: CLI (bez instalace)

```bash
# Konvertovat 2m repeatery na PKT mód
python3 ft897_packet_converter.py my_backup.dat my_modified.dat
```

---

## 📦 Co je v balíčku

### 🖥️ GUI Aplikace

| Soubor | Popis |
|--------|-------|
| **ft897_gui.py** | Hlavní GUI aplikace (PyQt6) |
| **ft897_memory.py** | Backend knihovna pro práci s image |
| **run_gui.sh** | Pomocný spouštěcí skript |

### 💻 CLI Nástroje

| Soubor | Popis |
|--------|-------|
| **ft897_packet_converter.py** | Konvertor 2m→PKT |
| **ft897_analyze.py** | Analyzer s statistikami |
| **test_ft897_converter.py** | Automatické testy |
| **example_workflow.sh** | Ukázkový workflow |

### 📚 Dokumentace

| Soubor | Popis |
|--------|-------|
| **README.md** | Tento soubor |
| **README_GUI.md** | Kompletní GUI dokumentace |
| **README_FT897_CONVERTER.md** | CLI dokumentace |
| **QUICK_START_CZ.md** | Rychlý start (CLI) |
| **CLAUDE.md** | Projektová dokumentace |

---

## 🎯 Hlavní funkce

### ✨ Co umí GUI aplikace

**Správa kanálů:**
- ✅ Načtení/uložení FT-897 image (.dat, .img)
- ✅ Zobrazení všech kanálů v tabulce
- ✅ Úprava jednotlivých kanálů
  - Frekvence (MHz + fine tune v kHz)
  - Mód (LSB, USB, CW, AM, FM, DIG, PKT)
  - Duplex (Simplex, +, -, Split)
  - Offset v kHz
  - Název (8 znaků)
  - Příznaky: Skip, IPO, ATT

**Batch operace:**
- ✅ Konverze všech 2m repeaterů na PKT mód
- ✅ Hromadné úpravy
- ✅ Export statistik

**Analýza:**
- ✅ Statistiky (počty kanálů, pásma, módy)
- ✅ Grafické přehledy
- ✅ Filtrování a řazení

**Bezpečnost:**
- ✅ Automatické zálohy
- ✅ Potvrzení před zápisy
- ✅ Status bar s přehledem změn

---

## 📋 Požadavky

### Minimální systémové požadavky

- **Python 3.7 nebo novější**
- **OS:** Linux, macOS, Windows

### Závislosti

**Pro CLI aplikace:**
- ✅ Žádné závislosti (pouze Python stdlib)

**Pro GUI aplikaci:**
- 📦 PyQt6 (instalace: `pip install PyQt6`)

```bash
# Instalace všech závislostí
pip install -r requirements.txt
```

---

## 🎓 Použití

### GUI Aplikace - Základní workflow

1. **Spustit aplikaci:**
   ```bash
   python3 ft897_gui.py
   ```

2. **Načíst image:**
   - File → Load Image... (Ctrl+O)
   - Vybrat .dat soubor

3. **Prohlédnout kanály:**
   - Tabulka zobrazí všechny kanály
   - Žlutá = 2m repeater
   - Zelená = PKT mód

4. **Upravit kanál:**
   - Dvojklik na řádek
   - Změnit parametry
   - OK pro uložení

5. **Batch konverze:**
   - Tools → Convert 2m to PKT
   - Potvrdit

6. **Uložit změny:**
   - File → Save (Ctrl+S)

### CLI Aplikace - Základní workflow

```bash
# 1. Analyzovat image (volitelné)
python3 ft897_analyze.py ft897_backup.dat

# 2. Konvertovat 2m repeatery na PKT
python3 ft897_packet_converter.py ft897_backup.dat ft897_modified.dat

# 3. Nahrát zpět do rádia pomocí programovacího SW
```

---

## 📸 Ukázka GUI

### Hlavní okno
```
┌──────────────────────────────────────────────────────────────┐
│ FT-897 Memory Manager                                   [_][□][×]│
├──────────────────────────────────────────────────────────────┤
│ File  Tools  Help                                            │
├──────────────────────────────────────────────────────────────┤
│ [📂 Load Image] [💾 Save] [💾 Save As...]  [📊 Statistics] │
├──────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────────────────┐   │
│ │ Batch Operations                                       │   │
│ │ [🔄 Convert 2m Repeaters to PKT]                      │   │
│ └────────────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────────────────┐   │
│ │Ch# │Frequency│Mode│Duplex│Offset│Name │Band │S│I│A│  │   │
│ ├────┼─────────┼────┼──────┼──────┼─────┼─────┼─┼─┼─┤  │   │
│ │  5 │145.6250 │FM  │  +   │ 600.0│R5   │ 2m  │ │ │ │  │   │
│ │ 12 │145.7750 │PKT │  -   │ 600.0│R12  │ 2m  │ │ │ │  │   │
│ │ 23 │438.6250 │FM  │  +   │7600.0│UHF  │70cm │ │ │ │  │   │
│ │... │         │    │      │      │     │     │ │ │ │  │   │
│ └────────────────────────────────────────────────────────┘   │
│                                                              │
│ [✏️ Edit Selected Channel]                                  │
├──────────────────────────────────────────────────────────────┤
│ File: ft897_backup.dat | Channels: 45/200 | 2m Repeaters: 3 │
└──────────────────────────────────────────────────────────────┘
```

### Editor kanálu
```
┌───────────────────────────────┐
│ Edit Channel 5          [_][×]│
├───────────────────────────────┤
│ Frequency (MHz):  [145] MHz   │
│ Fine tune (kHz):  [625] kHz   │
│                               │
│ Mode:        [FM ▼]          │
│ Duplex:      [+  ▼]          │
│ Offset (kHz): [600] kHz      │
│                               │
│ Name: [R5______]              │
│                               │
│ ☐ Skip in scan                │
│ ☐ IPO                         │
│ ☐ Attenuator                  │
│                               │
│         [OK]  [Cancel]        │
└───────────────────────────────┘
```

---

## 🔍 Technické detaily

### Formát FT-897 Memory Channel (26 bytů)

```
Byte 0:  tag_on_off:1, tag_default:1, unknown1:3, mode:3
Byte 1:  duplex:2, is_duplex:1, is_cwdig_narrow:1, is_fm_narrow:1, freq_range:3
Byte 2:  skip:1, unknown1_1:1, ipo:1, att:1, unknown2:4
...
Bytes 14-17: Frequency (32-bit LE, v 10Hz jednotkách)
Bytes 18-21: Offset (32-bit LE, v 10Hz jednotkách)
```

### Módy (3-bit hodnoty 0-7)

```
0 = LSB    4 = AM
1 = USB    5 = FM
2 = CW     6 = DIG
3 = CW-R   7 = PKT ← cíl konverze
```

**⚠️ Poznámka:** Memory mode values jsou **jiné** než CAT command values!

---

## ⚠️ Důležitá upozornění

### Bezpečnost

1. ⚠️ **VŽDY SI ZÁLOHUJTE ORIGINÁLNÍ IMAGE!**
2. ⚠️ **Testujte v bezpečném prostředí před nahráním do rádia**
3. ⚠️ **Program vytvořen na základě reverse-engineeringu** (použití na vlastní riziko)

### Doporučený workflow

```
1. Záloha z rádia → ft897_original.dat
2. Kopie zálohy → ft897_backup.dat (pojistka!)
3. Úprava v aplikaci → ft897_modified.dat
4. Test v programovacím SW (náhled)
5. Nahrání do rádia (opatrně!)
6. Kontrola na rádiu
```

---

## 🐛 Řešení problémů

### PyQt6 se nepodaří nainstalovat

```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt6

# macOS (s Homebrew)
brew install pyqt6

# Windows nebo pip
pip install --upgrade pip
pip install PyQt6
```

### GUI se nespustí

```bash
# Zkontrolovat Python verzi
python3 --version  # min 3.7

# Zkontrolovat PyQt6
python3 -c "from PyQt6.QtWidgets import QApplication; print('OK')"

# Pokud chyba, použít CLI verzi
python3 ft897_packet_converter.py input.dat output.dat
```

### Program nenajde žádné kanály

- Zkontrolujte, že image není poškozený
- Použijte `ft897_analyze.py` pro diagnostiku
- Zkuste jinou image

---

## 📚 Dokumentace a zdroje

### Dokumentace v tomto projektu

- **[README_GUI.md](README_GUI.md)** - Kompletní GUI dokumentace
- **[README_FT897_CONVERTER.md](README_FT897_CONVERTER.md)** - CLI dokumentace
- **[QUICK_START_CZ.md](QUICK_START_CZ.md)** - Rychlý start v češtině
- **[CLAUDE.md](CLAUDE.md)** - Projektová dokumentace pro AI

### Externí zdroje

- [Yaesu FT-897 Operating Manual](https://www.hamradio.co.uk/pub/media/wysiwyg/FT-897_OpMan.pdf)
- [CHIRP Open-Source Programming](https://chirpmyradio.com/)
- [FT-897 CAT Commands](https://www.qsl.net/sp9hzx/pdf/FT-897D_Yaesu-official_CAT-Commands.pdf)

---

## 🤝 Přispívání

Máte nápad na vylepšení? Našli jste chybu?

1. Fork repository
2. Vytvořte feature branch (`git checkout -b feature/AmazingFeature`)
3. Commitněte změny (`git commit -m 'Add AmazingFeature'`)
4. Pushněte branch (`git push origin feature/AmazingFeature`)
5. Vytvořte Pull Request

---

## 📄 Licence

MIT License - používejte a upravujte dle potřeby.

```
Copyright (c) 2025 Claude AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## ✉️ Kontakt a podpora

**Vytvořeno pomocí Claude AI** na základě:
- CHIRP open-source projektu (ft857.py driver)
- FT-897 CAT command dokumentace
- Reverse-engineering community výzkumu

**Issues a Bug Reports:**
- GitHub Issues (pokud je repo veřejné)
- Email: [váš email]

---

## 🎓 Pro vývojáře

### API Příklad

```python
from ft897_memory import FT897Image, MODE_PKT

# Načíst image
image = FT897Image()
image.load_from_file("backup.dat")

# Pracovat s kanály
for channel in image.get_used_channels():
    print(f"Ch{channel.index}: {channel.frequency/1e6:.4f} MHz")

# Konvertovat 2m→PKT
count = image.convert_2m_to_pkt()
print(f"Converted {count} channels")

# Uložit
image.save_to_file("modified.dat")

# Statistiky
stats = image.get_statistics()
print(stats)
```

### Spuštění testů

```bash
# CLI testy
python3 test_ft897_converter.py

# Kompletní workflow
./example_workflow.sh test_image.dat
```

---

## 🌟 Roadmap

### Plánované funkce

- [ ] Import/Export CSV
- [ ] Tone/CTCSS editor v GUI
- [ ] Split frequency podpora
- [ ] Drag & drop pro změnu pořadí kanálů
- [ ] Preset templates
- [ ] Online repeater databáze
- [ ] CAT interface pro přímou komunikaci s rádiem

---

**⚡ Vytvořeno s 💙 pro radioamatérskou komunitu 📻**

**73 de Claude AI 📡**
