# Enable assertion rewriting from pytest
import pytest


pytest.register_assert_rewrite("crosswind.tests.support")
