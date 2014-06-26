"""Tests for the extractoutput preprocessor"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from .base import PreprocessorTestsBase
from ..extractoutput import ExtractOutputPreprocessor


class TestExtractOutput(PreprocessorTestsBase):
    """Contains test functions for extractoutput.py"""


    def build_preprocessor(self):
        """Make an instance of a preprocessor"""
        preprocessor = ExtractOutputPreprocessor()
        preprocessor.extract_output_types = {'text/plain', 'image/png', 'application/pdf'}
        preprocessor.enabled = True
        return preprocessor


    def test_constructor(self):
        """Can a ExtractOutputPreprocessor be constructed?"""
        self.build_preprocessor()
    

    def test_output(self):
        """Test the output of the ExtractOutputPreprocessor"""
        nb = self.build_notebook()
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)

        # Check if text was extracted.
        output = nb.cells[0].outputs[1]
        assert 'text/plain_filename' in output
        text_filename = output['text/plain_filename']

        # Check if png was extracted.
        output = nb.cells[0].outputs[6]
        assert 'image/png_filename' in output
        png_filename = output['image/png_filename']
        
        # Check that pdf was extracted
        output = nb.cells[0].outputs[7]
        assert 'application/pdf_filename' in output
        pdf_filename = output['application/pdf_filename']

        # Verify text output
        assert text_filename in res['outputs']
        self.assertEqual(res['outputs'][text_filename], b'b')

        # Verify png output
        assert png_filename in res['outputs']
        self.assertEqual(res['outputs'][png_filename], b'g')

        # Verify pdf output
        assert pdf_filename in res['outputs']
        self.assertEqual(res['outputs'][pdf_filename], b'h')
