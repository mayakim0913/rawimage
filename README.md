# Raw image viewer
**Raw image viewer** loads and parses raw images into selected color format(YUV422, RGB888, RGB565, RGBA).

Basic UI structure is generated by reading ui file 'MainGUI.ui', which is made by Qt designer.

The program based on **Python**, and uses OpenCV, Numpy, Pillow libraries (tested on 3.6.3).

## Features
> It displays the binary raw file in graphical mode and in Hex mode.
* Graphic mode: Generall image viewer mode
* Auto mode: Display raw files in all color formats
* Hex mode: Display raw files as Hex mode
> It can adjust image size, color format and check the value of each channel.
* Supported formats are YUV422(UYVY, YUYV, VYUY, YVYU), RGB888, RGB565, RGBA
> You can save the parsed file as compression image format(jpeg).

## Structure
* **Application UI Structure**
![Image_Info](./outline/Slide1.PNG)

* **Examples**
![Image_Info](./outline/Slide2.PNG)


* **File Structure**
```
rawimage/
├── icon              (Application ui icon)
│   ├── ...
├── outline           (Application outline screen shot)
│   ├── ...
├── image             (Sample raw image files)
│   ├── ...
├── __pycache__
│   ├── ...
├── MainGUI.ui        (Qt desinger ui)
├── MainGUI.py        (Coversion file from .ui to .py)
├── main.py           (Main function)
├── Parser.py         (Parsing to other color spaces)
└── LoadPicture.py    (Load sub windows for automaically showing all color spaces)
```

## Ingredients
* **Python 3.+ (tested on 3.6.3)**
  * Using PyQt5 libraries that is a Python binding to the cross-platform GUI toolkit Qt
  * Using Numpy, OpenCV, PIL, Enum libraries for processing the images
  * Using Time libraries to check Application performance
* **Qt designer**


## Prerequiste
* OS: Ubuntu and Windows (tested on Ubuntu 16.04)
* Python 3.+
* Python libraries (based on PyPI(Python Package Index))


## Getting Started 
**1) Installation (on Ubuntu 16.04)**
```
$ sudo apt-get install python3
$ sudo apt-get install python-pip
$ pip install times pytest-timeit Pillow enum34 PyQt5 opencv-python numpy
$ git clone git@github.com:mayakim0913/rawimage.git
(or git clone https://github.com/mayakim0913/rawimage)
```
**2) Installation (on Windows 10)**
* Download and execute the latest Python 3.* installation package from [here](https://www.python.org/downloads/).
* Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py). to a folder on your computer and then run python get-pip.py.
```
# ~/path_to_downloaded_folder$ python get-pip.py 
```
```
$ pip install times pytest-timeit Pillow enum34 PyQt5 opencv-python numpy
$ git clone git@github.com:mayakim0913/rawimage.git
(or git clone https://github.com/mayakim0913/rawimage)
```

**2) Usage Syntax**
```
# ~/rawimage$ python main.py
```

**3) Key board support**
* Ctrl + O: Show the file dialog to select the raw image file
* Ctrl + V: Show the file dialog to save the raw image file
* Ctrl ++: Zoom in to +0.1
* Ctrl +-: Zoom out to -0.1
* Ctrl + I: Show the application information
* Ctrl + Q: Quik the Application


**4) Default Feature**
* Color format: YUYV
* Width * Height: 400 * 400
* Console: print out time consumption


**4) Auto detection**
* Format Matching
  - If you set the format as YUV Format(YUYV, UYVY, VYUY, YVYU), it will be shown all YUV format
  - If you set the format as RGB Format(RGB, BGR, XRGB, RGBP), it will be shown all RGB format
* Channel Matching
  - If you choice only Y channel, It will be shown all YUV format with only Y channel


## Limitation
* Hex Viewer is Slow
* Some exceptions might not be handled.
* Can't load big endian image in auto detection mode
