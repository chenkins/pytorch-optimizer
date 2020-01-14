import torch
import pytest
import torch_optimizer as optim


def assert_sparse_not_supported(optimizer_class, err_msg=None):
    param = torch.randn(1, 1).to_sparse().requires_grad_(True)
    grad = torch.randn(1, 1).to_sparse()
    param.grad = grad
    optimizer = optimizer_class([param])
    optimizer.zero_grad()
    with pytest.raises(RuntimeError) as ctx:
        optimizer.step()

    msg = err_msg or 'does not support sparse gradients'
    assert msg in str(ctx.value)


def test_sparse_not_supported():
    assert_sparse_not_supported(optim.DiffGrad)
    assert_sparse_not_supported(optim.AdaMod)
    assert_sparse_not_supported(optim.RAdam)