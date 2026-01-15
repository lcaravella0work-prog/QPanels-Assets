# Outliner Collection Manager - ARCHIVED

**Status**: Non-functional, archived as of v2.1.6 (2026-01-15)

## Why Archived?

The Outliner Collection Manager (v2.1.5) was an advanced panel system with:
- Collection management
- Layer visibility controls  
- Custom operators

**Problem**: Complex implementation incompatible with QPanels Core auto-registration system.

## What Replaced It?

v2.1.6 restored **19 functional panels** from QPanels v5.4.0:
- ✅ 11 Properties panels (armature, camera, mesh, etc.)
- ✅ 7 Space panels (graph editor, node editor, etc.)
- ✅ 1 Basic outliner panel (outliner.py)

## Git History

- **Branch**: `archive/outliner-v2.1.5-non-functional`
- **Last working commit**: `99fbf1d`
- **Files removed**:
  - `panels/outliner/__init__.py`
  - `panels/outliner/ui.py`
  - `panels/outliner/operators.py`
  - `panels/outliner/operator_utils.py`
  - `panels/outliner/internals.py`
  - `panels/outliner/test_outliner.py`
  - `panels/outliner/README.md`

## Recovery Instructions

If needed, restore from Git:

```bash
git checkout 99fbf1d -- panels/outliner/
```

## Replacement Strategy

Future outliner enhancements should:
1. Use simplified single-file architecture (like `outliner.py`)
2. Follow auto-registration pattern in `panels/__init__.py`
3. Test integration with QPanels Core before release

## Related Issues

- Complexity: 2,383 lines of code in 7 files
- Registration: Failed to auto-discover with `discover_modules()`
- Testing: Insufficient integration testing with QPanels Core

## Version Timeline

- **v2.1.0-v2.1.5**: Outliner Collection Manager (non-functional)
- **v2.1.6**: Restored v5.4.0 functional panels
- **Future**: Simplified outliner enhancements TBD
