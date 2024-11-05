import piexif
import random
import ray
import ipyplot
import ray.data as df
from PIL import Image
import pandas as pd
import traceback
from typing import Dict
from PIL.ImageStat import Stat
import matplotlib.pyplot as plt
import whylogs as why
from whylogs.extras.image_metric import log_image
from whylogs.core.datatypes import DataType
from whylogs.core.metrics import Metric
from whylogs.core.resolvers import StandardResolver
from whylogs.core.schema import DatasetSchema, ColumnSchema
from whylogs.extras.image_metric import ImageMetric, ImageMetricConfig

class ImageResolver(StandardResolver):
    def resolve(self, name: str, why_type: DataType, column_schema: ColumnSchema) -> Dict[str, Metric]:
        if "image" in name:
            return {ImageMetric.get_namespace(): ImageMetric.zero(column_schema.cfg)}
        return super().resolve(name, why_type, column_schema)

class RayWhylogsImgBinProfileExpActor():

    def __init__(self):
        self.img1 = Image.effect_mandelbrot((256, 256), (-3, -2.5, 2, 2.5), 9)
        self.img2 = Image.effect_mandelbrot((256, 256), (-3, -2.5, 2, 2.5), 20)
        self._result = {}
        self._fractal_images = []
        self._cnt = 100

    def generate_mandelbrot(self, width, height, x_min, y_min, x_max, y_max, iterations):
        try:
            for _ in range(self._cnt):
                img = Image.effect_mandelbrot(
                    (width, height),
                    (-random.randint(1, 5), -random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)),
                    iterations
                )
                if img is not None:  # Check if img is valid
                    self._fractal_images.append(img)
            return self._fractal_images
        except Exception as error:
            print(traceback.format_exc())

    def get_binary_data(self):
        try:
            display(self.img1)
            display(self.img2)
            results = log_image(self.img1)
            print("Results Summary:", results.view().get_column("image").to_summary_dict())
            return self.img1, self.img2
        except Exception as error:
            print("Exception in get_binary_data:", traceback.format_exc())

    def get_logged_column_dtls(self, lstmandelbrot: list):
        try:
            if len(lstmandelbrot) == 0:
                print("No images to log.")
                return None
            elif len(lstmandelbrot) <= 99:
                print("Not enough images to access the 100th image.")
                return None

            self._result = log_image(list(lstmandelbrot))
            schema = DatasetSchema(resolvers=ImageResolver(), default_configs=ImageMetricConfig())
            stats = Stat(lstmandelbrot[99])
            df = pd.DataFrame({"median": stats.median, "sum": stats.sum, "images": lstmandelbrot[99]})
            results = why.log(df, schema=schema).view()

            print("Logged image columns summary:", results.get_column("median").to_summary_dict())
            print("Logged image columns sum:", results.get_column("sum").to_summary_dict())
            print("Logged image columns images:", results.get_column("images").to_summary_dict())

            return self._result
        except Exception as error:
            print("Exception in get_logged_column_dtls:", traceback.format_exc())

def main_exp():
    try:
        objraywhylogsprf = RayWhylogsImgBinProfileExpActor()
        lstmandelbrot = objraywhylogsprf.generate_mandelbrot(256, 256, -2.0, -1.5, 1.0, 1.5, 100)
        print("Generated number of images:", len(lstmandelbrot))

        objraywhylogsprf.get_logged_column_dtls(lstmandelbrot)
        return lstmandelbrot

    except Exception as error:
        print("Exception in main_exp:", traceback.format_exc())

if __name__ == "__main__":
    main_exp()
