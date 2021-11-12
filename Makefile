run:
	python3 ripper.py
arch:
	sudo pacman -S --noconfirm --needed make python python-pip tesseract tesseract-data-eng ffmpeg
pip:
	python3 -m pip install -r requirements.txt

bootstrap-arch: arch pip