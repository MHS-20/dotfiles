-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

local keymap = vim.keymap.set
local opts = { noremap = true, silent = true }

-- Insert mode
keymap("i", "jk", "<ESC>", opts)

-- Terminal
-- keymap("n", "<leader>tt", "<cmd>terminal<CR>", { desc = "Open terminal" })
keymap("n", "<leader>tt", function()
  Snacks.terminal.toggle()
end, { desc = "Toggle terminal" })

-- Splits
keymap("n", "<leader>sv", "<C-w>v", { desc = "Split window vertically" })
keymap("n", "<leader>sx", "<cmd>close<CR>", { desc = "Close split" })

-- Tabs (old)
-- keymap("n", "<leader>to", "<cmd>tabnew<CR>", { desc = "Open new tab" })
-- keymap("n", "<leader>tn", "<cmd>tabnext<CR>", { desc = "Next tab" })
-- keymap("n", "<leader>tp", "<cmd>tabprevious<CR>", { desc = "Previous tab" })
-- keymap("n", "<leader>tx", "<cmd>tabclose<CR>", { desc = "Close tab" })

-- Quit
keymap("n", "<leader>q", "<cmd>qa<CR>", { desc = "Quit" })

-- LazyGit
keymap("n", "<leader>gg", "<cmd>LazyGit<CR>", { desc = "LazyGit" })

-- Tabs
keymap("n", "<leader>to", "<cmd>tabnew<CR>", { desc = "Open new tab" })

-- Find files (Telescope)
-- keymap("n", "<leader>ff", "<cmd>Telescope find_files<CR>", { desc = "Find files" })

-- File explorer (Neo-tree)
-- keymap("n", "<leader>e", "<cmd>Neotree toggle<CR>", { desc = "Toggle explorer" })

-- Save
keymap("n", "<leader>w", "<cmd>w<CR>", { desc = "Save file" })

-- Yank all
vim.keymap.set("n", "<leader>aa", 'ggVG"+y', {
  desc = "Yank entire file to clipboard",
})
