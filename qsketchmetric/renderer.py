import math
import string
from copy import deepcopy
from pathlib import Path
from random import choice
from typing import Optional, Dict

import ezdxf
from ezdxf import units, bbox
from ezdxf.entities import DXFGraphic
from ezdxf.layouts import Modelspace
from ezdxf.math import Vec3
from py_expression_eval import Parser  # type: ignore
from ezdxf.document import Drawing


class Renderer:
    """
    The :class:`Renderer` class interprets parametric DXF files, transforming them into visual representations.

    :param input_parametric_path: Path to the parametric file intended for rendering.
    :param output_rendered_object: A pre-initialized :class:`ezdxf.document.Drawing` drawing object.
        You can initialize such an object using methods like :meth:`ezdxf.readfile` or :meth:`ezdxf.new`
        By providing an already existing drawing, users can merge multiple visual elements into a singular
        representation.
    :param variables: **(Optional)** Supplementary constant variables that can enhance the mathematical
        representations used.Defaults to an empty dictionary.
    :param offset: **(Optional)** Provides offsets for the parametric visualization. Defaults to (0, 0).

    .. seealso::
          `ezdxf Documentation <https://ezdxf.readthedocs.io/en/stable/>`_ - A comprehensive library to manage
          DXF drawings, allowing users to read, write, and modify DXF content efficiently.
    """

    def __init__(self, input_parametric_path: Path, output_rendered_object: Drawing,
                 variables: Optional[dict[str, float]] = None, offset: tuple[int, int] = (0, 0)):
        """
            Instantiate a new :class:``Renderer`` object.
        """

        if variables is None:
            variables = dict()

        self.new_points: Dict[Vec3, tuple[int, int]] = {}
        self.input_parametric_path: Path = input_parametric_path

        self.input_dxf: Drawing = ezdxf.readfile(self.input_parametric_path)
        self.input_msp: Modelspace = self.input_dxf.modelspace()

        self.output_dxf: Drawing = output_rendered_object
        self.output_msp: Modelspace = self.output_dxf.modelspace()

        self.offset_drawing_x: float = offset_drawing[0]
        self.offset_drawing_y: float = offset_drawing[1]

        self.variables: Dict[str, float] = {} | extra_variables

        self.graph: Dict[Vec3, list[tuple[str, Vec3, float, dict]]] = {}
        self.visited_graph: Dict[Vec3, list[tuple[str, Vec3]]] = {}
        self.points: Dict[str, Vec3] = {}
        self.new_entities: list[DXFGraphic] = []

    def render(self) -> dict[str, tuple[float, float]]:
        """
           Transforms the input parametric DXF drawing and produces a rendered output on the output DXF.

           :return: A dictionary containing rendered points marked in the parametric drawing.
        """

        self.input_dxf.units = units.MM
        extracted_texts: filter = filter(None, self.input_dxf.query("MTEXT")[0].text.split(
            "----- custom -----")[-1].split("\P"))

        extracted_variables: Dict[str, float] = {
            v.split(":")[0].strip(): float(Parser().parse(v.split(":")[1].strip()).evaluate(self.variables)) for v in
            extracted_texts}

        self.variables |= extracted_variables

        self._prepare_graph()

        root = min(self.graph.keys())
        self.new_points = {root: (root.x, root.y)}

        self._dfs(root, 0, 0)
        self._construct_rest_of_dxf()
        self._center_drawing()

        return self.points

    def get_bb_dimensions(self) -> tuple[float, float]:
        """
            Retrieve the bounding box dimensions of the output DXF.

            This method determines the bounding box of the output DXF by calculating the width and height
            of the rectangle that encompasses all entities within the DXF file.

            :return: A tuple containing the width and height of the bounding box.
            """

        bounding_box = bbox.extents(self.output_msp, cache=bbox.Cache())

        return (bounding_box.rect_vertices()[2].x - bounding_box.rect_vertices()[0].x,
                bounding_box.rect_vertices()[2].y - bounding_box.rect_vertices()[0].y)

    def _prepare_graph(self):
        """
            .. note:: This method is private and not intended for external use.

            Prepares a graph representation of the entities.

            This method processes entities to construct the graph. Supported entities include:

            - **LINE**: Determines start and end points, assesses line types, and updates the graph.
            - **CIRCLE**: Evaluates the center point and updates the graph.
            - **ARC**: Evaluates the center point, accounting for start and end angles, and updates the graph.
            - **POINT**: Evaluates the location point and updates the graph.

            :note: Entities of type "MTEXT" are filtered out during processing.
        """
        input_layers = dict()

        for entity in filter(lambda x: x.dxftype() != "MTEXT", self.input_msp.entity_space.entities):
            new_length = "?"

            xdata = dict(map(lambda x: (x[1].split(":")), entity.get_xdata("QCAD")))

            constant_xdata = xdata.get("c", False)
            line_xdata = xdata.get("line", False)
            line_type = "BYLAYER"
            layer = entity.dxf.layer

            input_layers[layer] = self.input_dxf.layers.get(entity.dxf.layer).color

            if line_xdata:
                line, space = list(map(float, str(line_xdata).split()))
                line_type = f"{line}_{space}_" + ''.join(choice(string.ascii_lowercase) for _ in range(8))

                self.output_dxf.linetypes.add(name=line_type, pattern=[line + space, line, -space],
                                              description="- - - - - -", )

            if entity.dxftype() == "LINE":

                start = entity.dxf.start
                end = entity.dxf.end

                start = Vec3(round(start.x, 3), round(start.y, 3), 0)
                end = Vec3(round(end.x, 3), round(end.y, 3), 0)

                self.variables["c"] = math.dist(start, end)

                if constant_xdata == "?":
                    pass
                else:
                    new_length = Parser().parse(constant_xdata).evaluate(self.variables)

                e_data = {"layer": layer, "linetype": line_type}

                self.graph[end] = self.graph.get(end, []) + [("LINE", start, new_length, e_data)]
                self.graph[start] = self.graph.get(start, []) + [("LINE", end, new_length, e_data)]
                self.visited_graph[end] = self.visited_graph.get(end, []) + [(e_data["layer"], start)]
                self.visited_graph[start] = self.visited_graph.get(start, []) + [(e_data["layer"], end)]

            elif entity.dxftype() == "CIRCLE":
                center = entity.dxf.center
                center = Vec3(round(center.x, 3), round(center.y, 3), 0)
                self.variables["c"] = entity.dxf.radius

                new_length = Parser().parse(constant_xdata).evaluate(self.variables)

                e_data = {"layer": layer, "radius": entity.dxf.radius, "linetype": line_type}

                self.graph[center] = self.graph.get(center, []) + [("CIRCLE", center, new_length, e_data)]

            elif entity.dxftype() == "ARC":
                center = entity.dxf.center
                center = Vec3(round(center.x, 3), round(center.y, 3), 0)
                self.variables["c"] = entity.dxf.radius

                new_length = Parser().parse(constant_xdata).evaluate(self.variables)

                e_data = {"layer": layer, "radius": entity.dxf.radius, "start_angle": entity.dxf.start_angle,
                          "end_angle": entity.dxf.end_angle, "linetype": line_type}

                self.graph[center] = self.graph.get(center, []) + [("ARC", center, new_length, e_data)]

            elif entity.dxftype() == "POINT" and layer == "VIRTUAL_LAYER":
                location = entity.dxf.location
                location = Vec3(round(location.x, 3), round(location.y, 3), 0)

                e_data = {"name": list(xdata.values())[0]}

                self.graph[location] = self.graph.get(location, []) + [("POINT", location, 0, e_data)]

        self._prepare_layers(input_layers)

    def _prepare_layers(self, input_layers: dict[str, int]):
        output_layers = [layer.dxf.name for layer in self.output_dxf.layers]

        for layer, color in input_layers.items():
            if layer not in output_layers and layer != "VIRTUAL_LAYER":
                self.output_dxf.layers.new(name=layer, dxfattribs={'color': color})

    def _construct_rest_of_dxf(self):
        """
        .. note:: This method is private and not intended for external use.

        Construct the DXF file's additional components.

        This method iterates through the graph data. Identifies lines that were marked with '?' as their length,
        and constructs them based on the already processed entities.
        """

        for node, v in self.graph.items():
            for line in [l for l in v if
                         l[0] == "LINE" and l[2] == "?" and (l[3]["layer"], l[1]) in self.visited_graph[node]]:
                self.new_entities.append(self.output_msp.add_line((
                    self.new_points[node][0] + self.offset_drawing_x, self.new_points[node][1] + self.offset_drawing_y),
                    (self.new_points[line[1]][0] + self.offset_drawing_x,
                     self.new_points[line[1]][1] + self.offset_drawing_y),
                    dxfattribs={"layer": line[3]["layer"], "linetype": line[3]["linetype"]}))
                self.visited_graph[line[1]].remove((line[3]["layer"], node))
                self.visited_graph[node].remove((line[3]["layer"], line[1]))

    def _dfs(self, node: Vec3, offset_x: float, offset_y: float):
        """
            .. note:: This method is private and not intended for external use.

            Executes a DFS traversal starting from the provided node and adds geometric entities to the output DXF.

            This method traverses the graph representation of the DXF to generate new entities
            based on the given node and offsets.

            :param node: Starting node for DFS traversal. It updates automatically as the traversal progresses.
            :param offset_x: X-coordinate offset for current node and its connected entities.
            :param offset_y: Y-coordinate offset for current node and its connected entities.
        """

        for name, vector, length, data in [c for c in self.graph[node] if c[2] != "?"]:

            if name == "CIRCLE":
                self.new_entities.append(self.output_msp.add_circle(
                    (node.x + offset_x + self.offset_drawing_x, node.y + offset_y + self.offset_drawing_y), length,
                    dxfattribs={"layer": data["layer"], "linetype": data["linetype"]}))

            elif name == "ARC":
                self.new_entities.append(self.output_msp.add_arc(
                    (node.x + offset_x + self.offset_drawing_x, node.y + offset_y + self.offset_drawing_y), length,
                    data["start_angle"], data["end_angle"],
                    dxfattribs={"layer": data["layer"], "linetype": data["linetype"]}))

            elif name == "LINE":
                if (data["layer"], vector) in self.visited_graph[node]:
                    factor = length / math.dist(vector, node)

                    new_offset_x = (vector.x - node.x) * factor - (vector.x - node.x)
                    new_offset_y = (vector.y - node.y) * factor - (vector.y - node.y)

                    self.new_points[vector] = (vector.x + offset_x + new_offset_x, vector.y + offset_y + new_offset_y)

                    if data["layer"] != "VIRTUAL_LAYER":
                        self.new_entities.append(self.output_msp.add_line(
                            (node.x + offset_x + self.offset_drawing_x, node.y + offset_y + self.offset_drawing_y), (
                                vector.x + offset_x + new_offset_x + self.offset_drawing_x,
                                vector.y + offset_y + new_offset_y + self.offset_drawing_y),
                            dxfattribs={"layer": data["layer"], "linetype": data["linetype"]}))

                    self.visited_graph[node].remove((data["layer"], vector))
                    self.visited_graph[vector].remove((data["layer"], node))

                    self._dfs(vector, offset_x + new_offset_x, offset_y + new_offset_y)

            elif name == "POINT":
                self.points[data["name"]] = (node.x + offset_x, node.y + offset_y)

    def _center_drawing(self):
        """
            .. note:: This method is private and not intended for external use.

            Adjusts the drawing entities to compensate for offset introduced by hanging the entities
            off the origin node.
        """

        new_entities_copy = deepcopy(self.new_entities)

        for e in new_entities_copy:
            if e.dxftype() == "LINE":
                start = e.dxf.start
                end = e.dxf.end
                e.update_dxf_attribs({"start": Vec3(start.x - self.offset_drawing_x, start.y - self.offset_drawing_y),
                                      "end": Vec3(end.x - self.offset_drawing_x, end.y - self.offset_drawing_y)})
            else:
                center = e.dxf.center
                e.update_dxf_attribs(
                    {"center": Vec3(center.x - self.offset_drawing_x, center.y - self.offset_drawing_y)})

        bounding_box = bbox.extents(new_entities_copy, cache=bbox.Cache())

        center_x = -bounding_box.rect_vertices()[0].x
        center_y = -bounding_box.rect_vertices()[0].y

        for e in self.new_entities:
            if e.dxftype() in ["ARC", "CIRCLE"]:
                center = e.dxf.center

                e.update_dxf_attribs({"center": (center[0] + center_x, center[1] + center_y)})

            elif e.dxftype() == "LINE":
                start = e.dxf.start
                end = e.dxf.end

                e.update_dxf_attribs({"start": (start[0] + center_x, start[1] + center_y)})
                e.update_dxf_attribs({"end": (end[0] + center_x, end[1] + center_y)})

        for k, v in self.points.items():
            self.points[k] = (round(v[0] + center_x, 3), round(v[1] + center_y, 3))
