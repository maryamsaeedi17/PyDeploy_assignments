from typing import Union, List
import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

@app.get("/")
def introduction():
    return {"Hello and welcome to my solar system API!",
            "My API provides you image and some information about 8 planets of the solar system🌌."}

@app.get("/planets")
def planets():
    planets_list = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    # planets_list = "Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune"
    return{"Name of 8 planets in order of distance from sun": planets_list }

@app.get("/planets/{planet_name}")
def planet_info(planet_name: str):
    if planet_name == "mercury":
        info = "Mercury is the closest planet to the Sun, and the smallest planet in our solar system - only slightly larger than Earth's Moon. For more information visit https://science.nasa.gov/mercury/facts/"
    elif planet_name == "venus":
        info = "Venus is the second planet from the Sun, and the sixth largest planet. It’s the hottest planet in our solar system. For more information visit https://science.nasa.gov/venus/venus-facts/"
    elif planet_name == "earth":
        info = "Earth – our home planet – is the third planet from the Sun, and the fifth largest planet. It's the only place we know of inhabited by living things. For more information visit https://science.nasa.gov/earth/"
    elif planet_name == "mars":
        info = "Mars is the fourth planet from the Sun, and the seventh largest. It’s the only planet we know of inhabited entirely by robots. For more information visit https://science.nasa.gov/mars/facts/"
    elif planet_name == "jupiter":
        info = "Jupiter is the fifth planet from the Sun, and the largest in the solar system – more than twice as massive as the other planets combined. For more information visit https://science.nasa.gov/jupiter/facts/"
    elif planet_name == "saturn":
        info = "Saturn is the sixth planet from the Sun, and the second largest in the solar system. It’s surrounded by beautiful rings. For more information visit https://science.nasa.gov/saturn/facts/"
    elif planet_name == "uranus":
        info = "Uranus is the seventh planet from the Sun, and the third largest planet in our solar system. It appears to spin sideways. For more information visit https://science.nasa.gov/uranus/facts/"
    elif planet_name == "neptune":
        info = "Neptune is the eighth, and most distant planet from the Sun. It’s the fourth-largest, and the first planet discovered with math. For more information visit https://science.nasa.gov/neptune/facts/"
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Planet name must be one of 8 main planet of solar system, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune.")

    return{f"Information of {planet_name}" : info}


@app.get("/planets/{planet_name}/image")
def planet_info(planet_name: str):
    if planet_name == "mercury":
        img = cv2.imread("assets/planets/mercury.jpg")
    elif planet_name == "venus":
        img = cv2.imread("assets/planets/venus.jpg")
    elif planet_name == "earth":
        img = cv2.imread("assets/planets/earth.jpg")
    elif planet_name == "mars":
        img = cv2.imread("assets/planets/mars.jpg")
    elif planet_name == "jupiter":
        img = cv2.imread("assets/planets/jupiter.jpg")
    elif planet_name == "saturn":
        img = cv2.imread("assets/planets/saturn.jpg")
    elif planet_name == "uranus":
        img = cv2.imread("assets/planets/uranus.jpg")
    elif planet_name == "neptune":
        img = cv2.imread("assets/planets/neptune.jpg")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Planet name must be one of 8 main planet of solar system, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune.")
    
    _, encode_img = cv2.imencode(".png", img)
    return StreamingResponse(content=io.BytesIO(encode_img.tobytes()), media_type = "image/png")
