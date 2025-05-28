from datetime import datetime as dt
from  matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

SAMPLES = -60

class GraphGenerator():
    def __init__(self, json_loader, logger):
        self.json_loader = json_loader
        self.times, self.prices = self.list_json_data()
        self.logger = logger


    def list_json_data(self) -> list[str]:
        """
        Method parses dictionarry components 
        Returns two lists - one for the json keys, the other for the values
        """
        json_data = self.json_loader.json_data
        times = list(json_data.keys())[SAMPLES:]
        prices = list(json_data.values())[SAMPLES:]
        return times, prices


    @staticmethod
    def time_format(time:str, separator:str) -> str:
        """
        Recives a time string in format 'HH:MM:SS' and separetor ('-' or ':')
        Returns the time separated according to the 'separetor' ('HH:MM' or 'HH-MM')
        """
        time_object = dt.strptime(time, "%H:%M:%S")
        return time_object.strftime(f'%H{separator}%M')


    def create_image_name(self) -> str:
        """
        Method creates detailed image name
        Returns a fuul name that contains - current date, first and last hour of the graph
        """
        first_time = self.time_format(self.times[0], "-")
        last_time = self.time_format(self.times[-1], "-")
        today = dt.now().strftime('%Y-%m-%d')
        folder = "graph_images"
        new_name = f"bitcoin_graph_{today}_from_{first_time}_to_{last_time}.png"
        file_name = os.path.join(folder, new_name)
        return str(file_name)
    

    def generate_graph(self) -> None:
        """ 
        Method creates and styles a graph,
        then saves it as an image.
        """
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
        file_name = self.create_image_name()
        plt.savefig(file_name)
        plt.close()
        self.logger.info(f"A new graph image named '{file_name}' was created")