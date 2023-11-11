from htmltools import Tag
import matplotlib.pyplot as plt
import pandas as pd
from shiny import App, render, ui

demo_df: pd.DataFrame = pd.read_csv('../out/cpool.out', delim_whitespace=True)

app_ui: Tag = ui.page_fluid(
    ui.panel_title("Demo plot"),
    ui.output_plot("demo_plot"),
)


def server(input, output, session):
    @output
    @render.plot
    def demo_plot():
        fig, ax = plt.subplots()
        ax.stackplot(demo_df['Year'].values - 499, demo_df.drop(['Year', 'Lon', 'Lat', 'Total'] ,axis=1).T,
                    labels=['VegC', 'LitterC', 'SoilC'], alpha=0.8)
        ax.legend(loc='upper left', reverse=True)
        ax.set_title('Carbon Pool')
        ax.set_xlabel('Year')
        ax.set_ylabel('kg/m^2')
        return fig


app = App(app_ui, server)
