# detection-bias
Scripts to quantify the galaxy detection bias in cosmic shear measurements

# Detection Bias in Cosmic Shear Measurements

This repository contains scripts to quantify and correct detection biases of galaxies for cosmic shear analyses. It includes tools for realistic galaxy simulation, injection into survey tiles, catalog comparison after detection, and computation of detection probabilities as weights for shear correlation functions.

The methods implemented are described in this paper: [arXiv:2507.01546](https://arxiv.org/pdf/2507.01546)

---

## 📁 Project Structure

```
detection-bias/
├── galaxy_injector.py # Simulate and inject galaxies into survey tiles
├── catalog_comparator.py # Compare injected vs detected catalogs
├── GalaxyWeightAssigner.py # Assign weights based on detection probabilities
├── requirements.txt # Python dependencies
└── README.md
```



---

## Main Components

### 1. `galaxy_injector.py`
- Generates realistic galaxy images using **GalSim** with KiDS-like parameters.  
- Injects galaxies into survey tiles for testing detection completeness.  
- Supports adjustable parameters for flux, size, and position distributions.

### 2. `catalog_comparator.py`
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

## Usage

1. **Simulate and inject galaxies**

```bash
python galaxy_injector.py --config configs/injection_config.yaml
```
2. **Compare catalogs**
 ```  python catalog_comparator.py --injected injected_catalog.fits --detected detected_catalog.fits ```

3. **Assign weights to the galaxies**
 
The `GalaxyWeightAssigner.py` script uses the **detection bias model** described in the paper to assign weights to galaxies.  
The model computes the **detection probability** of a galaxy based on two key quantities:

- The **projected separation** $r$ between a galaxy and its **nearest neighbor** (primary galaxy).  
- The **magnitude difference** $\Delta m$ between the two galaxies.

The detection probability $p_\mathrm{det}$ is modeled as:

$$
f(\Delta m, \theta) = 0.5 + \frac{1}{\pi}\, \mathrm{arctan}\left(\frac{b\,\theta - \Delta m}{\delta}\right) ,
$$

where $a, b, c, d$ are parameters calibrated from injected galaxies and catalog comparisons (see Section 3 of [arXiv:2507.01546](https://arxiv.org/pdf/2507.01546)).

Once the detection probability is computed for each galaxy, it can directly be used as weights during the calculation of (shear) correlation functions.

This weight corrects for the **selection bias** introduced by galaxy detection inefficiency in crowded fields.

```bash
python GalaxyWeightAssigner.py --catalog detected_catalog.fits --weights detection_probs.npy
```

Note 1: This calculation requires precomputed detection probability function from the CatalogComparator.py output and is intended for HPC environments due to the large number of galaxy pairs.
Note 2: Scripts are designed for high-performance computing environments due to large data volumes.


