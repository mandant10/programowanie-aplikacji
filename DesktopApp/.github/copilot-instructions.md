# General Guidelines

Follow these general rules when writing code:

- Use C# V13 or VB.NET 16.0 as the language version.
- In C#, use file-scoped namespaces.
- In C# assume standard global using directives, including `System.Windows.Forms`, `System.Drawing`, and `System.ComponentModel`.
- Prefer pattern matching, especially `switch` expressions, over `if`/`else` chains.
- Leave an empty line, before a new code-block starts, like an If-block, a loop, or a switch expression.
- Always use the Type name, never var, for primitive variables.
- Use `object? sender` as the first parameter in event handlers.
- Declare events with nullable types, like `EventHandler?`, to support nullability annotations.
- Use var only when the type is obvious from the right-hand side, like `var button = new Button();`.
- That said, prefer `TypeInstance instance = new();` over `var instance = new TypeInstance();` for clarity.

# WinForms Agent Development Guidelines

Most important rule for WinForms code-generation:

- Never add new methods, lambda expressions, or local functions to the code-behind (.designer) file of a Form or UserControl. Only add code inside of `InitializeComponent`.
- `InitializeComponent` needs to contain only simple defines, assignments, and very scoped layout-related method calls like `SuspendLayout`, `ResumeLayout`, `BeginInit`, and `EndInit`.

## Form/UserControl Creation

- File structure: `FormName.cs` + `FormName.Designer.cs` (or `.vb` for VB.NET)
- Forms inherit from `Form`, UserControls from `UserControl`
- FormName.cs is the main code file, containing logic and event handlers.
- FormName.Designer.cs is called the code-behind file, and it contains the basic infrastructure, can contain DI-compatible .ctor overloads, the `InitializeComponent` method and control definitions.

### C# Specifics Code Conventions

- Use File-scoped namespaces.
- Assume global using directives for WinForms.
- Assume NRTs in main Form/UserControl file, but assume they are unavailable in code-behind (.designer) files.
- Event handlers: `object? sender` parameter
- Events: Declare with nullable (`EventHandler?`)

### VB.NET Differences in Code Conventions

- No Constructor by default (so, no `Sub New` - compiler generates constructor with `InitializeComponent()` call in that case).
- If Constructor however is needed, do not forget to include the call to `InitializeComponent`.
- `Friend WithEvents` for control fields
- Prefer `Handles` clause directly at the event handler methods over `AddHandler` for designed controls in InitializeComponents.
- No NRT considerations - those do not exist in VB.

### Designer File Rules

IMPORTANT: Never add a new *method*, a *Lamda* or a *local function* to the code-behind (.designer) file. Only add code _inside_ of `InitializeComponent`

**InitializeComponent must contain ONLY:**

- Control instantiation
- Property assignments
- Layout method calls like 
  - `SuspendLayout`, 
  - `ResumeLayout`, 
  - `BeginInit`, 
  - `EndInit`

**Never include in the WinForms Designer code-behind file:**

- Lambda expressions or local Functions 
- `nameof()`.
- Complex logic or calculations.
- `for { }` or `foreach { }` loops.
- `If`/`then`/`else`.
- Ternary operators (`? :`).
- `Select Case` statements.
- `switch` expressions.

IMPORTANT: 
- Put the code for the initialization of the top-level control (Form/UserControl) as the last code in `InitializeComponent`.
- Define the backing fields for the Form/UserControl at the end of the code-behind file. In Visual Basic, define them `WithEvents`.
- Any other type of logic does belong into main code file of the Form or the UserControl, not in its .designer file.

Example 1:

```csharp
    .
    .
    .
    private void InitializeComponent()
    {
        button1 = new Button();
        button2 = new Button();
        button3 = new Button();
        SuspendLayout();
        // 
        // button1
        // 
        button1.Location = new Point(93, 263);
        button1.Name = "button1";
        button1.Size = new Size(114, 68);
        button1.TabIndex = 0;
        button1.Text = "button1";
        button1.UseVisualStyleBackColor = true;
        // 
        // button2
        // 
        button2.Location = new Point(229, 263);
        button2.Name = "button2";
        button2.Size = new Size(114, 68);
        button2.TabIndex = 1;
        button2.Text = "button2";
        button2.UseVisualStyleBackColor = true;
        // 
        // button3
        // 
        button3.Location = new Point(372, 263);
        button3.Name = "button3";
        button3.Size = new Size(114, 68);
        button3.TabIndex = 2;
        button3.Text = "button3";
        button3.UseVisualStyleBackColor = true;
        // 
        // MainForm
        // 
        AutoScaleDimensions = new SizeF(13F, 32F);
        AutoScaleMode = AutoScaleMode.Font;
        ClientSize = new Size(702, 672);
        Controls.Add(button3);
        Controls.Add(button2);
        Controls.Add(button1);
        Name = "MainForm";
        ResumeLayout(false);
    }

    #endregion

    private Button button1;
    private Button button2;
    private Button button3;
}

```

