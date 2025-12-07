from app.controllers.compressor import Compressor, Header


def test_gen_header():
    compressor = Compressor()
    header = Header(table={"a": 2, "b": 3, "c": 4}, file_name="test_file.txt")
    header = compressor.gen_header_data(header)
    expect_header = "vct@@test_file.txt///a=2,b=3,c=4@@vct"
    assert header == expect_header
