# FT-897 Memory Manager - Windows Průvodce

**Verze pro Windows bez instalace závislostí!**

## 🎯 Rychlý start (Windows)

### Krok 1: Zkontrolujte Python

Otevřete **Command Prompt** (cmd) a zadejte:

```cmd
python --version
```

**Měli byste vidět:** `Python 3.7.x` nebo novější

**Pokud ne**, nainstalujte Python:
1. Stáhněte z https://www.python.org/downloads/
2. Při instalaci **zaškrtněte** "Add Python to PATH"
3. Restartujte počítač

### Krok 2: Spusťte GUI aplikaci

**Jednoduchý způsob:**
```cmd
Dvojklik na:  run_gui.bat
```

**Nebo z příkazové řádky:**
```cmd
python ft897_gui_tkinter.py
```

**To je vše!** Žádná instalace balíčků není potřeba! 🎉

---

## 📦 Dvě verze GUI

### ✅ **Tkinter GUI** (DOPORUČENO pro Windows)

```cmd
python ft897_gui_tkinter.py
```

**Výhody:**
- ✅ **Žádné závislosti** - funguje hned!
- ✅ Součást Python standardní knihovny
- ✅ Malé, rychlé, spolehlivé
- ✅ Nativní Windows vzhled

**Použijte tuto verzi!**

### ⚠️ PyQt6 GUI (volitelné)

```cmd
pip install PyQt6
python ft897_gui.py
```

**Výhody:**
- Modernější vzhled
- Více funkcí

**Nevýhody:**
- ⚠️ Vyžaduje instalaci PyQt6 (může selhat na Windows)
- ⚠️ Větší závislost

**Není potřeba na Windows!** Tkinter verze je lepší volba.

---

## 🎨 Tkinter GUI - Funkce

### Hlavní funkce

- **📂 Načítání/ukládání image souborů**
  - File → Load Image (Ctrl+O)
  - File → Save (Ctrl+S)
  - File → Save As...

- **📊 Tabulka všech kanálů**
  - Zobrazení všech používaných kanálů
  - Barevné zvýraznění:
    - 🟢 Zelená = PKT mód
    - 🟡 Žlutá = 2m repeater

- **✏️ Editor kanálu**
  - Dvojklik na řádek v tabulce
  - Úprava frekvence, módu, duplex, offset, názvu
  - Příznaky: Skip, IPO, ATT

- **🔄 Batch operace**
  - Tools → Convert 2m to PKT
  - Automatická konverze všech 2m repeaterů

- **📈 Statistiky**
  - Tools → Statistics
  - Přehled pásem a módů

### Klávesové zkratky

| Klávesa | Akce |
|---------|------|
| **Ctrl+O** | Načíst image |
| **Ctrl+S** | Uložit |
| **Ctrl+Q** | Ukončit |
| **Dvojklik** | Editovat kanál |

---

## 📝 Návod krok za krokem

### 1. Zálohujte paměť rádia

Použijte programovací software (CHIRP, FTBasicMMO, RT Systems) pro vytvoření zálohy:
- Uložte jako `ft897_backup.dat`

### 2. Spusťte GUI

**Způsob A - Jednoduchý (doporučeno):**
```cmd
Dvojklik na: run_gui.bat
```

**Způsob B - Z příkazové řádky:**
```cmd
cd cesta\k\Radio-player
python ft897_gui_tkinter.py
```

### 3. Načtěte image

1. **File → Load Image...** (nebo Ctrl+O)
2. Vyberte `ft897_backup.dat`
3. Tabulka se naplní kanály

### 4. Prohlédněte kanály

- **Tabulka** ukazuje všechny kanály
- **Žlutá** = 2m repeater (kandidát na konverzi)
- **Zelená** = Již v PKT módu

### 5. Upravte kanál (volitelné)

1. **Dvojklik** na řádek
2. Upravte parametry v dialogu
3. Klikněte **OK**

### 6. Konvertujte 2m repeatery na PKT

1. **Tools → Convert 2m to PKT**
2. Potvrďte operaci
3. Všechny 2m repeatery se změní na PKT mód

### 7. Uložte změny

1. **File → Save** (nebo Ctrl+S)
2. Soubor je aktualizován

### 8. Nahrajte zpět do rádia

1. Otevřete programovací software
2. Načtěte upravený `ft897_backup.dat`
3. Odešlete do rádia
4. Zkontrolujte na rádiu

---

## 🐛 Řešení problémů (Windows)

### "Python is not recognized..."

**Problém:** Python není v PATH

**Řešení:**
1. Přeinstalujte Python
2. **ZAŠKRTNĚTE** "Add Python to PATH"
3. Restartujte počítač

### GUI se nespustí

**Zkontrolujte Python verzi:**
```cmd
python --version
```

**Musí být 3.7 nebo novější!**

**Zkontrolujte Tkinter:**
```cmd
python -c "import tkinter; print('OK')"
```

**Mělo by vypsat:** `OK`

### Soubory .dat nelze otevřít

1. Zkontrolujte, že soubor není poškozený
2. Zkuste jinou zálohu
3. Ujistěte se, že je to opravdu FT-897 image

### Ikony (emoji) se nezobrazují správně

To je v pořádku - funkce aplikace není ovlivněna. Windows může mít problémy s emoji v některých fontech.

---

## 💻 CLI Nástroje (alternativa)

