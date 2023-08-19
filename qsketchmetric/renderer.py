import math
import string
from copy import deepcopy
from pathlib import Path
from random import choice

import ezdxf
from ezdxf import units, bbox
from ezdxf.math import Vec3
from py_expression_eval import Parser
from ezdxf.document import Drawing


class Renderer:
    """
    Class for rendering parametric 2D dxf drawings
    """

    def __init__(self, input_parametric_path: Path, output_rendered_object: Drawing, extra_variables: dict = None,
                 offset_drawing: tuple = (0, 0)):
        """
        Initializes a new instance of the class.

        Args:
            input_parametric_path (Path): The path to the input parametric file from which the drawing will be rendered.

            output_rendered_object (Drawing): The output rendered ezdxf drawing object to which the drawing
            will be rendered. Drawing object must be created beforehand using ezdxf.new(). Passing an existing object
            allows to combine multiple drawings into one.

            extra_variables (dict, optional): Extra constant variables to be used in the mathematics expressions.

            offset_drawing (tuple, optional): The offset values for the parametric drawing. Defaults to (0, 0).
        """

        if extra_variables is None:
            extra_variables = dict()

        self.new_points = {}
        self.input_parametric_path = input_parametric_path

        self.input_dxf = ezdxf.readfile(self.input_parametric_path)
        self.input_msp = self.input_dxf.modelspace()

        self.output_dxf = output_rendered_object
        self.output_msp = self.output_dxf.modelspace()

        self.offset_drawing_x = offset_drawing[0]
        self.offset_drawing_y = offset_drawing[1]

        self.variables = {} | extra_variables

        self.graph = {}
        self.visited_graph = {}
        self.points = {}
        self.new_entities = []

    def render(self):
        """
            Render the input DXF to produce an  output DXF with the applied transformations.

            The method executes the following steps:
            1. Sets the units of the input DXF to millimeters.
            2. Extracts and evaluates custom variables defined in the input DXF's MTEXT
            3. Initiates a depth-first search (`_dfs`) starting from the root node, to traverse the graph and derive
               new points based on the graph relationships.
            4. Constructs the final output DXF based on the derived points using `_construct_rest_of_dxf`.
            5. Adjusts the drawing to be centered using `_center_drawing`.

            Returns:
                dict: A dictionary containing the points used in the rendered output.

        """

        self.input_dxf.units = units.MM

        self.variables |= {
            v.split(":")[0].strip(): float(Parser().parse(v.split(":")[1].strip()).evaluate(self.variables)) for v in
            filter(None, self.input_dxf.query("MTEXT")[0].text.split("----- custom -----")[-1].split("\P"))}

        self._prepare_graph()

        root = min(self.graph.keys())
        self.new_points = {root: (root.x, root.y)}

        self._dfs(root, 0, 0)
        self._construct_rest_of_dxf()
        self._center_drawing()

        return self.points

    def get_bounding_box(self):
        """
        Get the bounding box of the output DXF.

        This function calculates and returns the bounding box of the output DXF. The bounding box is a rectangle that
        encloses all the entities in the DXF file.

        Returns:
            A tuple containing the width and height of the bounding box. The width is calculated as the difference
            between the x-coordinates of the top-right and bottom-left vertices of the bounding box. The height is calculated as the difference between the y-coordinates of the top-right and bottom-left vertices of the bounding box.
        """

        bounding_box = bbox.extents(self.output_msp, cache=bbox.Cache())

        return (bounding_box.rect_vertices()[2].x - bounding_box.rect_vertices()[0].x,
                bounding_box.rect_vertices()[2].y - bounding_box.rect_vertices()[0].y)

    def _prepare_graph(self):
        """
            Prepares the graph by iterating through the entities in the input_msp entity space.
            For each entity, it extracts relevant information from the xdata and creates a new_length value.
            If the entity is a LINE, it calculates the start and end points, adds the line type to the output_dxf linetypes,
            and updates the graph and visited_graph dictionaries accordingly.
            If the entity is a CIRCLE, it calculates the center point and updates the graph dictionary.
            If the entity is an ARC, it calculates the center point and updates the graph dictionary.
            If the entity is a POINT, it calculates the location point and updates the graph dictionary.
        """

        for entity in filter(lambda x: x.dxftype() != "MTEXT", self.input_msp.entity_space.entities):
            new_length = "?"

            xdata = dict(map(lambda x: (x[1].split(":")), entity.get_xdata("QCAD")))

            constant_xdata = xdata.get("c", False)
            line_xdata = xdata.get("line", False)
            line_type = "BYLAYER"

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

                e_data = {"layer": entity.dxf.layer, "linetype": line_type}

                self.graph[end] = self.graph.get(end, []) + [("LINE", start, new_length, e_data)]
                self.graph[start] = self.graph.get(start, []) + [("LINE", end, new_length, e_data)]
                self.visited_graph[end] = self.visited_graph.get(end, []) + [(e_data["layer"], start)]
                self.visited_graph[start] = self.visited_graph.get(start, []) + [(e_data["layer"], end)]

            elif entity.dxftype() == "CIRCLE":
                center = entity.dxf.center
                center = Vec3(round(center.x, 3), round(center.y, 3), 0)
                self.variables["c"] = entity.dxf.radius

                new_length = Parser().parse(constant_xdata).evaluate(self.variables)

                e_data = {"layer": entity.dxf.layer, "radius": entity.dxf.radius,
                          "linetype": line_type}

                self.graph[center] = self.graph.get(center, []) + [("CIRCLE", center, new_length, e_data)]

            elif entity.dxftype() == "ARC":
                center = entity.dxf.center
                center = Vec3(round(center.x, 3), round(center.y, 3), 0)
                self.variables["c"] = entity.dxf.radius

                new_length = Parser().parse(constant_xdata).evaluate(self.variables)

                e_data = {"layer": entity.dxf.layer, "radius": entity.dxf.radius,
                          "start_angle": entity.dxf.start_angle,
                          "end_angle": entity.dxf.end_angle, "linetype": line_type}

                self.graph[center] = self.graph.get(center, []) + [("ARC", center, new_length, e_data)]

            elif entity.dxftype() == "POINT":
                location = entity.dxf.location
                location = Vec3(round(location.x, 3), round(location.y, 3), 0)

                e_data = {"name": list(xdata.values())[0]}

                self.graph[location] = self.graph.get(location, []) + [("POINT", location, 0, e_data)]

    def _construct_rest_of_dxf(self):
        """
            Constructs the remaining part of the DXF file based on the graph data.
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
            Performs a depth-first search (DFS) traversal on the graph starting from the given node.

            Args:
                node (Vec3): The starting node for the DFS traversal. It is updated recursively for each node

                offset_x (float): The x-coordinate offset to be applied to the node and its connected entities.
                It is updated recursively for each node depending on the length of the line connecting the node to its
                connected entities.

                offset_y (float): The y-coordinate offset to be applied to the node and its connected entities.
                It is updated recursively for each node depending on the length of the line connecting the node to its
                connected entities.

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
            Centers the drawing by calculating the bounding box of the output DXF and adjusting the coordinates of the
            entities and points accordingly. The centering is done to compensate for the offset that was added to
            the drawing by hanging the entities off the origin.
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
