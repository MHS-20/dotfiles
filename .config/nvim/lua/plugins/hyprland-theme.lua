return {
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "tokyonight",
    },
  },
  {
    "folke/tokyonight.nvim",
    opts = {
      style = "night",
      on_colors = function(colors)
        colors.bg = "#11111b"
        colors.bg_dark = "#0d0d17"
        colors.bg_float = "#1a1b26"
        colors.bg_highlight = "#1e1e2e"
        colors.bg_popup = "#1a1b26"
        colors.bg_search = "#33ccff"
        colors.bg_sidebar = "#11111b"
        colors.bg_statusline = "#11111b"
        colors.bg_visual = "#1e3348"
        colors.border = "#33ccff"
        colors.blue = "#33ccff"
        colors.blue0 = "#2ec6f0"
        colors.blue1 = "#33ccff"
        colors.blue2 = "#5ed0f2"
        colors.blue5 = "#66d4ff"
        colors.blue6 = "#33ccff"
        colors.blue7 = "#2ec6f0"
        colors.comment = "#565f89"
        colors.cyan = "#2ec6f0"
        colors.dark3 = "#1e1e2e"
        colors.dark5 = "#313244"
        colors.green = "#00ff99"
        colors.green1 = "#4dffaa"
        colors.green2 = "#5affb3"
        colors.hint = "#2ec6f0"
        colors.info = "#33ccff"
        colors.magenta = "#cba6f7"
        colors.orange = "#e5c07b"
        colors.purple = "#bb9af7"
        colors.purple1 = "#cba6f7"
        colors.red = "#f38ba8"
        colors.teal = "#00ff99"
        colors.warning = "#e5c07b"
        colors.yellow = "#e5c07b"
      end,
    },
  },
}
