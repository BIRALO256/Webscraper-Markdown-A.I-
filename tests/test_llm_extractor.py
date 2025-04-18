from processor.llm_extractor import extract_fields


def test_extract_fields_returns_string():
    result = extract_fields('Hello world', ['field'])
    assert isinstance(result, str)