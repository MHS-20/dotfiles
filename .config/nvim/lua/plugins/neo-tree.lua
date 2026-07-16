return {
  "nvim-neo-tree/neo-tree.nvim",
  opts = function(_, opts)
    -- We modify the opts table that LazyVim already created
    opts.window = opts.window or {}
    opts.window.width = 15 -- Set your desired width here
  end,
}
