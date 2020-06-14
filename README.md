# ImgToBraille
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⠿⣫⣿⣳⠣⡻⢾⣻⡻⡫⡪⣏⡶⢘⣻⡉⠖⠜⢓⡡⡡⠐⡎⢨⣩⡠⢂⠐⠄⠙⡀⠀⠄⢀⠁⠡⠡⡀⡁⠀⠄
⠸⠿⠿⣿⣿⡿⠿⠿⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠛⠃⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣿⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⣶⣿⡄
⠀⠀⠀⣿⣿⡇⠀⠀⠀⢸⣿⣿⠿⣿⣿⣦⠀⢼⣿⡇⠀⣶⣿⡛⠻⠿⠧⠀⠀⠀⠀⠀⢸⣿⡧⠀⣴⣿⡛⠛⠿⠧⠀⠀⠀⠀⠀⠠⢿⠿⠛⢻⣿⣆⠀⠀⠀⠀⠀⢿⣿⣿⠿⠂⢠⣾⡿⠛⢿⣿⣦⠀⣼⣿⣟⠻⠿⠦⠀⠿⣿⣿⠿⠇
⠀⠀⠀⣿⣿⡇⠀⠀⠀⢸⣿⣿⠀⢸⣿⣗⠀⣸⣿⡇⠀⠘⠿⠿⠿⣿⣦⠀⠀⠀⠀⠀⢸⣿⡷⠀⠘⠛⠿⠿⣷⣶⡀⠀⠀⠀⠀⣠⣶⡾⠿⢻⣿⣷⠀⠀⠀⠀⠀⠠⣿⣿⠀⠀⢿⣿⡿⠾⠿⠿⠿⠀⠙⠻⠿⢿⣿⣦⠀⠀⣿⣿
⠀⠀⠀⣿⣿⡇⠀⠀⠀⢸⣿⣧⠀⢸⣿⢟⠀⢸⡿⡇⠀⠻⢿⣶⣶⣿⠟⠀⠀⠀⠀⠀⢸⣿⢧⠀⠻⢿⣷⣶⣿⠿⠁⠀⠀⠀⠀⠻⣿⣷⡶⠿⣿⡿⠀⠀⠀⠀⠀⠘⢿⣿⣶⡄⠈⠻⢿⣶⣾⡿⠃⠀⠻⢿⣶⣴⣿⠟⠀⠀⢿⣿⣷⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⢐⠄⡀⠑⠂⢑⡈⡗⡄⠁⣪⠘⠊⠱⡝⢀⣍⠎⡽⠋⠕⡄⠿⡃⡇⡧⣫⣻⣴⡿⣻⣽⣟⣞⣧⣻⢟⣿⢾⡿⣷⢿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

Wanted to test some cython and opencv so I did this as a test

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

**Setup:**

```bash
git clone https://github.com/Kemaleen/ImgToBraille
cd ImgToBraille
```

Using venv:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt

deactivate   <-- exit virtualenv
```

Using Conda:

```bash
conda env create -f environment.yml
conda activate imgtobraille
```

**Usage:**

```
imgtobraille.py [-h] [-w width] [-t time] path

positional arguments:
  input          Input path (file/dir)

optional arguments:
  -h, --help     show this help message and exit
  -w width       Width of braille output in characters
  -t time        Frame time
```

Example:

```
python imgtobraille.py demos/demo.png -w 100
python imgtobraille.py demos/cube/ -w 50 -t 0.05
```
