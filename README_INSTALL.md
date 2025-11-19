# FT-897 Memory Manager - Instalační průvodce

Návod pro instalaci na **Linux, Raspberry Pi a podobné systémy**.

---

## 🚀 Rychlá instalace (doporučeno)

### Krok 1: Stáhněte projekt

```bash
git clone https://github.com/ok7dmo/Radio-player.git
cd Radio-player
```

### Krok 2: Spusťte instalační skript

```bash
chmod +x install.sh
./install.sh
```

**To je vše!** Instalační skript:
- ✅ Zkontroluje Python
- ✅ Nainstaluje PyQt6
- ✅ Vytvoří .desktop launcher
- ✅ Nastaví oprávnění

### Krok 3: Spusťte aplikaci

**Způsob 1 - Z menu aplikací:**
```
Applications → HamRadio → FT-897 Memory Manager
```

**Způsob 2 - Z terminálu:**
```bash
./run_gui.sh
```

**Způsob 3 - Přímé spuštění:**
```bash
python3 ft897_gui.py
```

---

## 📋 Manuální instalace

Pokud nechcete použít automatickou instalaci:

### 1. Nainstalujte Python (pokud není)

```bash
# Ubuntu/Debian/Raspberry Pi
sudo apt-get update
sudo apt-get install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

### 2. Nainstalujte PyQt6

**Raspberry Pi (doporučeno - systémový balíček):**
```bash
sudo apt-get install python3-pyqt6
```

**Jiné systémy (pip):**
```bash
pip3 install PyQt6
```

**Nebo použijte requirements.txt:**
```bash
pip3 install -r requirements.txt
```

### 3. Nastavte oprávnění

```bash
chmod +x ft897_gui.py
chmod +x run_gui.sh
```

### 4. Vytvořte .desktop launcher (volitelné)

```bash
mkdir -p ~/.local/share/applications
cp ft897-manager.desktop ~/.local/share/applications/

# Upravte cesty v .desktop souboru
nano ~/.local/share/applications/ft897-manager.desktop
```

---

## 🍓 Raspberry Pi - Speciální instrukce

### Doporučená metoda

```bash
# 1. Aktualizujte systém
sudo apt-get update
sudo apt-get upgrade

# 2. Nainstalujte PyQt6 (systémový balíček)
sudo apt-get install python3-pyqt6

# 3. Klonujte projekt
git clone https://github.com/ok7dmo/Radio-player.git
cd Radio-player

# 4. Spusťte installer
chmod +x install.sh
./install.sh

# 5. Spusťte aplikaci
./run_gui.sh
```

### Vytvoření zástupce na ploše

```bash
# Zkopírujte .desktop soubor na plochu
cp ~/.local/share/applications/ft897-manager.desktop ~/Desktop/

# Nastavte jako spustitelný
chmod +x ~/Desktop/ft897-manager.desktop
```

Nyní máte ikonu na ploše!

---

## 🖥️ Desktop launcher (.desktop soubor)

Instalační skript automaticky vytvoří launcher v:
```
~/.local/share/applications/ft897-manager.desktop
```

### Manuální vytvoření

Pokud chcete vytvořit launcher ručně:

```bash
nano ~/.local/share/applications/ft897-manager.desktop
```

Obsah:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=FT-897 Memory Manager
GenericName=Radio Memory Manager
Comment=Manage Yaesu FT-897 radio memory images
Exec=python3 /full/path/to/Radio-player/ft897_gui.py
Icon=/full/path/to/Radio-player/icon.png
Path=/full/path/to/Radio-player
Terminal=false
Categories=HamRadio;Utility;
Keywords=radio;ham;amateur;yaesu;ft897;memory;
StartupNotify=true
```

**Důležité:** Nahraďte `/full/path/to/Radio-player` skutečnou cestou!

---

## 🎨 Ikona aplikace

### Vytvoření jednoduché ikony

```bash
cd Radio-player

# Stáhněte nebo vytvořte ikonu (64x64 nebo 128x128 PNG)
# Například:
convert -size 128x128 xc:blue -fill white -pointsize 48 \
    -gravity center -annotate +0+0 'FT-897' icon.png
```

Nebo použijte jakýkoliv PNG obrázek rádia/transceiveru.

---

## 🔧 Řešení problémů

### PyQt6 se nepodaří nainstalovat (Raspberry Pi)

