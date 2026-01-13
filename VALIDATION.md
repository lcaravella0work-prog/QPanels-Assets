# QPanel Outliner - Validation Checklist

## Pre-Testing Setup
- [ ] Files are in correct location: `qpanel-assets/`
- [ ] All Python files have proper imports
- [ ] version.json is valid JSON
- [ ] No QCD code remains
- [ ] No Disable Objects operators present

## Code Structure
- [ ] All operators renamed from CM* to QPOutliner*
- [ ] All bl_idname changed from view3d.* to qpanel_outliner.*
- [ ] internals.py classes renamed:
  - [ ] CMListCollection → QPOutlinerListCollection
  - [ ] CMSendReport → QPOutlinerSendReport
  - [ ] CMUISeparatorButton → QPOutlinerUISeparatorButton
- [ ] No references to `persistent_data`
- [ ] No references to `qcd_collection_state`
- [ ] No references to `QCDSlots`

## Operators (32 total)
- [ ] SetActiveCollection
- [ ] ExpandAllOperator
- [ ] ExpandSublevelOperator
- [ ] QPOutlinerExcludeOperator
- [ ] QPOutlinerUnExcludeAllOperator
- [ ] QPOutlinerRestrictSelectOperator
- [ ] QPOutlinerUnRestrictSelectAllOperator
- [ ] QPOutlinerHideOperator
- [ ] QPOutlinerUnHideAllOperator
- [ ] QPOutlinerDisableViewportOperator
- [ ] QPOutlinerUnDisableViewportAllOperator
- [ ] QPOutlinerDisableRenderOperator
- [ ] QPOutlinerUnDisableRenderAllOperator
- [ ] QPOutlinerHoldoutOperator
- [ ] QPOutlinerUnHoldoutAllOperator
- [ ] QPOutlinerIndirectOnlyOperator
- [ ] QPOutlinerUnIndirectOnlyAllOperator
- [ ] QPOutlinerNewCollectionOperator
- [ ] QPOutlinerRemoveCollectionOperator
- [ ] QPOutlinerRemoveEmptyCollectionsOperator
- [ ] QPOutlinerSelectCollectionObjectsOperator
- [ ] SelectAllCumulativeObjectsOperator
- [ ] QPOutlinerSendObjectsToCollectionOperator
- [ ] QPOutlinerPhantomModeOperator
- [ ] QPOutlinerApplyPhantomModeOperator
- [ ] QPOutlinerUndoWrapper
- [ ] QPOutlinerRedoWrapper

## UI Classes (4 total)
- [ ] QPanelOutliner (main panel)
- [ ] QPO_UL_items (list view)
- [ ] QPOutlinerDisplayOptionsPanel
- [ ] SpecialsMenu

## Data Classes (2 total)
- [ ] QPOutlinerListCollection
- [ ] QPOutlinerSendReport
- [ ] QPOutlinerUISeparatorButton

## Registration
- [ ] outliner/__init__.py registers all classes
- [ ] Scene.qpanel_outliner property registered
- [ ] qpanel-assets/__init__.py imports outliner
- [ ] get_custom_panels() returns correct dict

## Runtime Testing
- [ ] Panel opens without errors
- [ ] Collections display in tree view
- [ ] Expand/collapse works
- [ ] Set active collection works
- [ ] Select objects works
- [ ] Send objects to collection works
- [ ] All RTOs toggle correctly:
  - [ ] Exclude
  - [ ] Select
  - [ ] Hide
  - [ ] Disable
  - [ ] Render
  - [ ] Holdout
  - [ ] Indirect
- [ ] Global RTOs work
- [ ] Add collection works
- [ ] Add subcollection works
- [ ] Remove collection works
- [ ] Rename collection works
- [ ] Phantom mode works
- [ ] Undo/Redo works
- [ ] Display options panel works
- [ ] Specials menu works
- [ ] Remove empty collections works

## Integration Testing
- [ ] Loads correctly in QPanel
- [ ] get_custom_panels() called successfully
- [ ] No conflicts with other panels
- [ ] Unloads cleanly

## Error Handling
- [ ] No console errors on load
- [ ] No console errors during operation
- [ ] Graceful handling of edge cases
- [ ] Proper error messages to user

## Performance
- [ ] Tree view updates smoothly
- [ ] No lag with many collections
- [ ] Efficient filtering

## Final Checks
- [ ] All TODO/placeholder code removed
- [ ] Code follows Blender addon conventions
- [ ] Proper tooltips on all operators
- [ ] Proper labels on all UI elements
- [ ] No debug print statements

## Sign-Off
- [ ] Code review complete
- [ ] All tests passed
- [ ] Ready for production
