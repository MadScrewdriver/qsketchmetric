import unittest
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch, ANY, MagicMock

import ezdxf.entities
from ezdxf.math import Vec3

from qsketchmetric.semiautomatic import SemiAutomaticParameterization


class TestSemiAutomaticParameterize(unittest.TestCase):

    def setUp(self):
        self.mock_input_dxf_path = Path("/sample/path/to/input.dxf")
        self.mock_input_dxf = Mock()
        self.mock_input_msp = Mock()

        self.point1 = Vec3(0, 3, 0)
        self.point2 = Vec3(1, 2, 0)
        self.point3 = Vec3(2, 1, 0)
        self.point4 = Vec3(3, 3, 0)

        self.rpoint1 = Vec3(-0.0001, 3.0004, 0)
        self.rpoint2 = Vec3(1.0002, 1.9995, 0)
        self.rpoint3 = Vec3(1.9999, 0.9998, 0)
        self.rpoint4 = Vec3(3.0003, 2.9996, 0)

        self.mock_graph_lines = {
            self.point1: [],
            self.point2: [],
        }

        self.mock_graph_lines_big = {
            self.point1: [self.point2],
            self.point2: [self.point1],
            self.point3: [],
        }

        self.entities = ['LINE', 'CIRCLE', 'ARC', 'POINT']

        self.dxf_attribs = {
            "start": self.rpoint1,
            "end": self.rpoint2,
            "center": self.rpoint3,
        }

        self.mock_entities = []
        for entity in self.entities:
            mock = Mock(dxftype=lambda entity=entity: entity)
            mock.dxf = Mock(
                start=self.dxf_attribs["start"],
                end=self.dxf_attribs["end"],
                center=self.dxf_attribs["center"],
            )
            self.mock_entities.append(mock)

        self.mock_input_msp.entity_space.entities = self.mock_entities

    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    @patch("ezdxf.readfile")
    def test_init_with_default_args(self, mock_readfile, mock_handle_output_path):
        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)
        self.assertEqual(obj.value, "c")
        self.assertEqual(obj.output_dxf_path, None)
        mock_handle_output_path.assert_called_once()

    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    @patch("ezdxf.readfile")
    def test_init_with_custom_args(self, mock_readfile, mock_handle_output_path):
        obj = SemiAutomaticParameterization(self.mock_input_dxf_path, default_value="?",
                                            output_dxf_path=Path("/custom/output.dxf"))
        self.assertEqual(obj.value, "?")
        self.assertEqual(obj.output_dxf_path, Path("/custom/output.dxf"))
        mock_handle_output_path.assert_called_once()

    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    @patch("ezdxf.readfile")
    def test_parametrize(self, mock_readfile, mock_handle_output_path):
        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)

        obj._set_appid_and_graph = Mock()
        obj._find_and_union = Mock()
        obj._draw_virtual_lines = Mock()
        obj._center_drawing = Mock()
        obj._draw_variables = Mock()
        obj.input_dxf = Mock()

        obj.parametrize()

        # Assert methods are called
        obj._set_appid_and_graph.assert_called_once()
        obj._find_and_union.assert_called_once()
        obj._draw_virtual_lines.assert_called_once()
        obj._center_drawing.assert_called_once()
        obj._draw_variables.assert_called_once()

        obj.input_dxf.saveas.assert_called_once_with(obj.output_dxf_path)

    @patch("pathlib.Path.is_file", return_value=True)
    @patch("ezdxf.readfile")
    @patch('os.path.exists', side_effect=[False, True])
    @patch('os.mkdir')
    @patch('shutil.move')
    def test_handle_output_path(self, mock_move, mock_mkdir, mock_exists, mock_readfile, mock_path):
        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)

        expected_output_path = self.mock_input_dxf_path.parent / "parametric" / "parametric_input.dxf"
        expected_backup_path = expected_output_path.parent / ".backup_parametric_input.dxf"

        self.assertEqual(obj.output_dxf_path, expected_output_path)
        mock_mkdir.assert_called_once_with(expected_output_path.parent)
        mock_move.assert_called_once_with(expected_output_path, expected_backup_path)

    @patch.object(SemiAutomaticParameterization, "_find_parent")
    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    @patch("ezdxf.readfile")
    def test_draw_virtual_lines(self, mock_readfile, mock_handle_output_path, mock_find_parent):
        mock_find_parent_side_effect = []
        # add
        mock_find_parent_side_effect.extend([self.point1, self.point2])
        # subgraph join_points point1
        mock_find_parent_side_effect.extend([self.point1, self.point1, self.point2, self.point1] * 2)
        # update parents point1
        mock_find_parent_side_effect.extend([self.point2, self.point1])
        # ever after parent is point1
        mock_find_parent_side_effect.extend([self.point1] * 8)

        mock_find_parent.side_effect = mock_find_parent_side_effect

        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)
        obj.input_dxf = self.mock_input_dxf
        obj._draw_virtual_x_y_lines = Mock()
        obj.graph_lines = self.mock_graph_lines
        obj._draw_virtual_lines()
        obj.input_dxf.layers.new.assert_called_once_with(name="VIRTUAL_LAYER", dxfattribs=ANY)

        self.assertEqual(obj.available_parents, {self.point1, self.point2})
        self.assertEqual(obj.parents[self.point2], self.point1)
        obj._draw_virtual_x_y_lines.assert_called_once_with(self.point1, self.point2)

    @patch("ezdxf.readfile")
    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    def test_find_parent(self, mock_readfile, mock_handle_output_path):
        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)
        obj.parents = {self.point1: self.point1, self.point2: self.point1,
                       self.point3: self.point2, self.point4: self.point3}

        self.assertEqual(obj._find_parent(self.point1), self.point1)
        self.assertEqual(obj._find_parent(self.point2), self.point1)
        self.assertEqual(obj._find_parent(self.point3), self.point1)
        self.assertEqual(obj._find_parent(self.point4), self.point1)

    @patch.object(SemiAutomaticParameterization, "_dfs")
    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    @patch("ezdxf.readfile")
    def test_find_and_union(self, mock_readfile, mock_handle_output_path, mock_dfs):
        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)
        obj.graph_lines = self.mock_graph_lines
        obj._find_and_union()

        self.assertEqual(mock_dfs.call_count, 2)

    @patch.object(SemiAutomaticParameterization, "_find_parent")
    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    @patch("ezdxf.readfile")
    def test_dfs(self, mock_readfile, mock_handle_output_path, mock_find_parent):
        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)
        obj.graph_lines = self.mock_graph_lines_big

        mock_find_parent.side_effect = [self.point1, self.point1]
        visited = []
        obj._dfs(self.point1, visited)
        self.assertEqual([self.point1, self.point2], visited)
        self.assertEqual(obj.parents[self.point1], self.point1)

    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    @patch("ezdxf.readfile")
    def test_set_appid_and_graph(self, mock_readfile, mock_handle_output_path):
        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)
        obj.input_dxf = self.mock_input_dxf
        obj.input_msp = self.mock_input_msp
        obj.graph_lines = {}

        obj._set_appid_and_graph()

        self.assertEqual(obj.graph_lines, {self.point1: [self.point2],
                                           self.point2: [self.point1], self.point3: []})

        for e in self.mock_entities:
            if e.dxftype() == "LINE":
                e.discard_xdata.assert_called_once_with(obj.APPID)
                e.set_xdata.assert_called_once_with(obj.APPID, [(1000, "c:c")])
                e.update_dxf_attribs.assert_any_call({"start": self.point1})
                e.update_dxf_attribs.assert_any_call({"end": self.point2})

            elif e.dxftype() in ["ARC", "CIRCLE"]:
                e.discard_xdata.assert_called_once_with(obj.APPID)
                e.set_xdata.assert_called_once_with(obj.APPID, [(1000, "c:c")])
                e.update_dxf_attribs.assert_called_once_with({"center": self.point3})

            else:
                e.destroy.assert_called_once()

    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    @patch("ezdxf.readfile")
    def test_center_drawing(self, mock_readfile, mock_handle_output_path):

        mock_input_dxf = ezdxf.new('R2010')
        mock_input_msp = mock_input_dxf.modelspace()

        new_entities = [
            mock_input_msp.add_line(self.point2, self.point3),
            mock_input_msp.add_line(self.point2, self.point4),
            mock_input_msp.add_circle(self.point4, 2),
            mock_input_msp.add_arc(self.point4, 1, 0, 90)
        ]

        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)
        obj.input_msp = mock_input_msp
        obj._center_drawing()

        expected_offset_x = self.point2.x
        expected_offset_y = self.point3.y

        expected_offset = Vec3(expected_offset_x, expected_offset_y)

        # Validate if each entity was translated correctly
        for entity in new_entities:
            if entity.dxftype() == "LINE":
                self.assertEqual(self.point2 - expected_offset, entity.dxf.start)
                self.assertTrue(entity.dxf.end in [self.point3 - expected_offset,
                                                   self.point4 - expected_offset])

            elif entity.dxftype() in ["ARC", "CIRCLE"]:
                self.assertEqual(self.point4 - expected_offset, entity.dxf.center)

    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    @patch("ezdxf.readfile")
    def test_draw_virtual_x_y_lines(self, mock_readfile, mock_handle_output_path):

        self.point1 = Vec3(0, 3, 0)
        self.point2 = Vec3(1, 2, 0)
        self.point3 = Vec3(2, 1, 0)
        self.point4 = Vec3(3, 3, 0)

        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)
        obj.input_msp = Mock()

        obj._draw_virtual_x_y_lines(self.point1, self.point3)

        obj.input_msp.add_line.assert_any_call(self.point1, (self.point3.x, self.point1.y),
                                               dxfattribs={"layer": "VIRTUAL_LAYER"})
        obj.input_msp.add_line.assert_any_call(self.point3, (self.point3.x, self.point1.y),
                                               dxfattribs={"layer": "VIRTUAL_LAYER"})

    @patch.object(SemiAutomaticParameterization, "_handle_output_path")
    @patch("ezdxf.readfile")
    def test_draw_variables(self, mock_readfile, mock_handle_output_path):
        text = "Available variables: \P\P----- build in -----\P\Pc: const\P?: undefined \P\P ----- custom -----\P\P"

        obj = SemiAutomaticParameterization(self.mock_input_dxf_path)
        obj.input_msp = Mock()

        variable_text = Mock()
        obj.input_msp.add_mtext.return_value = variable_text

        obj._draw_variables()
        obj.input_msp.add_mtext.assert_called_once_with(text, dxfattribs=ANY)
        self.assertEqual(variable_text.dxf.char_height, 10)
        variable_text.set_location.assert_called_once()


if __name__ == "__main__":
    unittest.main()
