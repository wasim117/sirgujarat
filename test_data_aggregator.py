#!/usr/bin/env python3
"""
Tests for DataAggregator class - handling missing data scenarios.
"""

import sys
from gujarati_ocr_json_extractor import DataAggregator


def test_only_taluko_data():
    """Test that entries with only taluko data have None for gaam."""
    aggregator = DataAggregator()
    
    # Add only taluko data
    aggregator.add_taluko_entry("P0640001", "તાલુકો નામ")
    
    data = aggregator.get_aggregated_data()
    
    assert "P0640001" in data
    assert data["P0640001"]["taluko"] == "તાલુકો નામ"
    assert data["P0640001"]["gaam"] is None
    print("✓ Test passed: Only taluko data handled correctly")


def test_only_gaam_data():
    """Test that entries with only gaam data have None for taluko."""
    aggregator = DataAggregator()
    
    # Add only gaam data
    aggregator.add_gaam_entry("P0640002", "ગામ નામ")
    
    data = aggregator.get_aggregated_data()
    
    assert "P0640002" in data
    assert data["P0640002"]["taluko"] is None
    assert data["P0640002"]["gaam"] == "ગામ નામ"
    print("✓ Test passed: Only gaam data handled correctly")


def test_both_taluko_and_gaam_data():
    """Test that entries with both taluko and gaam data are stored correctly."""
    aggregator = DataAggregator()
    
    # Add both taluko and gaam data
    aggregator.add_taluko_entry("P0640003", "તાલુકો નામ")
    aggregator.add_gaam_entry("P0640003", "ગામ નામ")
    
    data = aggregator.get_aggregated_data()
    
    assert "P0640003" in data
    assert data["P0640003"]["taluko"] == "તાલુકો નામ"
    assert data["P0640003"]["gaam"] == "ગામ નામ"
    print("✓ Test passed: Both taluko and gaam data handled correctly")


def test_multiple_entries_with_mixed_data():
    """Test multiple entries with various combinations of missing data."""
    aggregator = DataAggregator()
    
    # Entry 1: Only taluko
    aggregator.add_taluko_entry("P0640001", "તાલુકો 1")
    
    # Entry 2: Only gaam
    aggregator.add_gaam_entry("P0640002", "ગામ 2")
    
    # Entry 3: Both
    aggregator.add_taluko_entry("P0640003", "તાલુકો 3")
    aggregator.add_gaam_entry("P0640003", "ગામ 3")
    
    data = aggregator.get_aggregated_data()
    
    # Verify all entries exist
    assert len(data) == 3
    
    # Verify entry 1 (only taluko)
    assert data["P0640001"]["taluko"] == "તાલુકો 1"
    assert data["P0640001"]["gaam"] is None
    
    # Verify entry 2 (only gaam)
    assert data["P0640002"]["taluko"] is None
    assert data["P0640002"]["gaam"] == "ગામ 2"
    
    # Verify entry 3 (both)
    assert data["P0640003"]["taluko"] == "તાલુકો 3"
    assert data["P0640003"]["gaam"] == "ગામ 3"
    
    print("✓ Test passed: Multiple entries with mixed data handled correctly")


def test_empty_string_handling():
    """Test that empty strings are stored correctly (not converted to None)."""
    aggregator = DataAggregator()
    
    # Add empty string for taluko
    aggregator.add_taluko_entry("P0640004", "")
    
    data = aggregator.get_aggregated_data()
    
    assert "P0640004" in data
    assert data["P0640004"]["taluko"] == ""
    assert data["P0640004"]["gaam"] is None
    print("✓ Test passed: Empty string handled correctly")


def run_all_tests():
    """Run all test cases."""
    print("Testing DataAggregator - Missing Data Scenarios")
    print("=" * 60)
    
    try:
        test_only_taluko_data()
        test_only_gaam_data()
        test_both_taluko_and_gaam_data()
        test_multiple_entries_with_mixed_data()
        test_empty_string_handling()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
