# RemNote Local Server

A small architecture demo about how to interact with the system from a local knowledge base.

- Sync (read/write) rem
- Send page for statistical evaluation
- Run python code
- Generate Plots

## Architecture

- An API server on port 8000 to listen commands from the plugin
- A HTTP server on port 8080 (just a live-server) to serve content like

  - the plugin page
  - images/plots from disk
  - a live updating stats page

- Note: You can also make a live updating dashboard/stat page/graph view by opening a websocket to the API server, but just live reloading the some generated HTML is easier for this simple demo.
- Note: Similarly the API server process can serve the content, but again, `live-server .` good for prototyping.
- Note: There is almost no error checking. I just assume that the correct data is provided. For a proper plugin this is obviously required.

For this simple demo I just `eval` some python code. Of course you can also interact with a jupyter kernel for example. See e.g. https://stackoverflow.com/questions/54475896/interact-with-jupyter-notebooks-via-api

## Usage

- Install dependencies (you might want a virtualenv) and start the servers:

```sh
# API server
pip install fastapi uvicorn[standard]
pip install numpy plotly kaleido  # plotting dependencies
uvicorn api:app --reload

# Live-reload server
npm install live-server
live-server .
```

- Add plugin to remnote with url: `http://localhost:8080/plugin.html`. It works best as a popup with a shortcut assigned.

  - Note: You can also assign a single command to a shortcut to trigger without clicking a button and close the popup right after executing. Or implement an omnibar or something.

- Open the live-reloading [stats page/dashboard/local view](http://localhost:8080/stats.html) in a browser.
