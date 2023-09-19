import unittest
from pathlib import Path
from unittest.mock import Mock, patch, ANY, MagicMock

import ezdxf.entities
from ezdxf.math import Vec3

from qsketchmetric.renderer import Renderer


class TestRenderer(unittest.TestCase):

    def setUp(self):
        """
        Set up the test case by creating the necessary mocks and data.
        """

        self.mock_input_dxf = Mock()
        self.mock_output_dxf = Mock()

        self.circle_radius = 5
        self.arc_radius = 1
        self.start_angle = 0
        self.end_angle = 90
        self.line1_length = 3
        self.line2_length = 4

        self.offset_x = 10
        self.offset_y = 10
        self.offset = Vec3(self.offset_x, self.offset_y)

        self.point1 = Vec3(0, 0)
        self.point2 = Vec3(0, 1)
        self.point3 = Vec3(1, 0)
        self.point4 = Vec3(1, 1)

        self.new_point1 = Vec3(0, 0)
        self.new_point2 = Vec3(0, self.line1_length)
        self.new_point3 = Vec3(self.line2_length, 0)

        self.new_points = {
            self.point1: self.new_point1,
            self.point2: self.new_point2,
            self.point3: self.new_point3,
        }

        self.new_point1_off = self.new_point1 + self.offset
        self.new_point2_off = self.new_point2 + self.offset
        self.new_point3_off = self.new_point3 + self.offset

        self.new_points_off = {
            self.point1: self.new_point1_off,
            self.point2: self.new_point2_off,
            self.point3: self.new_point3_off,
        }

        self.graph = {
            self.point1: [
                ("LINE", self.point2, self.line1_length, {"layer": "VIRTUAL_LAYER", "linetype": "line_linetype"}),
                ("LINE", self.point3, self.line2_length, {"layer": "line_layer", "linetype": "line_linetype"}),
                ("ARC", self.point1, self.arc_radius, {"layer": "arc_layer", "linetype": "arc_linetype",
                                                       "radius": self.arc_radius, "start_angle": self.start_angle,
                                                       "end_angle": self.end_angle})],

            self.point2: [("LINE", self.point3, "?", {"layer": "line_layer", "linetype": "line_linetype"}),
                          ("LINE", self.point1, self.line1_length,
                           {"layer": "VIRTUAL_LAYER", "linetype": "line_linetype"}),
                          ("CIRCLE", self.point2, self.circle_radius,
                           {"layer": "circle_layer", "linetype": "circle_linetype", "radius": self.circle_radius})],

            self.point3: [("LINE", self.point2, "?", {"layer": "line_layer", "linetype": "line_linetype"}),
                          ("LINE", self.point1, self.line2_length,
                           {"layer": "circle_layer", "linetype": "circle_linetype"}),
                          ("POINT", self.point3, 0, {"name": "mock"}),
                          ("INSERT", self.point3, 0,
                          {"layer": "insert_layer", "linetype": "insert_linetype", "name": "insert",
                           "xscale": 1.5, "yscale": 1})],
        }

        self.entities = ['LINE', 'CIRCLE', 'ARC', 'INSERT']

        self.dxf_attribs = {
            "start": self.point1,
            "end": self.point2,
            "layer": "layer",
            "center": self.point3,
            "radius": self.circle_radius,
            "start_angle": self.start_angle,
            "end_angle": self.end_angle,
            "location": self.point3,
            "insert": self.point4,
            "name": "mock"
        }

        self.mock_entities = []
        for entity in self.entities:
            mock = Mock(dxftype=lambda entity=entity: entity)
            mock.dxf = Mock(
                start=self.dxf_attribs["start"],
                end=self.dxf_attribs["end"],
                layer=self.dxf_attribs["layer"],
                center=self.dxf_attribs["center"],
                radius=self.dxf_attribs["radius"],
                start_angle=self.dxf_attribs["start_angle"],
                end_angle=self.dxf_attribs["end_angle"],
                insert=self.dxf_attribs["insert"],
            )
            self.mock_entities.append(mock)

    @patch('ezdxf.readfile')
    def test_initialization(self, mock_readfile):
        """
            Test the initialization of the Renderer class to ensure that the input arguments are set correctly.
        """

        renderer = Renderer(
            input_parametric_path=Path('/path/to/input.dxf'),
            output_rendered_object=self.mock_output_dxf,
            variables={'var1': 10, 'var2': 5},
            offset=(self.offset_x, self.offset_y)
        )
        self.assertEqual(renderer.input_parametric_path, Path('/path/to/input.dxf'))
        self.assertEqual(renderer.output_dxf, self.mock_output_dxf)
        self.assertEqual(renderer.variables, {'var1': 10, 'var2': 5})
        self.assertEqual(renderer.offset_x, self.offset_x)
        self.assertEqual(renderer.offset_y, self.offset_y)

    @patch('qsketchmetric.renderer.Renderer._prepare_layers')
    @patch('ezdxf.readfile')
    def test_prepare_graph(self, mock_readfile, mock_prepare_layers):
        """
            Test the _prepare_graph method to ensure that the graph and visited_graph dictionaries
            are constructed correctly.
        """

        for mock_entity in self.mock_entities:
            mock_entity.get_xdata = lambda x: [(None, "c:2*100"), (None, "line:10 5")]
            mock_entity.dxf.name = f"{self.dxf_attribs['name']}"
            mock_entity.block().entity_space.entities = self.mock_entities

            if mock_entity.dxftype() == "INSERT":
                mock_entity.get_xdata = lambda x: [(None, "c:2*100@?"), (None, "line:10 5")]

        point_mock = Mock(dxftype=lambda: "POINT", get_xdata=lambda x: [(None, f"{self.dxf_attribs['name']}:"
                                                                               f"{self.dxf_attribs['name']}")])
        point_mock.dxf = Mock(location=self.dxf_attribs["location"], layer=self.dxf_attribs["layer"])

        self.mock_entities.append(point_mock)
        self.mock_entities.append(Mock(dxftype=lambda: "MTEXT"))

        self.mock_input_dxf.modelspace().entity_space.entities = self.mock_entities
        self.mock_output_dxf.blocks = ["mock"]

        mock_readfile.return_value = self.mock_input_dxf
        renderer = Renderer(
            input_parametric_path=Path('/path/to/input.dxf'),
            output_rendered_object=self.mock_output_dxf
        )

        renderer.get_bb_dimensions = Mock(return_value=(10, 5))

        renderer._prepare_graph()

        renderer.output_dxf.linetypes.add.assert_called_with(
            name=ANY,
            pattern=ANY,
            description="- - - - - -",
        )

        # Check for LINE entities
        self.assertIn(self.point1, renderer.graph)
        self.assertIn(self.point2, renderer.graph)

        # Check for CIRCLE, ARC entities
        self.assertIn(self.point3, renderer.graph)

        # Check for POINT entities
        self.assertIn(self.point3, renderer.graph)

        # Check for INSERT entities
        self.assertIn(self.point4, renderer.graph)


        self.assertIn((self.dxf_attribs["layer"], self.point2), renderer.visited_graph[self.point1])
        self.assertIn((self.dxf_attribs["layer"], self.point1), renderer.visited_graph[self.point2])

        for point, items in renderer.graph.items():
            for item in items:
                name = item[0]
                position = item[1]
                new_length = item[2]
                edata = item[3]

                if name != "POINT":
                    self.assertEqual(edata["layer"], self.dxf_attribs["layer"])
                    self.assertTrue(edata["linetype"].startswith(f"10.0_5.0_"))

                if name == "ARC":
                    self.assertEqual(edata["radius"], self.dxf_attribs["radius"])
                    self.assertEqual(edata["start_angle"], self.dxf_attribs["start_angle"])
                    self.assertEqual(edata["end_angle"], self.dxf_attribs["end_angle"])

                elif name == "CIRCLE":
                    self.assertEqual(edata["radius"], self.dxf_attribs["radius"])

                elif name == "POINT":
                    self.assertEqual(edata["name"], self.dxf_attribs["name"])

                elif name == "INSERT":
                    self.assertEqual(edata["xscale"], 20,
                    self.assertEqual(edata["yscale"], 20))

        mock_prepare_layers.assert_called_once()

    @patch('ezdxf.readfile')
    def test_dfs(self, mock_readfile):
        """
           Test the depth-first search functionality of the Renderer to ensure it processes the graph correctly.
           """
        # Mock the input DXF entities for your test case
        mock_readfile.return_value = self.mock_input_dxf

        renderer = Renderer(
            input_parametric_path=Path('/path/to/input.dxf'),
            output_rendered_object=self.mock_output_dxf
        )

        renderer.graph = self.graph

        renderer.visited_graph = {
            self.point1: [("VIRTUAL_LAYER", self.point2), ("line_layer", self.point3)],
            self.point2: [("VIRTUAL_LAYER", self.point1), ("line_layer", self.point3)],
            self.point3: [("line_layer", self.point1), ("line_layer", self.point2)],
        }

        renderer.new_points = {
            self.point1: self.new_point1,
        }

        renderer.offset_x = self.offset_x
        renderer.offset_y = self.offset_y

        # Call the _dfs method with the mocked values
        renderer._dfs(self.point1, 0, 0)

        # Assertions for added entities
        self.mock_output_dxf.modelspace().add_line.assert_called_with(
            self.new_point1_off, self.new_point3_off,
            dxfattribs={'layer': 'line_layer', 'linetype': 'line_linetype'})
        self.mock_output_dxf.modelspace().add_circle.assert_called_with(
            self.new_point2_off, self.circle_radius,
            dxfattribs={'layer': 'circle_layer', 'linetype': 'circle_linetype'})
        self.mock_output_dxf.modelspace().add_arc.assert_called_with(
            self.new_point1_off, self.arc_radius, self.start_angle, self.end_angle,
            dxfattribs={'layer': 'arc_layer', 'linetype': 'arc_linetype'})
        self.mock_output_dxf.modelspace().add_blockref.assert_called_with('insert', self.new_point3_off,
            dxfattribs={'layer': 'insert_layer', 'linetype': 'insert_linetype', 'xscale': 1.5, 'yscale': 1})

        self.assertEqual(renderer.output_dxf.modelspace().add_point.call_count, 0)
        self.assertEqual(len(renderer.new_entities), 4)

        # Assertions for new_points dictionary
        self.assertEqual(renderer.new_points, self.new_points)
        self.assertEqual(renderer.points, {"mock": self.new_point3})

        # Assertions for visited_graph and graph dictionaries
        self.assertTrue(renderer.visited_graph[self.point1] == [])
        self.assertTrue(renderer.visited_graph[self.point2] == [('line_layer', self.point3)])
        self.assertTrue(renderer.visited_graph[self.point3] == [('line_layer', self.point2)])

    @patch('ezdxf.readfile')
    def test_construct_rest_of_dxf(self, mock_readfile):
        """
        Test the _construct_rest_of_dxf method of the Renderer class to ensure it processes and
        adds entities to the output DXF.
        """

        mock_readfile.return_value = self.mock_input_dxf

        # Create a Renderer instance
        renderer = Renderer(
            input_parametric_path=Path('/path/to/input.dxf'),
            output_rendered_object=self.mock_output_dxf
        )

        # Mock data
        renderer.new_entities = [
            Mock().modelspace().add_line(),
            Mock().modelspace().add_circle(),
            Mock().modelspace().add_arc(),
            Mock().modelspace().add_blockref(),
        ]

        renderer.new_points = self.new_points
        renderer.graph = self.graph

        renderer.visited_graph = {
            self.point1: [],
            self.point2: [("line_layer", self.point3)],
            self.point3: [("line_layer", self.point2)],
        }

        renderer.offset_x = self.offset_x
        renderer.offset_y = self.offset_y

        # Call the _construct_rest_of_dxf method
        renderer._construct_rest_of_dxf()

        # Assertions
        self.mock_output_dxf.modelspace().add_line.assert_called_with(
            self.new_point2_off, self.new_point3_off, dxfattribs={'layer': 'line_layer', 'linetype': 'line_linetype'})

        # Ensure other entity types aren't being added unintentionally
        self.mock_output_dxf.modelspace().add_arc.assert_not_called()
        self.mock_output_dxf.modelspace().add_point.assert_not_called()
        self.mock_output_dxf.modelspace().add_circle.assert_not_called()
        self.mock_output_dxf.modelspace().add_blockref.assert_not_called()

        # Optionally, if the method modifies the new_entities list
        self.assertEqual(len(renderer.new_entities), 5)
        self.assertTrue(all(value == [] for value in renderer.visited_graph.values()))
        self.assertEqual(self.new_points.keys(), renderer.visited_graph.keys())

    @patch('ezdxf.readfile')
    def test_get_bb_dimensions(self, mock_readfile):
        """
        Test the get_bounding_box method of the Renderer class to ensure it returns the correct width and height of all
        the entities in the output DXF.
        """

        mock_output_dxf = ezdxf.new('R2010')
        insert = mock_output_dxf.blocks.new(name='insert')
        insert.add_line((0, 0), (5, 0))

        mock_output_msp = mock_output_dxf.modelspace()

        mock_output_msp.add_line(self.new_point1_off, self.new_point2_off),
        mock_output_msp.add_line(self.new_point1_off, self.new_point3_off),
        mock_output_msp.add_circle(self.new_point1_off, self.circle_radius),
        mock_output_msp.add_arc(self.new_point2_off, self.arc_radius, self.start_angle, self.end_angle)
        mock_output_msp.add_blockref('insert', self.new_point3_off,
                                     dxfattribs={'xscale': 2, 'yscale': 1})

        renderer = Renderer(
            input_parametric_path=Path('/path/to/input.dxf'),
            output_rendered_object=mock_output_dxf
        )

        w, h = renderer.get_bb_dimensions()

        self.assertEqual(w, 19)
        self.assertEqual(h, 10)

    @patch('ezdxf.readfile')
    def test_center_drawing(self, mock_readfile):
        """
        Test the _center_drawing method of the Renderer class to ensure it translates the newly drawn entities
        correctly. Also, ensure that the old entities are not translated. The centering is done to compensate for
        the offset that was added to the drawing by hanging the entities off the origin.
        """

        mock_readfile.return_value = self.mock_input_dxf

        mock_output_dxf = ezdxf.new('R2010')
        mock_output_msp = mock_output_dxf.modelspace()

        old_entities_point = Vec3(-1, -1)

        old_entities = [
            mock_output_msp.add_line(self.point1, old_entities_point),
            mock_output_msp.add_circle(old_entities_point, self.circle_radius),
            mock_output_msp.add_arc(old_entities_point, self.arc_radius, self.start_angle, self.end_angle)
        ]

        new_entities = [
            mock_output_msp.add_line(self.new_point1_off, self.new_point2_off),
            mock_output_msp.add_line(self.new_point1_off, self.new_point3_off),
            mock_output_msp.add_circle(self.new_point1_off, self.circle_radius),
            mock_output_msp.add_arc(self.new_point2_off, self.arc_radius, self.start_angle, self.end_angle)
        ]

        renderer = Renderer(
            input_parametric_path=Path('/path/to/input.dxf'),
            output_rendered_object=self.mock_output_dxf
        )

        renderer.offset_x = self.offset_x
        renderer.offset_y = self.offset_y

        renderer.new_entities = new_entities

        renderer._center_drawing()

        expected_offset_x = self.offset_x + self.circle_radius
        expected_offset_y = self.offset_y + self.circle_radius
        expected_offset = Vec3(expected_offset_x, expected_offset_y)

        # Validate if each entity was translated correctly
        for entity in new_entities:
            if entity.dxftype() == "LINE":
                self.assertEqual(self.new_point1 + expected_offset, entity.dxf.start)
                self.assertTrue(entity.dxf.end in [self.new_point2 + expected_offset,
                                                   self.new_point3 + expected_offset])
            if entity.dxftype() == "CIRCLE":
                self.assertEqual(self.new_point1 + expected_offset, entity.dxf.center)
            if entity.dxftype() == "ARC":
                self.assertEqual(self.new_point2 + expected_offset, entity.dxf.center)

        for old_entity in old_entities:
            if old_entity.dxftype() == "LINE":
                self.assertEqual(self.point1, old_entity.dxf.start)
                self.assertEqual(old_entities_point, old_entity.dxf.end)

            if old_entity.dxftype() in ["CIRCLE", "ARC"]:
                self.assertEqual(old_entities_point, old_entity.dxf.center)

    @patch('ezdxf.readfile')
    def test_render(self, mock_readfile):

        """
        Test the render method to ensure the graph is processed and the output DXF is populated.
        """

        mtext_text = "----- title -----\P foo1: foo2\P ----- custom ----- var1: 5*5 \P var2: 10/2"
        self.mock_input_dxf.query = lambda x: [Mock(text=mtext_text)]
        mock_readfile.return_value = self.mock_input_dxf

        renderer = Renderer(
            input_parametric_path=Path('/path/to/input.dxf'),
            output_rendered_object=self.mock_output_dxf
        )

        renderer.graph = self.graph
        renderer._prepare_graph = Mock()
        renderer._dfs = Mock()
        renderer._construct_rest_of_dxf = Mock()
        renderer._center_drawing = Mock()

        renderer.render()

        # Mock methods would have been called in the render process
        renderer._prepare_graph.assert_called_once()
        renderer._dfs.assert_called_once()
        renderer._construct_rest_of_dxf.assert_called_once()
        renderer._center_drawing.assert_called_once()

        self.assertTrue(renderer.variables == {'var1': 25, 'var2': 5})

    @patch('ezdxf.readfile')
    def test_prepare_layers(self, mock_readfile):

        """
        Test the render method to ensure the graph is processed and the output DXF is populated.
        """

        mock_readfile.return_value = self.mock_input_dxf
        self.mock_output_dxf.layers = MagicMock()

        layer = Mock()
        layer.dxf.name = 'layer'

        self.mock_output_dxf.layers.__iter__.return_value = iter([layer])

        renderer = Renderer(
            input_parametric_path=Path('/path/to/input.dxf'),
            output_rendered_object=self.mock_output_dxf
        )

        input_layers = {"layer": 1, "VIRTUAL_LAYER": 2, "CUSTOM_LAYER": 3}

        renderer._prepare_layers(input_layers)
        renderer.output_dxf.layers.new.assert_called_with(name="CUSTOM_LAYER", dxfattribs={'color': 3})
        renderer.output_dxf.layers.new.assert_called_once()


if __name__ == '__main__':
    unittest.main()