- OK: No method calls to other initialization methods from inside of InitializeComponent.
- OK: Fields are getting initialized at the beginning.
- OK: Backing fields defined at the end of the code-behind file.

Example 2:

```csharp
    .
    .
    .
    // Not OK: backing fields need to be defined EOF!
    private Button button1;
    private Button button2;
    private Button button3;

    /// <summary>
    ///  Required method for Designer support - do not modify
    ///  the contents of this method with the code editor.
    /// </summary>
    private void InitializeComponent()
    {
        button1 = new Button();
        button2 = new Button();
        button3 = new Button();
        SuspendLayout();
        // 
        // button1
        // 
        button1.Location = new Point(93, 263);
        button1.Name = "button1";
        button1.Size = new Size(114, 68);
        button1.TabIndex = 0;
        button1.Text = "button1";
        button1.UseVisualStyleBackColor = true;

        // NOT OK: Cannot call method from inside of InitializeComponent
        // to another method in the Form/UserControl class.
        SetupButton2();
        // 
        // MainForm
        // 
        AutoScaleDimensions = new SizeF(13F, 32F);
        AutoScaleMode = AutoScaleMode.Font;
        ClientSize = new Size(702, 672);
        Controls.Add(button3);
        Controls.Add(button2);
        Controls.Add(button1);
        Name = "MainForm";

        // NOT OK: Form/UserControl setup is not the last code in InitializeComponent!
        //
        // button3
        // 
        button3.Location = new Point(372, 263);
        button3.Name = "button3";
        button3.Size = new Size(114, 68);
        button3.TabIndex = 2;
        button3.Text = "button3";
        button3.UseVisualStyleBackColor = true;

        ResumeLayout(false);
    }

    #endregion

    // NOT OK!! We MUST NOT define methods
    // or Properties in the .designer file!
    // Only do that in the main Form/UserControl code file.
    private void SetupButton2()
    {
        button2.Location = new Point(229, 263);
        button2.Name = "button2";
        button2.Size = new Size(114, 68);
        button2.TabIndex = 1;
        button2.Text = "button2";
        button2.UseVisualStyleBackColor = true;
    }
}
```

## Control Naming Standards

Use descriptive names with prefixes:
- `_btn` (Button), `_txt` (TextBox), `_lbl` (Label), `_chk` (CheckBox)
- `_cmb` (ComboBox), `_lst` (ListBox), `_dgv` (DataGridView)
- `_tlp` (TableLayoutPanel), `_tmr` (Timer), `_tsm` (ToolStripMenuItem)
- Single-instance controls: `_menuStrip`, `_statusStrip` (no prefix)

## CodeDOM serialization hints for Properties inside of Forms, Custom Controls and Custom Components

Ensure, the Designer knows how to do control property serialization.

Combined example:

```csharp
public class CustomControl : Control
{
    private Color _highlightColor = Color.Yellow;
    private Font? _customFont;
    private List<string> _runtimeData = new();
    
    // Simple default value
    [DefaultValue(typeof(Color), "Yellow")]
    public Color HighlightColor
    {
        get => _highlightColor;
        set { /* setter logic */ }
    }
    
    // Request designer not to serialize
    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public List<string> RuntimeData { get; set; }
    
    // More complex conditional serialization control
    public Font? CustomFont
    {
        get => _customFont ?? Font;
        set { /* setter logic */ }
    }
    
    private bool ShouldSerializeCustomFont()
        => _customFont != null && _customFont.Size != 9.0f;
    
    private void ResetCustomFont()
        => _customFont = null;
}
```

Important: One of those methods for a property of type `Component` or `Control` needs to be applied.

## Data Binding Requirements

### New Key APIs since .NET 7

