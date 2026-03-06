# Testing & Validation Guide

This document outlines how to test and validate changes to the TradingAgents codebase without running the entire system.

## Current State

As noted in CLAUDE.md:
> "There is no automated test suite (pytest/unittest), linting configuration, or CI/CD pipeline."

However, there are several lightweight validation approaches available.

---

## 1. Syntax & Import Validation (Built-in, No Install Needed)

### Option A: Python Compile Check
**Fastest, zero overhead**

```bash
python -m py_compile tradingagents/graph/trading_graph.py
```

Checks for syntax errors without running the code. Works on individual files or entire directories:

```bash
python -m py_compile tradingagents/
```

### Option B: Module Import Check
**Validates syntax + finds import errors**

```bash
python -c "from tradingagents.graph.trading_graph import TradingAgentsGraph; print('✓ Import successful')"
```

Good for catching:
- Syntax errors
- Missing imports
- Circular dependencies
- Unresolved module references

### Option C: AST Analysis
**Parses code structure without executing**

```bash
python -c "import ast; ast.parse(open('tradingagents/graph/trading_graph.py').read()); print('✓ Valid Python')"
```

Useful for:
- Deep syntax validation
- Finding undefined variables
- Checking code structure

---

## 2. Functional Validation (Lightweight)

### test.py Script
**Existing test file in repo**

```bash
python test.py
```

Tests yfinance technical indicator retrieval. Good for:
- Verifying data flow still works
- Checking external API connections
- Integration with data vendors

Run after changes to data tools, vendoring, or indicators:
```bash
python test.py
```

### main.py Example
**Programmatic flow test**

```bash
python main.py
```

Runs a complete analysis flow (requires API keys in `.env`). Good for:
- End-to-end testing
- Verifying graph orchestration
- Checking agent outputs

---

## 3. Type Checking (Optional, Can Install)

### Option A: Mypy (Lightweight)
```bash
pip install mypy
mypy tradingagents/graph/trading_graph.py
```

Checks for type annotation violations without running code.

### Option B: Pyright (More Strict)
```bash
pip install pyright
pyright tradingagents/graph/trading_graph.py
```

More thorough type checking.

---

## 4. Code Quality Tools (Optional)

### Black (Code Formatting)
```bash
pip install black
black --check tradingagents/  # Check without modifying
black tradingagents/           # Auto-format
```

### Ruff (Linting)
```bash
pip install ruff
ruff check tradingagents/
```

Much faster than pylint/flake8. Can auto-fix many issues:
```bash
ruff check --fix tradingagents/
```

---

## 5. Testing Framework (Optional, For Real Tests)

### Pytest
```bash
pip install pytest
pytest tests/  # Run all tests
pytest tests/test_agents.py -v  # Verbose
```

Currently no tests exist, but you could add:
```python
# tests/test_trading_graph.py
import pytest
from tradingagents.graph.trading_graph import TradingAgentsGraph

def test_initialization():
    """Test that TradingAgentsGraph initializes without errors."""
    ta = TradingAgentsGraph(selected_analysts=["market"])
    assert ta.reflector is not None
    assert ta.graph is not None
```

---

## Recommended Workflow for Code Changes

After making changes, run these in order (no installs required):

### Level 1: Quick Syntax Check (5 seconds)
```bash
python -m py_compile tradingagents/
```

### Level 2: Import Check (10 seconds)
```bash
python -c "from tradingagents.graph.trading_graph import TradingAgentsGraph; print('✓')"
```

### Level 3: Module Specific Test (if applicable)
For data-related changes:
```bash
python test.py
```

For full pipeline changes:
```bash
python main.py  # Requires .env with API keys
```

### Level 4: Optional—Install Tools for Extra Checks

For larger refactors, consider installing:
```bash
pip install ruff mypy  # Total size: ~100MB, quick install

ruff check tradingagents/
mypy tradingagents/
```

---

## Quick Command Reference

| Task | Command | Time | Install? |
|------|---------|------|----------|
| Check syntax | `python -m py_compile tradingagents/` | 1s | No |
| Check imports | `python -c "from tradingagents.graph.trading_graph import TradingAgentsGraph"` | 2s | No |
| Test data flow | `python test.py` | 5-10s | No |
| Full end-to-end | `python main.py` | 30s-5m | No |
| Type check | `pip install mypy && mypy tradingagents/` | 10s | Yes |
| Lint code | `pip install ruff && ruff check tradingagents/` | 5s | Yes |

---

## CI/CD Setup (Future)

If you want to set up automated testing on git push, consider:

1. **GitHub Actions** (if on GitHub)
   - Free for public repos
   - Can run syntax checks, type checking, tests on every commit
   - Example: `.github/workflows/test.yml`

2. **Pre-commit hooks** (local)
   - Run checks before commit
   - Install: `pip install pre-commit`
   - Configure: `.pre-commit-config.yaml`

3. **Simple Makefile** (local)
   ```makefile
   validate:
   	python -m py_compile tradingagents/
   	python test.py

   check: validate
   	pip install ruff mypy
   	ruff check tradingagents/
   	mypy tradingagents/

   test: check
   	python main.py
   ```

---

## Validation After Recent Memory System Changes

The memory system disable was validated with:

```bash
# 1. Syntax check
python -m py_compile tradingagents/graph/trading_graph.py

# 2. Import check
python -c "from tradingagents.graph.trading_graph import TradingAgentsGraph; print('✓ Imports work')"

# 3. Verify method is callable
python -c "
from tradingagents.graph.trading_graph import TradingAgentsGraph
ta = TradingAgentsGraph.__new__(TradingAgentsGraph)
ta.reflect_and_remember(1000)  # Should not error
print('✓ reflect_and_remember() is callable (no-op)')
"
```

All checks passed ✓

---

## Recommendations

1. **Immediately available (no install):**
   - Always run `python -m py_compile` after changes
   - Use `python -c "from module import X"` to validate imports
   - Run `python test.py` for data-related changes

2. **Quick install (recommended):**
   - Install `ruff` for linting (1 tool covers 10 others)
   - Install `mypy` for type checking
   - Both are fast and useful

3. **Not needed unless you have many test files:**
   - pytest (for comprehensive test suites)
   - Full CI/CD pipeline (add when codebase stabilizes)

---

## Additional Resources

- [Python ast module](https://docs.python.org/3/library/ast.html)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [Mypy handbook](https://mypy.readthedocs.io/)
- [pytest docs](https://docs.pytest.org/)