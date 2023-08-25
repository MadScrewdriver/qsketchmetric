import math
import os
import shutil
from pathlib import Path

import ezdxf
from ezdxf import DXFTableEntryError, bbox
from ezdxf.math import Vec3
from typing import Optional


class SemiAutomaticParameterization:

    def __init__(self, input_dxf_path: Path, default_value: str = "c", output_dxf_path: Optional[Path] = None):
        """
        :param input_dxf_path: Path to the DXF file to be parameterized.
        :param default_value: **(Optional)** Default expression describing the entities. Defaults to "c".
        :param output_dxf_path: **(Optional)** Path for the output parameterized DXF file. If not provided, the
            output file will be saved in the "parametric" directory, in the same directory
            as the input file. With the name "parametric_" + input_file_name.

        The :class:`SemiAutomaticParameterize` class is used to semi-automatic parameterize a DXF file.
        By semi-automatic, it means that the user has to manually define the parameters of each entity after
        the parameterization process. Process includes:

        * Adding :ref:`MTEXT` entity.
        * Adding :ref:`VIRTUAL_LAYER` layer.
        * Adding default expression to each entity.
        * Joining entities with virtual lines in to the one coherent graph.
        """

        self.graph_lines: dict[Vec3, list[Vec3]] = {}
        self.parents: dict[Vec3, Vec3] = {}
        self.available_parents: set[Vec3] = set()
        self.APPID: str = "QCAD"
        self.value: str = default_value
        self.input_dxf_path: Path = input_dxf_path
        self.output_dxf_path: Optional[Path] = output_dxf_path

        self._handle_output_path()

        self.input_dxf = ezdxf.readfile(self.input_dxf_path)
        self.input_msp = self.input_dxf.modelspace()

    def parametrize(self):
        """
            The main method of the :class:`SemiAutomaticParameterize` class.
            Parametrizes the DXF file and saves it to the output path.
        """

        self._set_appid_and_graph()
        self._find_and_union()
        self._draw_virtual_lines()
        self._center_drawing()
        self._draw_variables()

        self.input_dxf.saveas(self.output_dxf_path)

    def _handle_output_path(self):
        """
            Handles the output path. If the output path is not provided, the output file will be saved in the
            "parametric" directory, in the same directory as the input file. With the name "parametric_" +
            input_file_name. If the output file already exists, it will be moved to the same directory as the
            input file with the name ".backup_parametric_" + input_file_name.
        """

        if self.output_dxf_path is None:
            self.output_dxf_path = (self.input_dxf_path.parent / "parametric" /
                                    ("parametric_" + self.input_dxf_path.name))

            if not os.path.exists(self.output_dxf_path.parent):
                os.mkdir(self.output_dxf_path.parent)

        if os.path.exists(self.output_dxf_path) and self.output_dxf_path.is_file():
            shutil.move(self.output_dxf_path, self.output_dxf_path.parent /
                        (".backup_parametric_" + self.input_dxf_path.name))

    def _draw_virtual_lines(self):
        """
            Joins the entities with virtual lines in to the one coherent graph.
        """

        self.input_dxf.layers.new(name="VIRTUAL_LAYER", dxfattribs={"linetype": "CONTINUOUS", "color": 40})

        for n in self.graph_lines.keys():
            self.available_parents.add(self._find_parent(n))

        for p in self.graph_lines.keys():

            subgraph_points = [n for n in self.graph_lines.keys() if self._find_parent(n) == self._find_parent(p)]
            join_points = [n for n in self.graph_lines.keys() if self._find_parent(n) != self._find_parent(p)]
            available_points = [(math.dist(s, j), s, j) for s in subgraph_points for j in join_points]

            if available_points:
                _, subgraph_point, join_point = min(available_points)

                current_parent = self._find_parent(join_point)
                new_parent = self._find_parent(subgraph_point)

                self.parents[current_parent] = new_parent
                self._draw_virtual_x_y_lines(subgraph_point, join_point)

    def _find_parent(self, node: Vec3) -> Vec3:
        """
            Finds the parent of the node.
        :param node: node to find the parent of. Updates while recursion progresses.
        :return: returns the parent of the node.
        """

        if self.parents[node] == self.parents[self.parents[node]]:
            return self.parents[node]
        else:
            self.parents[node] = self._find_parent(self.parents[node])
            return self.parents[node]

    def _find_and_union(self):
        """
            Finds and unions the graph in to the subgraphs.
        """

        self.parents = {k: k for k in self.graph_lines.keys()}
        visited = []

        for n in self.graph_lines.keys():
            if n not in visited:
                self._dfs(n, visited)

    def _dfs(self, node: Vec3, visited: list[Vec3]):
        """
            Depth first search algorithm.
        :param node: current node changing while recursion progresses.
        :param visited: list of already visited nodes grows while recursion progresses.
        """

        visited.append(node)
        for n in self.graph_lines[node]:
            if n not in visited:
                self.parents[self._find_parent(n)] = self._find_parent(node)
                self._dfs(n, visited)

    def _set_appid_and_graph(self):
        """
            Sets the XData and the graph of the entities.
        """


        try:
            self.input_dxf.appids.new(self.APPID)
        except DXFTableEntryError:
            pass

        for e in self.input_msp.entity_space.entities:
            if e.dxftype() == "LINE":
                start = Vec3(round(e.dxf.start.x, 3), round(e.dxf.start.y, 3))
                end = Vec3(round(e.dxf.end.x, 3), round(e.dxf.end.y, 3))

                e.discard_xdata(self.APPID)
                e.set_xdata(self.APPID, [(1000, self.value)])

                e.update_dxf_attribs({"start": start})
                e.update_dxf_attribs({"end": end})

                self.graph_lines[start] = self.graph_lines.get(start, []) + [end]
                self.graph_lines[end] = self.graph_lines.get(end, []) + [start]

            elif e.dxftype() in ["ARC", "CIRCLE"]:
                center = Vec3(round(e.dxf.center.x, 3), round(e.dxf.center.y, 3))

                e.discard_xdata(self.APPID)
                e.set_xdata(self.APPID, [(1000, self.value)])

                e.update_dxf_attribs({"center": center})
                self.graph_lines[center] = self.graph_lines.get(center, [])

            else:
                e.destroy()

    def _center_drawing(self):
        """
            Centers the parametric drawing.
        """

        entities = self.input_msp.entity_space.entities

        bounding_box = bbox.extents(entities, cache=bbox.Cache())
        bb_x = -bounding_box.rect_vertices()[0].x
        bb_y = -bounding_box.rect_vertices()[0].y

        for e in entities:
            if e.dxftype() == "LINE":
                start = e.dxf.start
                end = e.dxf.end

                e.update_dxf_attribs({"start": (start[0] + bb_x, start[1] + bb_y)})
                e.update_dxf_attribs({"end": (end[0] + bb_x, end[1] + bb_y)})

            elif e.dxftype() in ["ARC", "CIRCLE"]:
                center = e.dxf.center
                e.update_dxf_attribs({"center": (center[0] + bb_x, center[1] + bb_y)})

    def _draw_virtual_x_y_lines(self, subgraph_point: Vec3, join_point: Vec3):
        """
            Draws the virtual lines between the subgraph point and the join point.
        :param subgraph_point: point of the subgraph.
        :param join_point: point of the other subgraph.
        """

        delta_x = subgraph_point.x - join_point.x
        delta_y = subgraph_point.y - join_point.y

        if delta_x:
            line = self.input_msp.add_line(subgraph_point, (join_point.x, subgraph_point.y),
                                           dxfattribs={"layer": "VIRTUAL_LAYER"})
            line.set_xdata(self.APPID, [(1000, self.value)])

        if delta_y:
            line = self.input_msp.add_line(join_point, (join_point.x, subgraph_point.y),
                                           dxfattribs={"layer": "VIRTUAL_LAYER"})
            line.set_xdata(self.APPID, [(1000, self.value)])

    def _draw_variables(self):
        """
            Draws the MTEXT entity.
        """

        text = "Available variables: \P\P----- buld in -----\P\Pc: const\P?: undefined \P\P ----- custom -----\P\P"
        variable_text = self.input_msp.add_mtext(text, dxfattribs={"attachment_point": 8})

        variable_text.dxf.char_height = 10
        variable_text.set_location(insert=(-100, 100, 0), rotation=0)
