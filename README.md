# music-ripper
Given screenshot, download songs

## Requirements (Arch):
* `make`
* `python`
* `python-pip`
* `tesseract` 
* `tesseract-data-eng` (probably not the whole group of `tesseract-data`, but you could to be safe)
* `ffmpeg`

## Setup (after installing above):
* `make pip`

## Arch setup shorthand: `make bootstrap-arch`

## Usage:
`make run`
or just `python3 ripper.py`

Optional arg is a newline seperated list of songs. Ex: `python3 ripper.py test_data/country-1.txt`