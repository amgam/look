#Look - py-based image search engine

### Setup

There's a couple of packages that you'll need. Firstly you'll need pip, a python package manager.

fire up terminal and run
```
sudo easy_install pip
```

With pip now installed, grab the following:
```
pip install flask numpy scipy matplotlib gunicorn 
```
Lastly, you'll need to install OpenCV. Go ahead and grab Homebrew, another pack.manager
```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Then, 
```
brew install python
brew tap homebrew/science
brew install opencv

cat ~/.bash_profile | grep PYTHONPATH
ln -s /usr/local/Cellar/opencv/2.4.12/lib/python2.7/site-packages/cv.py cv.py
ln -s /usr/local/Cellar/opencv/2.4.12/lib/python2.7/site-packages/cv2.so cv2.so
```
For details on installing OpenCV, check [this](http://www.mobileway.net/2015/02/14/install-opencv-for-python-on-mac-os-x/) out. Remember to change the version numbers accordingly!

hopefully, you've got all your parts, its time to rev up. Navigate to the folder and run
```
python app/aria.py
```
It should tell you the URL that the local server is running off.

look intialized.
