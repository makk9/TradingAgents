#!/usr/bin/env python3
"""
Simple validation script for TradingAgents.
Catches real bugs without requiring external tools.
"""

import sys
import py_compile
import traceback
from pathlib import Path

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_header(text):
    print(f"\n{YELLOW}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    print(f"  {text}")

# Test 1: Syntax Check
def test_syntax():
    """Check Python syntax in all .py files."""
    print_header("Test 1: Syntax Validation")

    errors = []
    files_checked = 0

    tradingagents_dir = Path("tradingagents")

    for py_file in tradingagents_dir.rglob("*.py"):
        files_checked += 1
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            errors.append(f"{py_file}: {e}")

    if errors:
        print_error(f"Syntax errors in {len(errors)} file(s)")
        for error in errors:
            print_info(error)
        return False
    else:
        print_success(f"All {files_checked} files have valid syntax")
        return True

# Test 2: Core Imports
def test_core_imports():
    """Test that core modules can be imported."""
    print_header("Test 2: Core Module Imports")

    modules = [
        ("Trading Graph", "tradingagents.graph.trading_graph", "TradingAgentsGraph"),
        ("Agents", "tradingagents.agents", ""),
        ("Dataflows Config", "tradingagents.dataflows.config", "set_config"),
        ("Memory System", "tradingagents.agents.utils.memory", "FinancialSituationMemory"),
        ("LLM Clients", "tradingagents.llm_clients", "create_llm_client"),
    ]

    errors = []

    for name, module, cls in modules:
        try:
            mod = __import__(module, fromlist=[cls] if cls else [])
            if cls:
                getattr(mod, cls)
            print_success(f"{name} imports OK")
        except Exception as e:
            error_msg = f"{name}: {type(e).__name__}: {str(e)[:80]}"
            errors.append(error_msg)
            print_error(error_msg)

    return len(errors) == 0

# Test 3: Agent State Imports
def test_agent_states():
    """Test that agent state definitions are valid."""
    print_header("Test 3: Agent State Definitions")

    try:
        from tradingagents.agents.utils.agent_states import (
            AgentState,
            InvestDebateState,
            RiskDebateState,
        )
        print_success("AgentState imports OK")
        print_success("InvestDebateState imports OK")
        print_success("RiskDebateState imports OK")

        # Check that they're TypedDicts or dict-like
        if hasattr(AgentState, "__annotations__"):
            print_info(f"  AgentState has {len(AgentState.__annotations__)} fields")
        return True
    except Exception as e:
        print_error(f"Agent state error: {e}")
        traceback.print_exc()
        return False

# Test 4: Graph Setup
def test_graph_setup():
    """Test that graph setup components are importable."""
    print_header("Test 4: Graph Setup Components")

    components = [
        ("conditional_logic", "ConditionalLogic"),
        ("setup", "GraphSetup"),
        ("propagation", "Propagator"),
        ("reflection", "Reflector"),
        ("signal_processing", "SignalProcessor"),
    ]

    errors = []

    for module_name, class_name in components:
        try:
            module = __import__(
                f"tradingagents.graph.{module_name}",
                fromlist=[class_name]
            )
            cls = getattr(module, class_name)
            print_success(f"{class_name} imports OK")
        except Exception as e:
            error_msg = f"{class_name}: {type(e).__name__}"
            errors.append(error_msg)
            print_error(error_msg)

    return len(errors) == 0

# Test 5: Configuration
def test_config():
    """Test that default config is valid."""
    print_header("Test 5: Default Configuration")

    try:
        from tradingagents.default_config import DEFAULT_CONFIG

        required_keys = [
            "llm_provider",
            "deep_think_llm",
            "quick_think_llm",
            "max_debate_rounds",
            "data_vendors",
        ]

        missing = []
        for key in required_keys:
            if key in DEFAULT_CONFIG:
                print_success(f"Config has '{key}'")
            else:
                missing.append(key)
                print_error(f"Config missing '{key}'")

        return len(missing) == 0
    except Exception as e:
        print_error(f"Config error: {e}")
        return False

# Main validation runner
def main():
    print(f"\n{YELLOW}{'='*60}")
    print("TradingAgents Code Validation")
    print(f"{'='*60}{RESET}\n")

    tests = [
        ("Syntax Validation", test_syntax),
        ("Core Imports", test_core_imports),
        ("Agent States", test_agent_states),
        ("Graph Components", test_graph_setup),
        ("Configuration", test_config),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"{test_name} crashed: {e}")
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print_header("Validation Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test_name:<30} {status}")

    print(f"\n{total} test(s) run, {passed} passed, {total - passed} failed\n")

    if passed == total:
        print_success("All validations passed! Code is ready.\n")
        return 0
    else:
        print_error("Some validations failed. See above for details.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())