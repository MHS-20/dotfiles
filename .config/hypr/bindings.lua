-- Keep only your personal keybinding overrides here. Add new bindings or
-- unbind defaults before replacing them.

-- See current bindings and descriptions:
--   omarchy menu keybindings --print

-- To disable every Omarchy default binding, set this in
-- ~/.config/hypr/hyprland.lua before require("default.hypr.omarchy"), then add
-- only the bindings you want below:
--   omarchy_default_bindings = false

-- To disable all preinstalled app/webapp bindings, set:
--   omarchy_preinstalled_bindings = false

-- Add a new binding.
-- o.bind("SUPER + SHIFT + R", "SSH", "alacritty -e ssh your-server")

-- Change an existing binding by unbinding it first, then binding the key again.
-- This example changes SUPER+SPACE from the launcher to the Omarchy root menu.
-- hl.unbind("SUPER + SPACE")
-- o.bind("SUPER + SPACE", "Omarchy menu", "omarchy-menu toggle root")

-- Disable a default binding without replacing it.
-- hl.unbind("SUPER + SHIFT + B")

-- Logitech MX Keys examples:
-- o.bind("SUPER + SHIFT + S", nil, "omarchy-capture-screenshot")
-- o.bind("SUPER + H", nil, "voxtype record toggle")
-- o.bind("SUPER + PERIOD", nil, "omarchy-shell shell toggle omarchy.emojis")

-- SUPER + B: launch Brave directly (SUPER + B was unbound by default;
-- SUPER + SHIFT + B still opens the system default browser)
o.bind("SUPER + B", "Browser (Brave)", { launch = "brave" })

-- SUPER + Q closes the window instead of SUPER + W.
-- Unbind default SUPER + W (was: Close window)
hl.unbind("SUPER + W")
o.bind("SUPER + Q", "Close window", hl.dsp.window.close())

-- SUPER + E: open file manager (SUPER + E was unbound by default;
-- SUPER + SHIFT + F still opens it too)
o.bind("SUPER + E", "File manager", { omarchy = "nautilus" })

-- SUPER + N opens the editor (neovim) instead of SUPER + SHIFT + N.
-- SUPER + SHIFT + N now opens the browser in incognito/private mode.
-- Unbind default SUPER + SHIFT + N (was: Editor)
hl.unbind("SUPER + SHIFT + N")
o.bind("SUPER + N", "Editor", { omarchy = "editor" })
o.bind("SUPER + SHIFT + N", "Browser (private)", { omarchy = "browser --private" })
