# detection-bias
Scripts to quantify the galaxy detection bias in cosmic shear measurements

# Detection Bias in Cosmic Shear Measurements

This repository contains scripts developed during my Master's thesis to quantify and correct detection biases in galaxy shape measurements for cosmic shear analyses. It includes tools for realistic galaxy simulation, injection into survey tiles, catalog comparison after detection, and computation of detection probabilities as weights for shear correlation functions.

---

## 📁 Project Structure


---

## Main Components

### 1. `KiDSGalaxyInjector`
Generates realistic galaxy images with GalSim using KiDS-like parameters and injects them into survey tiles.

### 2. `CatalogComparator`
Compares injected catalogs with SExtractor-detected sources to quantify the detection efficiency and biases.

### 3. `GalaxyWeightAssigner`
Assigns weights to galaxies using a precomputed detection probability function. 

---

## 🔧 Requirements

You can install all dependencies via:

```bash
pip install -r requirements.txt

