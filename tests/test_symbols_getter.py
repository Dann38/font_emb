import unittest
import os
from symbols_extractor import symbols_extractor


class test_symbols_getter(unittest.TestCase):

    def test_order(self):
        path_project = os.path.abspath(os.path.join(os.getcwd(), "."))
        path_img = os.path.join(path_project, 'example_img', "1_img.png")
        excepted_result = ['a 195 180 208 196 0', 'a 127 129 139 145 0', 's 143 129 154 145 0', 'd 157 129 172 153 0', 'a 175 129 188 145 0', 's 192 129 204 145 0', 'd 207 129 221 153 0', 'a 224 129 237 145 0', 's 241 129 253 145 0', '']

        exual_result = symbols_extractor.take_symbols_and_bboxes(path_img, "eng")

        self.assertEqual(excepted_result, exual_result)