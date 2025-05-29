from datetime import datetime as dt
from  matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from src.constants import SAMPLES_COUNT
import os


class BitcoinGraphGenerator():
    def __init__(self, json_loader, logger):
        self.json_loader = json_loader
        self.times, self.prices = self._list_json_data()
        self.logger = logger


    def _list_json_data(self) -> tuple[list[str], list[float]]:
        """
        Helper method parses dictionary components 
        Returns two lists - one for the json keys, the other for the values
        """
        try:
            json_data = self.json_loader.json_data
            if not json_data:
                self.logger.warning("No JSON data available")
                return [], []
            
            times = list(json_data.keys())[-SAMPLES_COUNT:]
            prices = list(json_data.values())[-SAMPLES_COUNT:]
            
            if len(times) == 0:
                self.logger.warning("No data points after filtering")
                return [], []
                
            return times, prices
        except (AttributeError, TypeError) as e:
            self.logger.error(f"Error parsing JSON data: {e}")
            return [], []


    @staticmethod
    def time_format(time:str, separator:str) -> str:
        """
        Recives a time string in format 'HH:MM:SS' and separetor ('-' or ':')
        Returns the time separated according to the 'separetor' ('HH:MM' or 'HH-MM')
        """
        time_object = dt.strptime(time, "%H:%M:%S")
        return time_object.strftime(f'%H{separator}%M')


    def _create_image_name(self) -> str:
        """
        Helper method creates detailed image name
        Returns a full name that contains - current date, first and last hour of the graph
        """
        first_time = self.time_format(self.times[0], "-")
        last_time = self.time_format(self.times[-1], "-")
        today = dt.now().strftime('%Y-%m-%d')
        folder = "graph_images"
        new_name = f"bitcoin_graph_{today}_from_{first_time}_to_{last_time}.png"
        file_name = os.path.join(folder, new_name)
        return file_name
    

    def generate_graph(self) -> None:
        """ 
        Method creates and styles a graph,
        then saves it as an image.
        """
        if not self.times or not self.prices:
            self.logger.error("No data available to generate graph")
            return
        
        if len(self.times) != len(self.prices):
            self.logger.error("Times and prices lists have different lengths")
            return
        try:
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
            file_name = self._create_image_name()
            plt.savefig(file_name)
            plt.close()
            self.logger.info(f"Graph image saved as '{file_name}'")
        except Exception as e:
            self.logger.error(f"Failed to generate graph: {e}")
            plt.close()  # Always close the figure
            raise