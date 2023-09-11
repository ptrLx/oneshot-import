# OneShot import

Import images from the past into your [OneShot](https://github.com/ptrLx/OneShot) app.

## Requirements

* clone this repo
* install Python 3.11
* install pipenv (`pip install pipenv --user`)
* run `pipenv install` and `pipenv shell`
* now run the script (`python3 src/main.py`)

## How it works

* select images from different dates that you want to import into your OneShot diary
* copy them into the `image` folder
* now run `src/main.py`
* it will generate a `import-me.json`
* copy the images into your OneShot folder on your device and use the import feature of the app to import the `import-me.json`:
  <div style="display:flex;">
  <img alt="screenshot_1" src="assets/screenshot_1.jpg" width="30%">
  <img style="padding-left: 8px;" alt="screenshot_2" src="assets/screenshot_2.jpg" width="30%">
  </div>
