import ray
from ray.job_submission import JobSubmissionClient
import piexif
import random
import ipyplot
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

# Ray initialization
import ray
from ray.job_submission import JobSubmissionClient
import time
from ray.runtime_env import RuntimeEnv

# Ray cluster information
ray_head_ip = "kuberay-head-svc.kuberay.svc.cluster.local"
ray_head_port = 8265
ray_address = f"http://{ray_head_ip}:{ray_head_port}"

class ImageResolver(StandardResolver):
    def resolve(self, name: str, why_type: DataType, column_schema: ColumnSchema) -> Dict[str, Metric]:
        print(name)
        print(why_type)
        print(column_schema)

        if "image" in name:
            return {ImageMetric.get_namespace(): ImageMetric.zero(column_schema.cfg)}
        return super(ImageResolver, self).resolve(name, why_type, column_schema)

class RayWhylogsImgBinProfileExpActor:
    def __init__(self):
        self.img1 = Image.effect_mandelbrot((256, 256), (-3, -2.5, 2, 2.5), 9)
        self.img2 = Image.effect_mandelbrot((256, 256), (-3, -2.5, 2, 2.5), 20)
        self._result = {}
        self._fractal_images = []
        self._cnt = 100

    def generate_mandelbrot(self, width, height, x_min, y_min, x_max, y_max, iterations):
        try:
            for item in range(0, self._cnt):
                self._fractal_images.append(Image.effect_mandelbrot((width, height), 
                                                                    (-int(random.randint(1.0,5.0)), 
                                                                     -int(random.randint(1.0,5.0)), 
                                                                     random.randint(1.0,5.0), 
                                                                     random.randint(1.0,5.0)), iterations))
            return self._fractal_images
        except Exception as error:
            print(traceback.format_exc())

    def get_binary_data(self):
        try:
            # Displaying images directly within a remote function is not recommended
            return self.img1, self.img2
        except Exception as error:
            print("Exception: get_binary_data", traceback.format_exc())

    def get_logged_column_dtls(self, lstmandelbrot: list):
        print("=*="*50)

        self._result = log_image(list(lstmandelbrot))
        schema = DatasetSchema(resolvers=ImageResolver(), default_configs=ImageMetricConfig())
        stats = Stat(lstmandelbrot[99])
        df = pd.DataFrame({"median": stats.median, "sum": stats.sum, "images": lstmandelbrot[99]})
        results = why.log(df, schema=schema).view()

        print("whyloged image columns::", results.get_column("median").to_summary_dict())
        print("whyloged image columns::", results.get_column("sum").to_summary_dict())
        print("whyloged image columns::", results.get_column("images").to_summary_dict())

        print("=*="*50)

        return self._result

    def get_images(self):
        return self.img1, self.img2

def main_exp():
    try:
        # Create a RayWhylogsImgBinProfileExpActor instance
        objraywhylogsprf = RayWhylogsImgBinProfileExpActor()

        # Generate Mandelbrot images
        lstmandelbrot = objraywhylogsprf.generate_mandelbrot(256, 256, -2.0, -1.5, 1.0, 1.5, 100)
        print("generated no.of images: =========", len(lstmandelbrot))
        ipyplot.plot_images(lstmandelbrot, max_images=100, img_width=75)

        # Start Ray job submission
        with JobSubmissionClient(ray_address) as client:
            # Submit the RayWhylogsImgBinProfileExpActor job
            actor_handle = client.submit_actor(RayWhylogsImgBinProfileExpActor)
            actor = actor_handle.fetch()
            
            # Generate Mandelbrot images within the RayWhylogsImgBinProfileExpActor
            actor.generate_mandelbrot(256, 256, -2.0, -1.5, 1.0, 1.5, 100)
            
            # Get images from the actor
            img1, img2 = actor.get_images()
            # Displaying images directly within a remote function is not recommended
            # Display img1, img2 as needed

            # Log image data
            actor.get_logged_column_dtls(lstmandelbrot)

    except Exception as error:
        print(traceback.format_exc())

if __name__ == "__main__":
    main_exp()
