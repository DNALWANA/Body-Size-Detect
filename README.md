# Body Size Detected
This project is a real-time computer vision application built with **Python**, **OpenCV**, and **MediaPipe** that analyzes body proportions using a webcam. By calculating the ratio between the user's waist and shoulder widths, the program dynamically classifies the body shape as either "IDEAL" or "GEMUK" (Overweight). To make the experience interactive and entertaining, it features an asynchronous AI voice feedback system using **gTTS** and **threading**, which triggers humorous Indonesian audio commentary without lagging the video feed whenever the user's classification changes.
## Key Features

* **Real-time Detections:** Identify people and determine their categories.
* **Two Different Category:** Can differentiate operson seen based on two category, "Gemuk" (Overweight) and "Ideal" (Ideal).
* **Obesity Detector:** Assist in rapid camera-based obesity category screening.

## Screenshots

| "Gemuk" Body | "Ideal" Body | 
| :---: | :---: |
| ![Gemuk exp](./assets/Screenshot%20from%202026-01-23%2022-02-52.png) | ![Ideal exp](./assets/Screenshot%20from%202026-01-23%2022-05-07.png) | 

## Dependencies

### 1. Person placement must be straight
   If someone is not standing level facing the camera the calculation can be wrong.
### 2. Strict grease detector
   The program is designed strictly at a hip width of 0.60, even though it should be more than 0.65 to be considered fat. This design is deliberately made strict for people who want to diet.
### 3. Library
To run this project, you need Python installed along with the following libraries:

* opencv-python
* numpy<2.0.0,>=1.26.0
* gTTS
* pygame
* mediapipe

## Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/DNALWANA/Body-Size-Detect.git
    cd Body-Size-Detect
    ```

2.  **Install requirements**
    ```bash
    pip install -r requirment.txt
    ```

## Usage
```bash
python3 bodycount.py
```

## How to run the program

### 1. Detection Person
Point the person in front of the camera and let the system detect it.
### 2. Categorize Person
The program will categorize people by calculating the waist width and comparing it to the shoulders.
### 3. Calculate the Object
If a person is detected to have a waist width that is close to or exceeds the shoulder width, they will be categorized as "Gemuk" (overweight), fat category when detection is more than 0.60.
### 4. Press 'Q' to stop the program