**Problém:** `pip3 install PyQt6` trvá věčnost nebo selže

**Řešení:** Použijte systémový balíček:
```bash
sudo apt-get install python3-pyqt6
```

### GUI se nespustí

**Zkontrolujte závislosti:**
```bash
python3 -c "import PyQt6; print('PyQt6 OK')"
```

**Zkontrolujte Python verzi:**
```bash
python3 --version  # Musí být 3.7+
```

**Spusťte s debug výstupem:**
```bash
python3 ft897_gui.py 2>&1 | tee debug.log
```

### Launcher se nezobrazuje v menu

**Aktualizujte desktop databázi:**
```bash
update-desktop-database ~/.local/share/applications/
```

### Není oprávnění ke spuštění

```bash
chmod +x ft897_gui.py
chmod +x run_gui.sh
chmod +x install.sh
```

---

## 🗑️ Odinstalace

### Pomocí skriptu

```bash
chmod +x uninstall.sh
./uninstall.sh
```

### Manuálně

```bash
# Odebrat desktop launcher
rm ~/.local/share/applications/ft897-manager.desktop

# Odinstalovat PyQt6 (volitelné)
pip3 uninstall PyQt6

# Smazat adresář projektu
cd ..
rm -rf Radio-player
```

---

## 📦 Co se nainstaluje

### Systémové soubory

- `~/.local/share/applications/ft897-manager.desktop` - Desktop launcher

### Python balíčky

- `PyQt6` - GUI framework

### Adresář projektu

Všechny soubory zůstávají v adresáři, kam jste klonovali projekt.

---

## 🔄 Aktualizace

```bash
cd Radio-player
git pull
```

Pokud se změnily závislosti:
```bash
pip3 install -r requirements.txt --upgrade
```

---

## 🎯 Spouštění po startu systému (volitelné)

### Autostart na Raspberry Pi

```bash
# Vytvořte autostart soubor
mkdir -p ~/.config/autostart
cp ~/.local/share/applications/ft897-manager.desktop \
   ~/.config/autostart/
```

Aplikace se spustí při přihlášení.

---

## 💡 Tipy pro Raspberry Pi

### Přidání na hlavní panel

1. Pravý klik na panel
2. "Add/Remove Panel Items"
3. "Add" → "Application Launch Bar"
4. Najděte "FT-897 Memory Manager"

### Klávesová zkratka

1. Otevřete "Keyboard and Mouse" nastavení
2. "Keyboard" tab
3. "Keyboard Shortcuts"
4. Přidejte novou zkratku:
   - Command: `python3 /cesta/k/ft897_gui.py`
   - Shortcut: např. `Ctrl+Alt+F`

---

## 📚 Co dál

Po instalaci:

1. **Přečtěte dokumentaci:**
   - [README.md](README.md) - Přehled projektu
   - [README_GUI.md](README_GUI.md) - GUI návod
   - [README_FT897_CONVERTER.md](README_FT897_CONVERTER.md) - CLI nástroje

2. **Vytvořte zálohu:**
   - Použijte CHIRP nebo jiný SW
   - Zálohujte paměť rádia před úpravami!

3. **Vyzkoušejte aplikaci:**
   - Načtěte testovací image
   - Projděte funkce
   - Otestujte úpravy

---

## ❓ FAQ

**Q: Funguje to na Raspberry Pi Zero?**
A: Ano, ale doporučujeme Pi 3 nebo novější pro lepší výkon.

**Q: Mohu použít CLI nástroje bez GUI?**
A: Ano! CLI nástroje nefungují bez PyQt6:
```bash
python3 ft897_packet_converter.py input.dat output.dat
```

**Q: Jak aktualizovat aplikaci?**
A: `git pull` v adresáři projektu

**Q: Mohu přesunout aplikaci jinam?**
A: Ano, ale musíte upravit cesty v .desktop souboru

---

## 🆘 Podpora

**Problémy s instalací:**
1. Přečtěte si sekci "Řešení problémů" výše
2. Zkontrolujte `debug.log`
3. Zkuste CLI verzi (funguje vždy)

**Problémy s FT-897:**
1. Ověřte, že image je z FT-897/857
2. Použijte `ft897_analyze.py` pro diagnostiku
3. Zálohujte vždy originál!

---

**Instalace je snadná!** 🚀

**73 de Claude AI 📡**
