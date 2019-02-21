# Raw image viewer
It loads **Raw image files** on Qt ui display and converts it to **color format**(YUV422, RGB888, RGB565, RGBA) 
and save to compression image format(JPEG, PNG)

Form implementation is generated from reading ui file 'MainGUI.ui' by Qt designer

The program based on **Python**, and uses OpenCV, Numpy, Pillow libraries (tested on 3.7.0).

## Features
> It can disply the binary raw file in graphical mode and in Hex mode using Qt ui.
* Graphic mode: Generall image viewer mode
* Auto mode: Display raw files in all color formats
* Hex mode: Display raw files as Hex mode
> It can adjust image size, color format conversion, and check the value of each channel.
* Supported formats are YUV422(UYVY, YUYV, VYUY, YVYU), RGB888, RGB565, RGBA
> You can save the checked file as compression image format (jpeg, png).

## Structure
* **Application structure**
![Image_Info](./outline/Slide1.PNG)

* **Examples**
![Image_Info](./outline/Slide2.PNG)


* **File Structure**
```ruby
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
* **Python 3.6 + (tested on 3.7.0)**
  * Using PyQt5 libraries thay is a Python binding of the cross-platform GUI toolkit Qt
  * Using Numpy, OpenCV, PIL, Enum libraries for processing the images
  * Using Time libraries to check Application performance
* **Qt designer**


## Prerequiste
* OS: Ubuntu and Windows (tested on Ubuntu 16.04)
* Python 3.6(+=)
* Python libraries (based on PyPI(Python Package Index))


## Getting Started 
**1) Installation (on Ubuntu 16.04)**
```ruby
$ sudo apt-get install python3
$ curl -k -O https://bootstrap.pypa.io/get-pip.py
$ python get-pip.py
$ pip install times pytest-timeit Pillow enum PyQt5 opencv-python numpy
```

**2) Usage Syntax**
```ruby
$ python main.py
```

**3) Key board support**
* Ctrl + O: Show the file dialog to select the raw image file
* Ctrl + O: Show the file dialog to save the raw image file
* Ctrl ++: Zoom in to +0.1
* Ctrl +-: Zoom out to -0.1
* Ctrl + i: Show the application information
* Ctrl + q: Quik the Application


**4) Default Feature**
* Color format: YUYV
* Width * Height: 400 * 400
* Console: print out time consumption


## Limitation
* Hex Viewer Slow
* try - Exception not all processed
* not to be load for large size than original file w*h size
* "swap" doen't work
* Each channel value onlu can be seen in Auto detection mode
* Endian not be worked
* want h*w > file h*w => if - else statement!