Pokud nechcete GUI, můžete použít příkazovou řádku:

### Analýza image

```cmd
python ft897_analyze.py ft897_backup.dat
```

### Konverze 2m→PKT

```cmd
python ft897_packet_converter.py ft897_backup.dat ft897_modified.dat
```

**CLI nepotřebuje žádné závislosti!**

---

## 📊 Porovnání verzí

| Funkce | Tkinter GUI | PyQt6 GUI | CLI |
|--------|-------------|-----------|-----|
| **Žádné závislosti** | ✅ | ❌ | ✅ |
| **Funguje na Windows** | ✅ | ⚠️ | ✅ |
| **Tabulka kanálů** | ✅ | ✅ | ❌ |
| **Editor kanálů** | ✅ | ✅ | ❌ |
| **Batch operace** | ✅ | ✅ | ✅ |
| **Statistiky** | ✅ | ✅ | ✅ |
| **Rychlost** | ⚡⚡⚡ | ⚡⚡ | ⚡⚡⚡ |

**Pro Windows použijte Tkinter GUI!** ✅

---

## 📁 Struktura souborů

```
Radio-player/
│
├── 🖥️ GUI Aplikace (Windows)
│   ├── ft897_gui_tkinter.py  ← TOTO SPUSŤTE!
│   ├── run_gui.bat            ← Nebo toto (dvojklik)
│   └── ft897_memory.py        ← Backend (nutný)
│
├── 🖥️ GUI Aplikace (PyQt6 - volitelné)
│   ├── ft897_gui.py           ← Vyžaduje PyQt6
│   └── run_gui.sh             ← Pro Linux/Mac
│
├── 💻 CLI Nástroje
│   ├── ft897_packet_converter.py
│   ├── ft897_analyze.py
│   └── test_ft897_converter.py
│
└── 📚 Dokumentace
    ├── README_WINDOWS.md      ← Tento soubor
    ├── README.md
    ├── README_GUI.md
    └── QUICK_START_CZ.md
```

---

## ⚠️ Důležitá upozornění

### Před použitím

1. ⚠️ **VŽDY SI ZÁLOHUJTE ORIGINÁLNÍ IMAGE!**
   - Vytvořte kopii: `ft897_backup_ORIGINAL.dat`

2. ⚠️ **Testujte v bezpečném prostředí**
   - Nejdřív načtěte do programovacího SW
   - Zkontrolujte náhled
   - Teprve pak nahrajte do rádia

3. ⚠️ **Program vytvořen reverse-engineeringem**
   - Není oficiálně podporován Yaesu
   - Použití na vlastní riziko

### Doporučený workflow

```
1. Záloha z rádia
   → ft897_original.dat

2. Kopie zálohy (pojistka!)
   → ft897_backup.dat

3. Úprava v GUI
   → ft897_modified.dat

4. Test v programovacím SW
   → Náhled kanálů

5. Nahrání do rádia
   → Opatrně!

6. Kontrola na rádiu
   → Zkontrolujte 2m kanály
```

---

## 📚 Dodatečné zdroje

### Programovací software pro FT-897

**Zdarma:**
- **CHIRP** - https://chirpmyradio.com/
- **FTBasicMMO** - https://www.m0lxq.com/g4hfq/

**Komerční:**
- **RT Systems ADMS-4B** - https://www.rtsystemsinc.com/

### Dokumentace

- Yaesu FT-897 Manual
- FT-897 CAT Commands
- CHIRP Documentation

---

## ❓ FAQ

**Q: Potřebuji PyQt6?**
A: **NE!** Použijte `ft897_gui_tkinter.py` - funguje bez instalace!

**Q: Funguje to na Windows 10/11?**
A: **ANO!** Python 3.7+ je vše, co potřebujete.

**Q: Mohu používat CLI nástroje?**
A: **ANO!** CLI funguje stejně dobře jako GUI.

**Q: Je to bezpečné?**
A: **ANO**, pokud si zálohujete originál a testujete před nahráním.

**Q: Podporuje to FT-857?**
A: **ANO**, FT-857 a FT-897 používají stejný formát.

---

## 🆘 Pomoc a podpora

**Problémy s Windows:**
1. Restartujte počítač
2. Zkontrolujte Python verzi
3. Zkuste `run_gui.bat`

**Problémy s image:**
1. Použijte `ft897_analyze.py` pro diagnostiku
2. Zkuste jinou zálohu
3. Ověřte, že je to opravdu FT-897 image

**Další pomoc:**
- Přečtěte si README.md
- Prohlédněte si příklady v dokumentaci

---

## ✅ Checklist pro začátečníky

- [ ] Python 3.7+ nainstalován
- [ ] Python v PATH (restartovat po instalaci)
- [ ] Záloha z rádia vytvořena (.dat soubor)
- [ ] Kopie zálohy (pojistka!)
- [ ] Spuštěn `run_gui.bat`
- [ ] Image načten v GUI
- [ ] Kanály zkontrolovány
- [ ] Úpravy provedeny
- [ ] Soubor uložen
- [ ] Testováno v programovacím SW
- [ ] Nahráno do rádia
- [ ] Zkontrolováno na rádiu

---

**Vytvořeno pro Windows uživatele 💙**

**Žádné komplikace, žádná instalace - prostě to funguje!** ✅

**73 de Claude AI 📡**
