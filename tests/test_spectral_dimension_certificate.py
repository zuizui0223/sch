import pytest

from scripts.spectral_dimension_certificate import certify_dimension_from_curvature_spectrum


def test_dimension_one_rejected_by_second_mode_above_error():
    out = certify_dimension_from_curvature_spectrum(
        [4.0, 0.8, 0.1],
        registered_dimension=1,
        operator_error_bound=0.25,
    )
    assert out.registered_dimension_rejected
    assert out.certified_min_dimension == 2
    assert out.next_eigenvalue == pytest.approx(0.8)


def test_dimension_two_compatible_when_third_mode_below_error():
    out = certify_dimension_from_curvature_spectrum(
        [4.0, 0.8, 0.1],
        registered_dimension=2,
        operator_error_bound=0.25,
    )
    assert not out.registered_dimension_rejected
    assert out.certified_min_dimension == 2
    assert out.frobenius_rank_d_residual == pytest.approx(0.1)


def test_zero_error_recovers_exact_rank_lower_bound_for_psd_spectrum():
    out = certify_dimension_from_curvature_spectrum(
        [3.0, 1.0, 0.0, 0.0],
        registered_dimension=1,
        operator_error_bound=0.0,
    )
    assert out.certified_min_dimension == 2
    assert out.registered_dimension_rejected


def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError):
        certify_dimension_from_curvature_spectrum(
            [1.0, 2.0],
            registered_dimension=1,
            operator_error_bound=0.1,
        )
    with pytest.raises(ValueError):
        certify_dimension_from_curvature_spectrum(
            [1.0],
            registered_dimension=1,
            operator_error_bound=-0.1,
        )
