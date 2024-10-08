# AlmaPrintGrid : Application for printing items call numbers by scaning barcodes

![forthebadge](img/made-with-python-tkinter.svg)

**Status** : to be continued...

---

## Goals

Scan items barcodes, retrieve items callnumbers from **Exlibris Alma API** and populate a ready-to-print grid template.

## Development

### Install 

```
git clone https://github.com/gegedenice/alma-print-grid.git
```

### Environment variables

- Copy the .sample.env file nad rename in .env.
- Fill with your Alma API Key

### Virtualenv

Create a virtualenv 

Windows
```
python -m venv .venv
cd .venv/Scripts & activate
```
Linux

```
python3 -m venv .venv
source .venv/bin/activate
```

Then `pip install -r requirements.txt`

### Run

`python app.py`

## Build package with cx_Freeze

The  command
```
python setup.py build
```
compiles the files and generates a `build` folder with the executable app.exe inside.

## How it works

### In dev mode (UI styling)

Call numbers data are coming from the `dummy_item_data.json` file and not the Alma API.

Press Enter ky in each cell to fill a popup with whatever value, the `AlmaClient.dummy_search_item` method is then called and returns the value "320.08 TIF" from the dummy_item_data.json file.

![screenshot](img/screenshot.png)

### In production

- In `app.py`, change the 
  `item_value = AlmaClient.dummy_search_item(format="call-number",item_barcode=barcode)` 

   line in the `process_barcode` function to

  `item_value = AlmaClient.search_item(format="call-number",item_barcode=barcode)`

  to request Alma API on real barcodes.

2. Todo : in `app.py`, remplace `barcode = simpledialog.askstring("Scan Barcode",     "Please enter the barcode:")` with a real reading of scaned value process

### Todo

- when splitting the callnumber, the second part is displayed in first place, eg "DIFF \n 325.3" instead of "325.3 \n DIFF"

