import pytest


def value(w1: float, w2: float) -> float:
    return 4.0 * w1 * w2 / (w1 + w2)


def optimizer(w1: float, w2: float) -> float:
    return 2.0 * w2 / (w1 + w2)


def value_gradient(w1: float, w2: float) -> tuple[float, float]:
    total = w1 + w2
    return (
        4.0 * w2 * w2 / (total * total),
        4.0 * w1 * w1 / (total * total),
    )


def inverse_loss_map(loss1: float, loss2: float) -> float:
    # loss1=z^2 and loss2=(z-2)^2 imply loss1-loss2=4z-4.
    return (loss1 - loss2 + 4.0) / 4.0


def test_value_gradient_equals_exposed_functional_loss_vector():
    w1, w2 = 3.0, 2.0
    z = optimizer(w1, w2)
    grad = value_gradient(w1, w2)
    assert grad[0] == pytest.approx(z * z)
    assert grad[1] == pytest.approx((z - 2.0) ** 2)


def test_injective_loss_pair_recovers_optimized_phenotype():
    for w1, w2 in [(1.0, 1.0), (3.0, 2.0), (0.5, 4.0)]:
        z = optimizer(w1, w2)
        loss1, loss2 = value_gradient(w1, w2)
        assert inverse_loss_map(loss1, loss2) == pytest.approx(z)


def test_value_matches_weighted_exposed_loss():
    w1, w2 = 2.0, 5.0
    loss1, loss2 = value_gradient(w1, w2)
    assert value(w1, w2) == pytest.approx(w1 * loss1 + w2 * loss2)
