from datetime import datetime as dt
from  matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

class GraphGenerator():
    def __init__(self, logger):
        super().__init__()
        # json data ?
        self.times, self.prices = self.list_json_data

        self.logger = logger


    def list_json_data(json_data):
        times = list(json_data.keys())[-60:]
        prices = list(json_data.values())[-60:]
        return times, prices


    def time_format(time, separator=":"):
        """ Recieves time string in format 'HH:MM:SS' and returns hour/minute separated by format 'HH?MM' """ 
        time_object = dt.strptime(time, "%H:%M:%S")
        return time_object.strftime(f'%H{separator}%M')


    def create_image_metadata(self):
        first_time = self.time_format(self.times[0], "-")
        last_time = self.time_format(self.times[-1], "-")
        today = dt.now().strftime('%Y-%m-%d')
        folder = "graph_images"
        new_name = f"bitcoin_graph_{today}_from_{first_time}_to_{last_time}.png"
        file_name = os.path.join(folder, new_name)
        return file_name
    

    def generate_graph(self):
        # modify plot
        plt.figure(figsize=(16, 6))
        formatted_times = [self.time_format(t, ":") for t in self.times]
        plt.plot(formatted_times, self.prices, marker="o")
        plt.xlim(-0.5, len(formatted_times) - 0.5)
        plt.grid(axis='x', linestyle='--', color='gray', alpha=0.3)
        # title
        plt.title("Bitcoin Price Index for the Previous Hour")
        plt.xlabel("Time")
        plt.ylabel("Price (USD)")
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        # save and close
        plt.savefig(self.create_image_metadata)
        plt.close()
        self.logger.info("A new graph image was genarated")