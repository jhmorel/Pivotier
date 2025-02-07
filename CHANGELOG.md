# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.0.0] - 2025-02-06
### Added
- Enhanced "Align Cursor to Normal" to support multiple selections
- Added median normal calculation for multiple selected elements
- Position calculation now matches Blender's native "Cursor to Selected" behavior
- New preferences system with customizable settings:
  - Auto-Align on Selection toggle
  - Align to Active Object option
  - Preserve Original Location setting
  - Coordinate Space selection (Global/Local/Cursor)
- Added preset system for saving and loading preference configurations
- Custom keymap preferences integration
- **Batch Operations**:
  - Batch align for multiple objects
  - Support for different orientation modes (Global, Local, Cursor)
  - Alignment based on active object as reference
- **Enhanced Set Pivot to Base**:
  - Support for multiple object selection
  - Respects default orientation settings
  - Smart pivot placement based on object type
- **Improved Object Alignment**:
  - Support for different coordinate spaces
  - Enhanced alignment accuracy with active object
  - Better handling of object hierarchies

### Changed
- Updated cursor position calculation to use vertex median instead of element centers
- Improved normal vector calculation to use weighted average of selected elements
- Restructured addon to use modular architecture
- Enhanced object transformation handling for better precision
- Improved pivot point calculations across different object types
- Better integration with Blender's native transformation system
- Optimized performance for operations with multiple objects

### Fixed
- Fixed preferences visibility issue in Blender's addon preferences
- Corrected bl_idname to properly match addon's module name
- Improved stability when working with multiple objects
- Fixed orientation issues in different coordinate spaces
- Better error handling for edge cases

## [v1.1.0] - 2024-08-23
### Added
- **Align View to Cursor**: Aligns the 3D view to the 3D cursor, allowing for quick focus on the cursor's position.

## [v1.0.1] - 2024-08-02
### Changed
- Renamed the sidebar tab in Blender's viewport from "Tools" to "Pivotier".

## [v1.0.0] - 2024-07-30
### Added
- Initial release of Pivotier.
- **align_cursor_to_normal**: Aligns the 3D cursor to the normal of the selected face, edge or vertex.
- **align_object_to_cursor**: Aligns the selected object to the 3D cursor.
- **set_pivot_to_base**: Sets the pivot point to the base of the selected object.
- **set_pivot_to_cursor**: Sets the pivot point to the location and orientation of the 3D cursor.
Support for Blender 4.0, 4.1 and 4.2. Testing on earlier versions.
