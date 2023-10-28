import plotly.express as px
import plotly.io as pio


CONFIG = {
    "Scatter": px.scatter, 
    "Scatter 3d": px.scatter_3d, 
    "Bar": px.bar, 
    "Funnel": px.funnel, 
    "Histogram": px.histogram, 
    "Violin": px.violin,
    "Line": px.line, 
    "Area": px.area, 
}

def create_plot(chart, **kwargs):
    fn = CONFIG[chart]
    fig = fn(**kwargs)
    return fig

def create_plot_html(chart, **kwargs):
    fig = create_plot(chart, **kwargs)
    html = pio.to_html(fig)
    return html

def create_all(inputs):
    html = ""
    for input in inputs:
        fig = create_plot(**input)
        html += pio.to_html(fig, full_html=False)

    return html