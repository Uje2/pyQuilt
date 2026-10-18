from scripts.registry import register

# ---- widgets (all live in scripts/widgets.py) ----
register("widget.Label",          "scripts.widgets:Label")
register("widget.TextBox",        "scripts.widgets:TextBox")
register("widget.Button",         "scripts.widgets:Button")
register("widget.RectedButton",   "scripts.widgets:RectedButton")
register("widget.Button2",        "scripts.widgets:Button2")
register("widget.Slider",         "scripts.widgets:Slider")
register("widget.VerticalSlider", "scripts.widgets:VerticalSlider")
register("widget.Table",          "scripts.widgets:Table")
register("widget.Custom_Table",   "scripts.widgets:Custom_Table")
register("widget.Dialog",         "scripts.widgets:Dialog")
register("widget.TitleBar",       "scripts.widgets:TitleBar")
register("widget.Dummy",          "scripts.widgets:Dummy")

# ---- new widgets (also in scripts/widgets.py) ----
register("widget.Checkbox",     "scripts.widgets:Checkbox")
register("widget.ProgressBar",  "scripts.widgets:ProgressBar")
register("widget.ToggleSwitch", "scripts.widgets:ToggleSwitch")
register("widget.ImageWidget",  "scripts.widgets:ImageWidget")
register("widget.Panel",        "scripts.widgets:Panel")
register("widget.Dropdown",     "scripts.widgets:Dropdown")

# ---- abilities ----
register("ability.ShinraTensei", "scripts.ability:ShinraTensei")
register("ability.Turrent",      "scripts.ability:Turrent")

# ---- entities ----
register("entity.force", "scripts.entities:PhysicsEntity")