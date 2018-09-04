from __future__ import absolute_import, unicode_literals

from barril.units.unit_rich_text_representations import UnitRichTextRepresentations


def AssertRTFCaption(received_representation, expected_caption):
    html_mask = UnitRichTextRepresentations.HTML_TEXT_MASK
    assert received_representation == \
        html_mask % expected_caption

def testUnitRichTextRepresentations():

    # Some unit representation should be initially set
    expected_units_initially_set = [
        ('m3', 'm<sup>3</sup>'),
        ('m3/d', 'm<sup>3</sup>/d'),
        ('m3/m3', 'm<sup>3</sup>/m<sup>3</sup>'),
    ]

    # Testing the default values
    for unit, expected_representation in expected_units_initially_set:
        stored_representation = UnitRichTextRepresentations.GetUnitHtmlRepresentation(unit)
        AssertRTFCaption(stored_representation, expected_representation)

    # If not found the representation in defaults, returns the unit
    unknown_unit_caption = 'unknown_unit'
    unknown_unit_representation = UnitRichTextRepresentations.GetUnitHtmlRepresentation(unknown_unit_caption)
    assert unknown_unit_representation == unknown_unit_caption

    # It should be possible to set the rich text representation units
    new_unit = 'new_unit'
    new_unit_representation = 'new<sup>unit</sup>'

    UnitRichTextRepresentations.DEFAULT_UNITS_RICH_TEXT_REPRESENTATIONS[new_unit] = new_unit_representation
    AssertRTFCaption(
        UnitRichTextRepresentations.GetUnitHtmlRepresentation(new_unit),
        new_unit_representation
    )

    # But the user should be able to overwrite the default values with a custom representation
    new_cubic_meter_representation = 'm<sub>3</sub>'
    cubic_meter_caption = 'm3'
    UnitRichTextRepresentations.DEFAULT_UNITS_RICH_TEXT_REPRESENTATIONS[cubic_meter_caption] = new_cubic_meter_representation

    AssertRTFCaption(
        UnitRichTextRepresentations.GetUnitHtmlRepresentation(cubic_meter_caption),
        new_cubic_meter_representation
    )
