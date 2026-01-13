"""
Test script for Collection Outliner
Run this in Blender's Python console to test the integration
"""

import bpy
import sys

def test_registration():
    """Test that all operators are registered"""
    print("\n=== Testing Registration ===")
    
    operators_to_check = [
        "qpanels_assets.collection_outliner",
        "qpanels_assets.outliner_set_active_collection",
        "qpanels_assets.outliner_expand_all",
        "qpanels_assets.outliner_expand_sublevel",
        "qpanels_assets.outliner_select_collection_objects",
        "qpanels_assets.outliner_toggle_exclude",
        "qpanels_assets.outliner_toggle_select",
        "qpanels_assets.outliner_toggle_hide",
        "qpanels_assets.outliner_toggle_disable",
        "qpanels_assets.outliner_toggle_render",
        "qpanels_assets.outliner_toggle_holdout",
        "qpanels_assets.outliner_toggle_indirect",
        "qpanels_assets.outliner_remove_collection",
    ]
    
    all_ok = True
    for op_name in operators_to_check:
        if hasattr(bpy.ops.qpanels_assets, op_name.split(".")[-1]):
            print(f"✓ {op_name}")
        else:
            print(f"✗ {op_name} NOT FOUND")
            all_ok = False
    
    return all_ok


def test_property_group():
    """Test that property group is registered"""
    print("\n=== Testing Property Group ===")
    
    try:
        cm = bpy.context.scene.collection_manager
        print(f"✓ Scene.collection_manager exists")
        print(f"  - show_exclude: {cm.show_exclude}")
        print(f"  - show_selectable: {cm.show_selectable}")
        print(f"  - show_hide_viewport: {cm.show_hide_viewport}")
        print(f"  - cm_list_index: {cm.cm_list_index}")
        return True
    except AttributeError as e:
        print(f"✗ Property group not found: {e}")
        return False


def test_internals():
    """Test internal state management"""
    print("\n=== Testing Internals ===")
    
    try:
        # Add path if needed
        import sys
        addon_path = r"c:\Users\lcara\Documents\GitHub\QPanels-Core\qpanel-assets"
        if addon_path not in sys.path:
            sys.path.insert(0, addon_path)
        
        from outliner import internals
        
        print(f"✓ internals module imported")
        print(f"  - layer_collections: {type(internals.layer_collections)}")
        print(f"  - collection_tree: {type(internals.collection_tree)}")
        print(f"  - expanded: {type(internals.expanded)}")
        print(f"  - rto_history keys: {list(internals.rto_history.keys())}")
        return True
    except Exception as e:
        print(f"✗ Internals test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tree_building():
    """Test collection tree building"""
    print("\n=== Testing Tree Building ===")
    
    try:
        from outliner import internals
        
        # Build tree
        internals.update_collection_tree(bpy.context)
        
        print(f"✓ Tree built successfully")
        print(f"  - Total collections: {len(internals.layer_collections)}")
        print(f"  - Max tree level: {internals.max_lvl}")
        print(f"  - Top-level collections: {len(internals.collection_tree)}")
        
        # Print tree structure
        print("\n  Collection hierarchy:")
        for laycol in internals.collection_tree:
            print(f"    {'  ' * laycol['lvl']}{laycol['name']} (lvl {laycol['lvl']})")
            print_children(laycol, 1)
        
        return True
    except Exception as e:
        print(f"✗ Tree building failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_children(laycol, depth):
    """Recursively print collection children"""
    for child in laycol.get("children", []):
        print(f"    {'  ' * (depth + child['lvl'])}{child['name']} (lvl {child['lvl']})")
        print_children(child, depth + 1)


def test_invoke_popup():
    """Test invoking the main popup"""
    print("\n=== Testing Popup Invocation ===")
    
    try:
        # This should show the popup
        result = bpy.ops.qpanels_assets.collection_outliner('INVOKE_DEFAULT')
        print(f"✓ Popup invoked: {result}")
        return True
    except Exception as e:
        print(f"✗ Popup invocation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("="*50)
    print("Collection Outliner - Test Suite")
    print("="*50)
    
    results = {
        "Registration": test_registration(),
        "Property Group": test_property_group(),
        "Internals": test_internals(),
        "Tree Building": test_tree_building(),
        "Popup Invocation": test_invoke_popup(),
    }
    
    print("\n" + "="*50)
    print("Test Results Summary")
    print("="*50)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n{passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️ Some tests failed. Check output above for details.")


# Run tests when executed
if __name__ == "__main__":
    run_all_tests()
