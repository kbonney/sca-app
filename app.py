from flask import Flask, request, render_template
import plotly.express as px
import plotly.io as pio
import anndata
from os.path import join
import matplotlib.pyplot as plt
import scanpy as sc
import io
import base64
import mpld3

app = Flask(__name__)

with app.app_context():
    datapath = join("..", "rudolf-sca", "scripts", "dev_counts_no_aggressive.h5ad")
    app.config['adata'] = anndata.read_h5ad(datapath, backed="r")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/string_length', methods=['GET'])
def string_length():
    input_string = request.args.get('input', '')
    length = len(input_string)

    # Create a simple Plotly graph
    fig = px.scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], title="Sample Plot")
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('result.html', length=length, graph_html=graph_html)

@app.route('/show_data', methods=['POST'])
def show_data():
    gene = request.form['gene']
    # enforce gene name formatting
    gene = gene.title()
    # fetch data from context
    adata = app.config['adata']
    # Create a simple Plotly graph
    fig = plt.figure(figsize=(10,10))
    ax = plt.gca()
    sc.pl.umap(adata, ax=ax ,color=[gene], use_raw=False)
    # img = io.BytesIO()
    # plt.savefig(img, format='png')
    # img.seek(0)

    # # Encode the plot in base64 to embed in HTML
    # plot_url = base64.b64encode(img.getvalue()).decode()
    mpld3_html = mpld3.fig_to_html(fig)
    return render_template('mpld3_plot.html', mpld3_html=mpld3_html)
    # return render_template('sca_plot.html', plot_url=plot_url)

@app.route('/interactive_plot')
def interactive_plot():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 11, 12, 13])
    mpld3_html = mpld3.fig_to_html(fig)
    return render_template('mpld3_plot.html', mpld3_html=mpld3_html)


if __name__ == '__main__':
    app.run(debug=True)