from flask import Flask, request, render_template
import plotly.express as px
import plotly.io as pio
import anndata
from os.path import join
import matplotlib.pyplot as plt
import scanpy as sc
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/string_length', methods=['GET'])


@app.route('/string_length', methods=['GET'])
def string_length():
    input_string = request.args.get('input', '')
    length = len(input_string)

    # Create a simple Plotly graph
    fig = px.scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], title="Sample Plot")
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('result.html', length=length, graph_html=graph_html)

@app.route('/show_data', methods=['GET'])
def show_data():
    gene = request.args.get('input', '')
    # gene = "Oxtr"
    # Create a simple Plotly graph
    adata = anndata.read_h5ad(join("..", "rudolf-sca", "scripts", "dev_counts_no_aggressive.h5ad"))
    fig = plt.figure()
    ax = plt.gca()
    sc.pl.umap(adata, ax=ax ,color=[gene], use_raw=False)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the plot in base64 to embed in HTML
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('sca_plot.html', plot_url=plot_url)


if __name__ == '__main__':
    app.run(debug=True)