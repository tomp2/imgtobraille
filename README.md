⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⠿⣫⣿⣳⠣⡻⢾⣻⡻⡫⡪⣏⡶⢘⣻⡉⠖⠜⢓⡡⡡⠐⡎⢨⣩⡠⢂⠐⠄⠙⡀⠀⠄⢀⠁⠡⠡⡀⡁⠀⠄
⠸⠿⠿⣿⣿⡿⠿⠿⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠛⠃⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣿⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⣶⣿⡄
⠀⠀⠀⣿⣿⡇⠀⠀⠀⢸⣿⣿⠿⣿⣿⣦⠀⢼⣿⡇⠀⣶⣿⡛⠻⠿⠧⠀⠀⠀⠀⠀⢸⣿⡧⠀⣴⣿⡛⠛⠿⠧⠀⠀⠀⠀⠀⠠⢿⠿⠛⢻⣿⣆⠀⠀⠀⠀⠀⢿⣿⣿⠿⠂⢠⣾⡿⠛⢿⣿⣦⠀⣼⣿⣟⠻⠿⠦⠀⠿⣿⣿⠿⠇
⠀⠀⠀⣿⣿⡇⠀⠀⠀⢸⣿⣿⠀⢸⣿⣗⠀⣸⣿⡇⠀⠘⠿⠿⠿⣿⣦⠀⠀⠀⠀⠀⢸⣿⡷⠀⠘⠛⠿⠿⣷⣶⡀⠀⠀⠀⠀⣠⣶⡾⠿⢻⣿⣷⠀⠀⠀⠀⠀⠠⣿⣿⠀⠀⢿⣿⡿⠾⠿⠿⠿⠀⠙⠻⠿⢿⣿⣦⠀⠀⣿⣿
⠀⠀⠀⣿⣿⡇⠀⠀⠀⢸⣿⣧⠀⢸⣿⢟⠀⢸⡿⡇⠀⠻⢿⣶⣶⣿⠟⠀⠀⠀⠀⠀⢸⣿⢧⠀⠻⢿⣷⣶⣿⠿⠁⠀⠀⠀⠀⠻⣿⣷⡶⠿⣿⡿⠀⠀⠀⠀⠀⠘⢿⣿⣶⡄⠈⠻⢿⣶⣾⡿⠃⠀⠻⢿⣶⣴⣿⠟⠀⠀⢿⣿⣷⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⢐⠄⡀⠑⠂⢑⡈⡗⡄⠁⣪⠘⠊⠱⡝⢀⣍⠎⡽⠋⠕⡄⠿⡃⡇⡧⣫⣻⣴⡿⣻⣽⣟⣞⣧⣻⢟⣿⢾⡿⣷⢿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

Small project to learn some image processing with cython + OpenCV

---
**Setup:**

```bash
git clone https://github.com/Kemaleen/ImgToBraille
cd ImgToBraille
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
_Exit virtualenv with:_
```
deactivate
```

---

**Usage:**

```
python imgtobraille [-h] [-w width] [-d dithering] [-t time] path

positional arguments:
  path          Input path (file/dir)

optional arguments:
  -h, --help    show this help message and exit
  -w width      Width of print in characters
  -d dithering  1=threshold, 2=Floyd–Steinberg, 3=random, 4=none
  -t time       Frame time in seconds
```

Examples:

```
python imgtobraille demos/demo.png -w 100
python imgtobraille demos/cube/ -w 50 -t 0.05
```
