# OneShot import

Import images from the past into your [OneShot](https://github.com/ptrLx/OneShot) app.

## How it works

* follow the [Development instructions](#development) to run the app

<!-- * download the [latest release](https://github.com/ptrLx/oneshot-import/releases/latest) for your os
* create a folder `image` in the same folder as the executable -->
* select images from different dates that you want to import into your OneShot diary and copy them into the `image` folder
* start the executable
* it will generate a `import-me.json`
* copy the images into your OneShot folder on your device and use the import feature of the app to import the `import-me.json`:
  <div style="display:flex;">
  <img alt="screenshot_1" src="assets/screenshot_1.jpg" width="30%">
  <img style="padding-left: 8px;" alt="screenshot_2" src="assets/screenshot_2.jpg" width="30%">
  </div>

## Usage

```
usage: main.py [-h] [-y] [--summarize] [--no-summarize] [-p PATH] [-o OUTPUT] [--default-text DEFAULT_TEXT]
               [--default-happiness {NOT_SPECIFIED,VERY_HAPPY,HAPPY,NEUTRAL,SAD,VERY_SAD}] [--gui] [--auto] [--no-auto] [--no-gui]

Import images from the past into OneShot.

options:
  -h, --help            show this help message and exit
  -y, --yes             no confirmation request
  --summarize           summarize import results
  --no-summarize        disable summarization
  -p PATH, --path PATH  specify a path where the images are located
  -o OUTPUT, --output OUTPUT
                        specify a path where the export should be stored
  --default-text DEFAULT_TEXT
                        specify default text
  --default-happiness {NOT_SPECIFIED,VERY_HAPPY,HAPPY,NEUTRAL,SAD,VERY_SAD}
                        specify default happiness level
  --gui                 start the gui
  --auto                automatically pick an image if a date collision happens
  --no-auto             disable automatic decision on date collision (OneShots will still win over other images)
  --no-gui, --cli       use the cli
```

## Development

* clone this repo
* install Python 3.11 and tkinter
* install pipenv (`pip install pipenv --user`)
* add pipenv to the PATH (Windows)
* run `make setup`
* start the script: `make start`
