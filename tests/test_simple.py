#!/usr/bin/env python3
import os
import os.path

import unittest
import fasm


def example(fname):
    return os.path.join(os.path.dirname(__file__), '..', 'examples', fname)


def check_round_trip(test, result):
    s = fasm.fasm_tuple_to_string(result)
    test.assertEqual(list(fasm.parse_fasm_string(s)), result)


class TestFasm(unittest.TestCase):
    def test_blank_file(self):
        result = list(fasm.parse_fasm_filename(example('blank.fasm')))
        self.assertEqual(result, [])

        check_round_trip(self, result)

    def test_comment_file(self):
        result = list(fasm.parse_fasm_filename(example('comment.fasm')))
        self.assertEqual(
            result, [
                fasm.FasmLine(
                    set_feature=None,
                    annotations=None,
                    comment=' Only a comment.',
                )
            ])

        check_round_trip(self, result)

    def test_one_line_feature(self):
        result = list(fasm.parse_fasm_filename(example('feature_only.fasm')))
        self.assertEqual(
            result, [
                fasm.FasmLine(
                    set_feature=fasm.SetFasmFeature(
                        feature='EXAMPLE_FEATURE.X0.Y0.BLAH',
                        start=None,
                        end=None,
                        value=1,
                        value_format=None,
                    ),
                    annotations=None,
                    comment=None,
                )
            ])

        self.assertEqual(
            fasm.fasm_tuple_to_string(result), 'EXAMPLE_FEATURE.X0.Y0.BLAH\n')
        check_round_trip(self, result)

    def test_examples_file(self):
        result = list(fasm.parse_fasm_filename(example('many.fasm')))
        check_round_trip(self, result)


if __name__ == '__main__':
    unittest.main()
