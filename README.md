# detection-bias
Scripts to quantify the galaxy detection bias in cosmic shear measurements

# Detection Bias in Cosmic Shear Measurements

This repository contains scripts developed during my Master's thesis to quantify and correct detection biases in galaxy shape measurements for cosmic shear analyses. It includes tools for realistic galaxy simulation, injection into survey tiles, catalog comparison after detection, and computation of detection probabilities as weights for shear correlation functions.

The methods implemented are described in my paper: [arXiv:2507.01546](https://arxiv.org/pdf/2507.01546)

---

## 📁 Project Structure

```
detection-bias/
├── KiDSGalaxyInjector.py # Simulate and inject galaxies into survey tiles
├── CatalogComparator.py # Compare injected vs detected catalogs
├── GalaxyWeightAssigner.py # Assign weights based on detection probabilities
├── requirements.txt # Python dependencies
└── README.md
```



---

## Main Components

### 1. `KiDSGalaxyInjector.py`
- Generates realistic galaxy images using **GalSim** with KiDS-like parameters.  
- Injects galaxies into survey tiles for testing detection completeness.  
- Supports adjustable parameters for flux, size, and position distributions.

### 2. `CatalogComparator.py`
- Compares **injected catalogs** with **SExtractor-detected catalogs**.  
- Computes **detection efficiency** as a function of galaxy properties (flux, size, etc.).  
- Outputs detection probability tables for further analysis.

### 3. `GalaxyWeightAssigner.py`
- Uses the **precomputed detection probability function**.  
- Assigns **weights to galaxies** to correct for detection bias in shear correlation measurements.  
- Can be integrated directly into standard cosmic shear pipelines.

---

## Requirements

Install Python dependencies via:

```bash
pip install -r requirements.txt
```
