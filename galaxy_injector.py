import galsim
import numpy as np
import os
from astropy.io import fits
from astropy.table import Table

class GalaxyInjector:
    def __init__(self, tile_image_path, output_dir, catalog_path=None):
        self.tile_image_path = tile_image_path
        self.output_dir = output_dir
        self.catalog_path = catalog_path
        self.injected_catalog = None
        self.tile_image = None

    def load_tile_image(self):
        self.tile_image = fits.open(self.tile_image_path)
        print(f"Tile image loaded: {self.tile_image_path}")

    def load_catalog(self):
        if self.catalog_path:
            self.injected_catalog = Table.read(self.catalog_path)
            print(f"Catalog loaded with {len(self.injected_catalog)} entries.")
        else:
            raise ValueError("No catalog path provided.")

    def simulate_galaxy(self, mag, half_light_radius, flux_factor=1.0):
        flux = galsim.utilities.magnitude2flux(mag) * flux_factor
        gal = galsim.Exponential(half_light_radius=half_light_radius)
        gal = gal.withFlux(flux)
        return gal

    def inject_galaxies(self, psf_fwhm=0.7, pixel_scale=0.2):
        if self.tile_image is None or self.injected_catalog is None:
            raise RuntimeError("Tile image or catalog not loaded.")

        image_hdu = self.tile_image[0]
        image_data = image_hdu.data.copy()
        psf = galsim.Gaussian(fwhm=psf_fwhm)

        for obj in self.injected_catalog:
            x, y = obj['x'], obj['y']
            mag = obj['mag']
            hlr = obj.get('hlr', 0.5)  # Use default if not provided

            gal = self.simulate_galaxy(mag, hlr)
            final = galsim.Convolve([gal, psf])
            stamp = final.drawImage(scale=pixel_scale)

            ix, iy = int(x), int(y)
            try:
                image_data[iy:iy+stamp.array.shape[0], ix:ix+stamp.array.shape[1]] += stamp.array
            except ValueError:
                print(f"Skipped galaxy at ({x:.1f}, {y:.1f}) - out of bounds")

        hdu = fits.PrimaryHDU(data=image_data, header=image_hdu.header)
        output_path = os.path.join(self.output_dir, "injected_tile.fits")
        hdu.writeto(output_path, overwrite=True)
        print(f"Injected image saved to {output_path}")
