<p align="center">
  <img src="Pivotier_Banner.png" alt="Banner Image" />
</p>

## Pivotier

**Author:** Javier Hernández Morel

**Collaborator:** Eniel Rodríguez Machado,

Special thanks to **Eniel**, Senior Developer and close friend, whose expertise and guidance have been invaluable throughout the development of Pivotier.

### Description

Pivotier is a Blender addon that offers tools to enhance and streamline your workflow for object alignment and pivot point management. It includes utilities to easily align objects and the cursor to specific positions and orientations, making it essential for 3D artists and designers.

### Features

- **Align Cursor to Normal**: Aligns the 3D cursor to the median normal of selected faces, edges, or vertices. Supports multiple selections with smart position calculation that matches Blender's native behavior.
- **Align Object to Cursor**: Aligns the selected object to the 3D cursor, with support for multiple objects and different coordinate spaces.
- **Batch Operations**: Perform alignment operations on multiple objects at once, with support for different orientation modes and active object as reference.
- **Set Pivot to Base**: Sets the pivot point to the base of selected objects. Supports multiple selections and respects orientation settings.
- **Set Pivot to Cursor**: Sets the pivot point to the location and orientation of the 3D cursor.
- **Align View to Cursor**: Aligns the 3D view to the 3D cursor, allowing for quick focus on the cursor's position.

### Key Benefits

- **Smart Multi-Selection**: Most operations support working with multiple objects or elements at once
- **Flexible Orientations**: Work in Global, Local, or Cursor space according to your needs
- **Enhanced Precision**: Improved calculations for better accuracy in all operations
- **Native Integration**: Behavior that matches and enhances Blender's native functionality

### Preferences and Configuration

The addon includes a comprehensive preferences system that allows you to customize its behavior:

- **Auto-Align on Selection**: Automatically align objects when selection changes
- **Align to Active Object**: Use the active object as reference for alignment
- **Preserve Original Location**: Keep original object location when aligning rotation
- **Coordinate Space**: Choose between Global, Local, or Cursor space for operations
- **Custom Keymaps**: Enable and customize keyboard shortcuts
- **Preset System**: Save and load your preferred configurations

### Installation

1. Download the latest release of the addon from the [Releases](https://github.com/jhmorel/Pivotier/releases) page.
2. In Blender, go to `Edit > Preferences > Add-ons`.
3. Click `Install...` and select the downloaded ZIP file.
4. Enable the addon by checking the box next to "Pivotier".
5. Configure your preferences by clicking the dropdown arrow next to the addon.

### Usage

Once installed, the tools provided by Pivotier can be accessed through:
- The `Object` menu in the 3D Viewport
- The Pivotier panel in the sidebar (N-panel)
- Custom keyboard shortcuts (if enabled in preferences)

The addon's behavior can be customized through the preferences panel, where you can also save your preferred configurations as presets.

For batch operations:
1. Select multiple objects (the active object will be used as reference if specified in preferences)
2. Choose your desired operation from the Pivotier panel
3. The operation will be applied to all selected objects respecting the current coordinate space and alignment settings

### About the Addon

This addon was designed for my personal convenience, primarily to streamline processes when modeling environments. It may contain bugs, and I would greatly appreciate if you could report them as we are actively working on fixing them and adding new features as they arise.

This is a free-to-use tool, and I hope it proves useful. If you'd like to support me as a 3D artist, you can do so on Ko-fi: [ko-fi.com/jhmorel](https://ko-fi.com/jhmorel).

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.
