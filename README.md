# python_adb
python adb tool for Litbig on Mac OS

# Commands

## 1. parameter 1

### 1) help
모든 커맨드 보기

    python3 main.py help

### 2) current
현재 activity 보기

    python3 main.py current

### 3) volume
모든 stream volume 보기

    python3 main.py volume

### 4) screencap
화면 스크린 캡쳐

    python3 main.py screencap

## 2. parameter 2

### 1) project
프로젝트 설정

[project]: benz_sb, benz_sg, ka4, scania, dpeco, hlab

    python3 main.py project [project]

### 2) fastboot
이미지 fastboot

[img]: system, vendor, boot, ...

    python3 main.py fastboot [img]

### 3) launch
앱 실행

[app]: allapps, settings, documents, polnav, launcher, ...

    python3 main.py launch [app]

### 4) broadcast
broadcast action 송신

[action]: boot_completed, ...

    python3 main.py broadcast [action]

### 5) key
KeyEvent keycode 전송

[keyCode]: home, back, A, B, ...

    python3 main.py key [keyCode]

### 6) version
앱 버전 보기

[app]: allapps, settings, documents, polnav, launcher, ...

    python3 main.py version [app]

### 7) volume
stream volume 보기

[stream]: system, ring, music, alarm, notification, ...

    python3 main.py volume [stream]

## 3. parameter 3

### 1) volume
stream volume 설정

[stream]: system, ring, music, alarm, notification, ...

[volume]: 0 ~ x

    python3 main.py volume [stream] [volume]

### 2) polnav
polnav api request

[extra]: VOLUME, ...

[value]: 0 ~ 30, ...

    python3 main.py polnav [extra] [value]