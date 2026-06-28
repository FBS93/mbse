# Activity Render

This package renders validated `ActivityModel` documents to SVG and exposes stable lookup helpers for viewer highlighting.

`ActivityRender` owns only render concerns:

- prepare Activity elements as DOT nodes and edges.
- render DOT to SVG through Graphviz.
- normalize SVG text fragments into stable text ids.
- expose structural ids for actions, decisions, finals, and transitions.

Runtime execution and server session state remain outside this layer.
