# imgtobraille
#### Create braille unicode representations of images.
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

Learning project that involved Numpy and Numba. 

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
usage: __main__.py [-h] [-dims dimensions [dimensions ...]] [-e diffusion] [-fps fps] [-p] path

positional arguments:
  path                  Path to file or directory

optional arguments:
  -h, --help            show this help message and exit
  -dims dimensions [dimensions ...]
                        width and height of output as characters. Use 0 for automatic terminal width/height
  -e diffusion          error diffusion level, range 0-1. 0=no dithering, 1=full error diffusion.
  -fps fps              Fps for animation
  -p                    Whether to prerender all frames before animating.

```

Example:

```
python -m imgtobraille ./demos/demo.jpg -dims 35
```
Outputs:
```
⠀⠀⠀⠀⠀⠀⠀⠀⢠
⠀⠀⢠⣴⣶⣿⣶⡄⠀⠀⠀⠀⠀⡀
⠀⠀⢸⡿⠀⠀⣿⣿⢂⣠⣾⠿⠿⣿⣿⣦⠀⠀⣺⣿⣷⣿⣿⣿⣧⣶⣿⣷⣀⠀⣠⣶⣤⡀
⠀⠀⢸⡇⠀⢀⣿⠃⣾⣟⣅⣄⣴⣿⡟⢁⣰⣾⣿⠿⠋⠁⣩⣿⡿⠋⢉⣿⡟⢰⣿⠉⢹⡧
⠀⠀⢸⡇⠀⢰⣿⠀⢿⣟⠛⠛⠻⠻⠁⢸⣿⣿⡗⠀⠀⣶⣿⡟⠁⠀⣾⣿⠠⣿⡇⠀⣽⠇
⠀⠀⠘⢻⡿⢿⠟⠀⠘⠻⣧⣤⣼⣿⡷⠀⢹⣿⣷⠀⠀⢻⣿⣇⠀⠀⣿⣷⠀⠹⣿⡾⠛
⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠘⠉⠙⠉⠁⠀⠀⠉⠋⠁⠀⠈⠉⠙⠂⠀⠁⠓⠀⠈⠁⠁
⠀⠀⠀⠀⠀⠀⠀⠀⣀
⠀⠀⡀⠒⠒⠒⠂⡀⠑⠃
⠀⢀⡇⢰⠶⢦⠠⠸⣄⡰⠚⠉⠉⠉⠲⢄⠄⢈⠉⠉⠷⠉⠉⠑⢶⠊⠛⠦⡀⢀⡤⠦⢀⡠
⠀⢸⠂⠈⠀⡞⠀⡼⠋⢠⠔⢰⠎⠀⢀⣜⠖⠂⠀⠀⡠⢖⡆⠀⢀⡠⡄⠀⣹⡎⢀⢄⠀⣶
⠀⢸⠀⠀⠀⠇⠀⡇⠀⡀⠀⠀⠀⠀⡏⡆⠀⠀⣴⠋⡤⠛⠁⢠⡜⢡⠁⠀⡟⠀⠘⠸⠀⡗
⠀⠀⡇⠈⠉⠀⢠⠑⡄⠘⠣⠭⠙⠛⢣⣣⠀⠀⢳⠀⢻⠀⠀⢠⠀⡇⠀⣼⢧⠀⠓⠃⢠⠁
⠀⠀⠈⠯⠖⠒⠈⠀⠈⠲⠄⠀⠀⠀⠎⠈⠃⠀⠀⠇⠈⠄⠤⠼⠄⠧⠖⠚⠸⠁⠦⠪⠑
```
