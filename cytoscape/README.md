# Cytoscape
[Cytoscape](http://www.cytoscape.org) is an open source software platform for visualizing molecular 
interaction networks and biological pathways and integrating these 
networks with annotations, gene expression profiles and other state data. 

Here, Cytoscape was used to visualize OpenTrials grahps of the form
`trial <-> interaction <-> condition`
for given queries.

`*.cys` files are Cytoscape session files which can be loaded directly
in Cytoscape. To use them download [Cytoscape](http://www.cytoscape.org)
 and `File -> Open`.
 
To visualize an OpenTrials query import the corresponding`*,gml` file
from the `opentrials/result` folder via `File -> Import -> Network -> File`.

`OpenTrials.xml` is the Cytoscape Style file for the OpenTrial graphs.
To use the visualize style, import it via `File -> Import -> Styles`
and select it in the visual mapping.