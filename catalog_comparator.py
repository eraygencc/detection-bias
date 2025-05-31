import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.coordinates import match_coordinates_sky, SkyCoord
import astropy.units as u


class CatalogComparator:
    def __init__(self, injected_catalog_path, detected_catalog_path, separation_arcsec=1.0):
        self.injected_catalog_path = injected_catalog_path
        self.detected_catalog_path = detected_catalog_path
        self.separation_arcsec = separation_arcsec

    def load_catalogs(self):
        self.injected_df = pd.read_csv(self.injected_catalog_path)
        self.detected_df = pd.read_csv(self.detected_catalog_path)
        print(f"Loaded {len(self.injected_df)} injected and {len(self.detected_df)} detected sources.")

    def match_catalogs(self):
        injected_coords = SkyCoord(ra=self.injected_df['RA']*u.deg, dec=self.injected_df['DEC']*u.deg)
        detected_coords = SkyCoord(ra=self.detected_df['RA']*u.deg, dec=self.detected_df['DEC']*u.deg)

        idx, sep2d, _ = injected_coords.match_to_catalog_sky(detected_coords)

        self.injected_df['matched_sep'] = sep2d.arcsec
        self.injected_df['matched'] = sep2d.arcsec < self.separation_arcsec

        self.matched_df = self.injected_df[self.injected_df['matched']].copy()
        self.unmatched_df = self.injected_df[~self.injected_df['matched']].copy()

        print(f"Matched {len(self.matched_df)} sources. Unmatched: {len(self.unmatched_df)}.")

    def save_results(self, matched_path="matched.csv", unmatched_path="unmatched.csv"):
        self.matched_df.to_csv(matched_path, index=False)
        self.unmatched_df.to_csv(unmatched_path, index=False)
        print(f"Saved matched sources to {matched_path} and unmatched to {unmatched_path}.")


# Example usage:
# comparator = CatalogComparator("injected_sources.csv", "detected_sources.csv")
# comparator.load_catalogs()
# comparator.match_catalogs()
# comparator.save_results()
