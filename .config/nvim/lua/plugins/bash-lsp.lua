return {
  {
    "mason-org/mason.nvim",
    opts = { ensure_installed = { "bash-language-server", "shellcheck" } },
  },
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        bashls = {},
      },
    },
  },
}