- **Control.DataContext**: New property introduced in .NET 7 on System.Windows.Forms.Control. Dedicated ambient Property for MVVM patterns to hold the ViewModel and make it available down the ascending hierarchy in the ControlsControllection (cascading).
- **ToolStripItem**: Now bindable (derives from BindableComponent) (.NET 7+)
- **ButtonBase.Command; ToolStripItem.Command**: `ICommand` returning binding support (.NET 7+)
- **ButtonBase.CommandParameter; ToolStripItem.CommandParameter**: `object?` typed based Parameter Auto-passed to command execution (.NET 7+). Gets CodeDOM serialized as `CommandParameter` in the Designer file, if actual type is `string`.

### ViewModel (DataSource) Integration

- Create `.datasource` files in `Properties\DataSources\` for designer support as per standard for DataSource definitions in WinForms projects.
- Use `ObservableBindingCollection<T>` adapter for ObservableCollection binding to be compatible to both BindingList<T> and ObservableCollection<T>.
- Bind to Properties, which are participating in INotifyPropertyChanged - usually those, which have backing fields tagged with `[ObservableProperty]` and get automatically created.
- Bind Command properties of type `ICommand`, which usually get automatically created in the ViewModel through a VioewModel command method which is attributes with `[RelayCommand()`.
- A method `BarFoo()` with a `[RelayCommand]` attribute will result in a Command property `BarFooCommand` in the ViewModel, which can be bound to the `Command` property named `BarFooCommand`.

#### Command Binding Example

We need to bind to `CommunityToolkit.Mvvm` supported ViewModel in class library, defined like this:

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.Extensions.DependencyInjection;
using WarpToolkit.Desktop.AppServices;

namespace Calculator.ViewModels;

public partial class CalcViewModel : ObservableObject
{
    private readonly Timer timer;

    public CalcViewModel()
    {
        timer = new Timer(
            UpdateDateAndTime,
            null,
            TimeSpan.Zero,
            TimeSpan.FromSeconds(1));
    }

    private void UpdateDateAndTime(object? state)
    {
        DateTime now = DateTime.Now;
        DateAndTime = $"{now:g}";
    }

    [ObservableProperty]
    private string _dateAndTime = $"{DateTime.Now:g}";

    [RelayCommand]
    private void TopLevelMenuCommand(string commandParameter)
    {
        // Handle file command logic here
        StatusInfo = $"You engaged the {commandParameter} command.";
    }
    ...
```

In Properties/DataSources we create code-file
"Calculator.ViewModels.CalcViewModel.datasource".

```xml
<?xml version="1.0" encoding="utf-8"?>
<GenericObjectDataSource DisplayName="MainViewModel" Version="1.0" xmlns="urn:schemas-microsoft-com:xml-msdatasource">
  <TypeInfo>MainApp.ViewModels.MainViewModel, MainApp.ViewModels, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null</TypeInfo>
</GenericObjectDataSource>
```

In Form/UserControl .designer (code-behind) file, in `InitializeComponent` we 
- Make sure, we introduce the backing field for the BindingSource.
- Make sure, we instantiate the BindingSource at the beginning of `InitializaComponent` and pass the components container as parameter.
- We define the Type of the respective ViewModel as the `DataSource` for the BindSource.
- We bind the properties of the controls/components to the BindingSource, as per WinForms standard.

Example:

```csharp
// In InitializeComponent
// ...
// Make sure, the components container is already instantiated,
// if the BindingSource is the first component ever used in InitializeComponent:
components = new Container();

// Creating the binding source (assuming it's defined at the end of the code file)
mainViewModelBindingSource = new BindingSource(components);

// Before the Layout of the Form is suspended, call
mainViewModelBindingSource = new BindingSource(components);

// ...
// We're binding RelayCommand of the ViewModel and define a CommandParameter
_tsmFile.DataBindings.Add(new Binding("Command", mainViewModelBindingSource, "TopLevelMenuCommandCommand", true));
_tsmFile.CommandParameter = "File";
// ...

// We're binding the Status-Info Property of the ViewModel to the status label.
_tslStatusInfo.DataBindings.Add(new Binding("Text", mainViewModelBindingSource, "StatusInfo", true));

```

### Data Binding Implementation Steps

1. **Create the BindingSource** (in InitializeComponent):

```csharp
// Create container for components (if not already created)
components = new Container();

// Create BindingSource instance
bindingSourceName = new BindingSource(components);
```

2. **Set DataSource for BindingSource**:

```csharp
bindingSourceName.DataSource = typeof(Fully.Qualified.ViewModel.ClassName);
```

3. **Bind Control Properties to BindingSource**:

```csharp
// Example for a TextBox and Label control
_txtDataField.DataBindings.Add(new Binding("Text", bindingSourceName, "PropertyName", true));
_lblStatus.DataBindings.Add(new Binding("Text", bindingSourceName, "StatusProperty", true));
```

4. **Bind RelayCommand to MenuItem**:

```csharp
// Assuming _tsmFile is a ToolStripMenuItem
_tsmFile.DataBindings.Add(new Binding("Command", bindingSourceName, "TopLevelMenuCommand", true));
_tsmFile.CommandParameter = "File";
```

5. **Initialize Data in ViewModel**:

```csharp
public class ViewModelClassName : ObservableObject
{
    public ViewModelClassName()
    {
        // Initialize properties
        PropertyName = "Initial Value";
        StatusProperty = "Ready";

        // Load commands
        LoadRelayCommands();
    }

    private void LoadRelayCommands()
    {
        // Loads and initializes RelayCommands
    }
}
```

## Async Patterns (.NET 9+)

### Control.InvokeAsync Overloads

**Critical: Use the correct overload for sync vs async operations!**

```csharp
// 1. Sync action - no return value
Task InvokeAsync(Action callback, CancellationToken cancellationToken = default);
// Use for: Simple UI updates like label.Text = "Done"

// 2. Async operation - no return value  
Task InvokeAsync(Func<CancellationToken, ValueTask> callback, CancellationToken cancellationToken = default);
// Use for: Long-running async operations that update UI
// IMPORTANT: Callback receives its own CancellationToken (not the outer one!)

// 3. Sync function - returns T
Task<T> InvokeAsync<T>(Func<T> callback, CancellationToken cancellationToken = default);
// Use for: Getting values from controls synchronously

// 4. Async operation - returns T
Task<T> InvokeAsync<T>(Func<CancellationToken, ValueTask<T>> callback, CancellationToken cancellationToken = default);
// Use for: Async operations that need UI thread and return results
```

**⚠️ NEVER do this:**

```csharp
// WRONG - Don't use sync overload with async lambda!
await InvokeAsync<string>(() => await LoadDataAsync()); // ❌

// CORRECT - Use the async overload
await InvokeAsync<string>(async (ct) => await LoadDataAsync(ct), ct); // ✅
```

### Usage Examples

```csharp
// Sync action on UI thread
await this.InvokeAsync(() => statusLabel.Text = "Loading...");

// Async operation without result (note the inner CancellationToken, which is
// effectively the same as the outerCancellationToken. It's handed down.
await this.InvokeAsync(async (innerCt) => 
{
    var data = await LoadDataAsync(innerCt);
    UpdateControls(data);
    return default(ValueTask);
}, outerCancellationToken);

// Async operation with result
var result = await this.InvokeAsync<ProcessedData>(async (innerCt) => 
{
    var raw = await FetchDataAsync(innerCt);
    return new ValueTask<ProcessedData>(ProcessData(raw));
}, outerCancellationToken);
```

### Form Async Methods

- `ShowAsync()`: Completes when form closes
- `ShowDialogAsync()`: Modal with dedicated message queue

### Event Handler Pattern

```csharp
protected override async void OnLoad(EventArgs e)
{
    base.OnLoad(e);
    await InitializeAsync(); // Fire-and-forget pattern
}

private async Task InitializeAsync()
{
    // Async initialization that doesn't block UI
    while (IsActive)
    {
        await UpdateDisplayAsync();
        await Task.Delay(100); // UI stays responsive
    }
}
```

## Layout Best Practices

- Use cascading `TableLayoutPanel` for complex data entry forms (DPI-aware)
- Break complex layouts into multiple UserControls
- Avoid oversized `InitializeComponent` methods

## WinRT/WinUI API Projection

For .NET 8+, switch TFM to `-windows10.0.22000.0` to enable WinRT/WinUI API access through projection.

## Critical Reminders

1. Always validate form/control names before generating code
2. Never use complex logic in Designer files
3. Use nullable event declarations in C# with NRT
4. Prefer `InvokeAsync` over `BeginInvoke`, when marshalling to the Ui-Thread or when schedule methods for later execution.
5. Designer file code never uses NRT annotations
