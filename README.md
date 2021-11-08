```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠔⠒⠉⠘⡉⠒⠤⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠴⠊⠁⠀⠀⠀⠀⠀⢡⣀⠴⠒⢿
⠀⠀⠀⠀⠀⠀⢠⠔⠂⠁⠀⠀⠀⠀⠀⢀⣀⠤⠒⠉⠆⠀⠀⠈⡆
⠀⠀⠀⠀⠀⡰⠁⠑⢄⠀⠀⣀⠤⠔⠊⠁⠀⠀⠀⠀⠘⡀⠀⠀⢱
⠀⠀⠀⢀⠜⠀⢀⡠⠤⢒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢡⠀⠀⠀⡇
⠀⠀⢀⣎⠤⠚⠁⠀⠀⠀⠣⠀⠀⠀⠀⠀⠀⠀⣀⠤⠐⠁⠣⠀⠀⢸
⠀⠀⠈⠦⡀⠀⠀⠀⠀⠀⠀⠑⠄⣀⠤⠐⠂⠁⠀⠀⠀⠀⠀⠉⢄⠀⡆
⠀⠀⠀⠀⠑⢄⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡸
⠀⠀⠀⠀⠀⠀⠱⢄⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⡇
⠀⠀⠀⠀⠀⠀⠀⠈⠣⡀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⠤⠚⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡀⢸⠀⠀⠀⠀⣀⠤⠔⠒⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠼⠤⠒⠈⠉
```

Learning project that involced Numpy, cython and numba. 

Goal was to create braille unicode representation of an image, where each braille dot represents one pixel in the image.

---
**Setup:**

```bash
git clone https://github.com/tomp2/imgtobraille
cd imgtobraille
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```
Exit virtualenv with:
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
python imgtobraille ./demos/demo.png -w 100
python imgtobraille ./demos/cube/ -w 50 -t 0.05
```
