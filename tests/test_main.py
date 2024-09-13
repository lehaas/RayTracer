import io
from raytracer.definitions.vector import Color, Vector
from raytracer.raytracer import output_ppm


def test_output_ppm():
    """Test that output_ppm returns a valid ppm file."""
    out = io.StringIO()
    output_ppm(out, height=1, width=2, func=lambda i, j: Color(Vector([0, 0, 0])))

    assert out.getvalue() == f"P3\n2 1\n255\n{0} {0} {0}\n{0} {0} {0}\n"


def test_output_ppm_w_function(mocker):
    """Test that output_ppm returns a valid ppm file."""
    with mocker.patch("raytracer.color.linear_to_gamma", side_effect=lambda x: x):
        out = io.StringIO()
        output_ppm(
            out,
            height=2,
            width=3,
            func=lambda c, r: Color(Vector([0.1 * c, 0.2 * r, 0])),
        )

        assert (
            out.getvalue()
            == f"""P3\n3 2\n255\n{0} {0} {0}\n{25} {0} {0}\n{51} {0} {0}\n{0} {51} {0}\n{25} {51} {0}\n{51} {51} {0}\n"""
        )
