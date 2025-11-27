---
layout: post
title: "Figma MCP Setup Guide for Google Antigravity"
date: 2025-11-25 00:00:00 -0300
categories: [Tutorials]
tags: [agents, mcp, antigravity, figma, setup]
description: "A step-by-step guide to setting up the Figma MCP server on Google Antigravity, including critical fixes for local server configuration and stdio mode."
---

> **Future Compatibility**: This guide addresses current limitations with the Figma MCP server and Google Antigravity. Future updates to either the Figma MCP package or the IDE may resolve these issues, rendering this workaround unnecessary. Please check for native support or updated documentation before proceeding.
{: .prompt-info }

This guide details how to set up the Figma MCP server on Google Antigravity. This is a key enabler for the **"Vibe Coding"** workflow I described in [From Copy-Paste Hell to Vibe Coding]({% post_url 2025-11-20-mcp-feedback-automation %}), allowing your agent to "see" your designs and verify its own work.

Here are the critical fixes we discovered (local server, stdio mode, and silencing stdout pollution).

## Prerequisites

- **Node.js**: Version 18+ (verified with v24.11.1).
- **npm**: Installed with Node.js.
- **Antigravity**: Installed and configured.

## Step 1: Generate Figma Personal Access Token

1.  Log in to Figma in your browser.
2.  Go to **Settings** -> **Security**.
3.  Under **Personal Access Tokens**, click **Generate new token**.
4.  Name it (e.g., "Antigravity MCP") and ensure it has Files > **file_content:read**  permission.
5.  **Copy the token immediately**. You will need it later.

## Step 2: Install the MCP Server Package

Open your terminal in the Antigravity directory (or wherever you want the package to live) and install `figma-mcp-server`.

> Do **NOT** install `figma-developer-mcp`. It does not support the required `stdio` mode correctly for this setup. Use `figma-mcp-server`.
{: .prompt-danger }

```bash
npm install figma-mcp-server -g
```

## Step 3: Patch the Server (Critical)

The `figma-mcp-server` package prints a debug message to standard output on startup, which breaks the JSON communication protocol used by Antigravity. You must silence this.

1.  Locate the file `node_modules/figma-mcp-server/mcpServer.js`.
2.  Open it in a text editor.
3.  Find the line:
    ```javascript
    dotenv.config({ path: path.resolve(__dirname, ".env") });
    ```
4.  **Comment it out** by adding `//` at the beginning:
    ```javascript
    // dotenv.config({ path: path.resolve(__dirname, ".env") });
    ```
5.  Save the file.

## Step 4: Configure Antigravity

Open or create your `mcp_config.json` file and add the following configuration.

> You must use **absolute paths** for the `command`, `args`, and `PATH` to avoid "EOF" errors. Replace the paths below with the actual paths on your new computer.
{: .prompt-info }

```json
{
  "mcpServers": {
    "figma": {
      "command": "node",
      "args": [
        "/ABSOLUTE/PATH/TO/YOUR/node_modules/figma-mcp-server/mcpServer.js"
      ],
      "env": {
        "FIGMA_API_KEY": "YOUR_FIGMA_TOKEN_FROM_STEP_1"
      }
    }
  }
}
```

### Example Configuration

If your username is `jdoe`, it might look like this:

```json
{
  "mcpServers": {
    "figma": {
      "command": "node",
      "args": [
        "/home/jdoe/antigravity/node_modules/figma-mcp-server/mcpServer.js"
      ],
      "env": {
        "FIGMA_API_KEY": "figd_xxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

## Troubleshooting

- **EOF Error**: Usually means Antigravity can't find the `node` executable. Check your absolute paths and the `PATH` environment variable.
- **Invalid Character Error**: Usually means something is printing to stdout (like `dotenv`). Double-check Step 3.
- **Unauthorized**: Check your `FIGMA_API_KEY` in Step 4.

## Test Case: Frontend Mentor QR Code Component

I tested the Figma MCP by implementing the [Frontend Mentor QR Code Component](https://www.frontendmentor.io/challenges/qr-code-component-iux_sIO_H) using React and Tailwind CSS.

**Comparison:**

|               Figma Design                |        React Implementation         |
| :---------------------------------------: | :---------------------------------: |
| ![Figma Design](/assets/img/figma_design.png) | ![React App](/assets/img/react_app.png) |

**Result:**
The implementation closely matches the Figma design, demonstrating the effectiveness of using the Figma MCP to retrieve design details (colors, typography, spacing) directly within the IDE.
