

[![PyPI version](https://badge.fury.io/py/motmetrics.svg)](https://badge.fury.io/py/motmetrics) [![](https://travis-ci.org/cheind/py-motmetrics.svg?branch=master)](https://travis-ci.org/cheind/py-motmetrics)

## py-motmetrics[simplify]

Original Py-Motmetrics is not very easy to use. So I have a simplified package.


### Installation

#### PyPi and development installs

```
git clone https://github.com/carry-xz/py-motmetrics-simplify
cd py-motmetrics 
pip install -e . 
```

### Usage

#### Populating the accumulator

```python
import motmetrics as mm

gt_file = './motmetrics/data/TUD-Campus/gt.txt'
dt_file = './motmetrics/data/TUD-Campus/test.txt'
summary = mm.simpeval(gt_file, dt_file)

## list is ok 
## ['FrameId', 'Id', 'X', 'Y', 'Width', 'Height', 'Confidence', 'ClassId', 'Visibility', 'unused']

gt_list = [
  [1,1,399,182,121,229,1,-1,-1,-1],
  [1,2,282,201,92,184,1,-1,-1,-1],
  [1,3,63,153,82,288,1,-1,-1,-1],
  [1,4,192,206,62,137,1,-1,-1,-1],
  [1,5,125,209,74,157,1,-1,-1,-1],
  [1,6,162,208,55,145,1,-1,-1,-1],
  [2,1,399,181,139,235,1,-1,-1,-1],
  [2,2,269,202,87,182,1,-1,-1,-1],
  [2,3,71,151,100,284,1,-1,-1,-1],
  ]

dt_list = [
    [1,3,113.84,274.5,57.307,130.05,-1,-1,-1,-1],
    [1,6,273.05,203.83,77.366,175.56,-1,-1,-1,-1],
    [1,10,416.68,205.54,91.04,206.59,-1,-1,-1,-1],
    [1,13,175.02,195.54,60.972,138.36,-1,-1,-1,-1],
    [2,3,116.37,265.2,62.858,142.64,-1,-1,-1,-1],
    [2,6,267.86,202.71,77.704,176.33,-1,-1,-1,-1],
    [2,10,423.95,203.42,91.88,208.5,-1,-1,-1,-1],
    [2,13,177.14,202.51,58.209,132.09,-1,-1,-1,-1],
    [3,3,118.93,255.89,68.408,155.24,-1,-1,-1,-1],
    [3,6,262.73,201.65,78.033,177.08,-1,-1,-1,-1],
    [3,10,431.14,201.32,92.719,210.4,-1,-1,-1,-1],
    [3,13,179.21,209.5,55.445,125.82,-1,-1,-1,-1],
]

summary = mm.simpeval(gt_list, dt_list)

```


### License

```
MIT License

Copyright (c) 2017-2020 Christoph Heindl
Copyright (c) 2018 Toka
Copyright (c) 2019-2020 Jack Valmadre

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


[Pandas]: http://pandas.pydata.org/
[MOTChallenge]: https://motchallenge.net/
[devkit]: https://motchallenge.net/devkit/

