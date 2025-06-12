# Swagger MCP

Automatically convert a Swagger/OpenAPI specification into an MCP server for use with Windsurf, Cursor, or other tools.

## Quickstart

Install from PyPI using `pipx` (recommended):

```bash
brew install pipx
pipx ensurepath
pipx install --force swagger-mcp
```

Alternatively, install from source:

```bash
git clone https://github.com/khengyun/swagger-mcp.git
cd swagger-mcp
pipx install -e . --force
```

Confirm the installation succeeded:

```bash
which swagger-mcp
which swagger-mcp-sample-server
```

Spin up a sample "products and product categories" API on your local machine on port 9000:

```bash
swagger-mcp-sample-server
```

Visit <http://localhost:9000/docs> to confirm the sample server is running.

We'll use this sample server to show how to configure an MCP server in Windsurf. Make sure the sample server is running before following the Windsurf or Cursor instructions below.

## Swagger MCP UI

You can manage multiple Swagger MCP servers through a small web UI. Start the UI server:

```bash
swagger-mcp-ui
```

Open <http://localhost:8000> in your browser. Use the form to add a server by providing a name, the OpenAPI spec URL or path, and optionally a server URL. Running servers are listed on the page and can be stopped individually.

## Windsurf

Start an MCP Server in Windsurf (`Windsurf Settings -> Settings -> Windsurf Settings -> Cascade -> Add Server -> Add Custom Server`):

```json
{
  "mcpServers": {
    "product-mcp": {
      "command": "swagger-mcp",
      "args": [
        "--spec",
        "http://localhost:9000/openapi.json",
        "--name",
        "Product MCP",
        "--server-url",
        "http://localhost:9000"
      ]
    }
  }
}
```

That's it! Your API is now accessible through Windsurf, Cursor, or other tools as a set of AI-friendly tools. Ask your AI agent to list, create, update, and delete products and categories.

### Demo

## Cursor (>=v0.46)

Support for Cursor is still in beta as Cursor MCP integration matures. Windsurf is currently the preferred experience.

```json
{
  "mcpServers": {
    "product mcp": {
      "command": "swagger-mcp",
      "args": [
        "--spec",
        "http://localhost:9000/openapi.json",
        "--name",
        "Product MCP",
        "--server-url",
        "http://localhost:9000",
        "--cursor"
      ]
    }
  }
}
```

**Please Note:** In Cursor, you may need to replace the command `swagger-mcp` with the full path to the `swagger-mcp` executable (`which swagger-mcp`). Also note the `--cursor` flag. This is for Cursor compatibility. MCP integration is currently in beta in Cursor as of v0.46 and may not work as expected. Currently, Windsurf is a better experience in general.

See other examples in **Other Fun Servers**.

## Additional Options

You can pass a JSON file, YAML file, or URL for the `--spec` option:

```
/path/to/openapi.json
/path/to/openapi.yaml
https://api.example.com/openapi.json
```

Filter endpoints: Only include endpoints where the path matches the regex pattern:

```json
{
  "mcpServers": {
    "product mcp": {
      "command": "swagger-mcp",
      "args": [
        "--spec",
        "http://localhost:9000/openapi.json",
        "--name",
        "product-mcp",
        "--server-url",
        "http://localhost:9000",
        "--include-pattern",
        "category"
      ]
    }
  }
}
```

Filter endpoints: Exclude endpoints where the path matches the regex pattern:

```json
{
  "mcpServers": {
    "product mcp": {
      "command": "swagger-mcp",
      "args": [
        "--spec",
        "http://localhost:9000/openapi.json",
        "--name",
        "product-mcp",
        "--server-url",
        "http://localhost:9000",
        "--exclude-pattern",
        "product"
      ]
    }
  }
}
```

### Authentication

```json
{
  "mcpServers": {
    "product mcp": {
      "command": "swagger-mcp",
      "args": [
        "--spec",
        "http://localhost:9000/openapi.json",
        "--name",
        "product-mcp",
        "--server-url",
        "http://localhost:9000",
        "--bearer-token",
        "your-token-here"
      ]
    }
  }
}
```

### Custom headers

```json
{
  "mcpServers": {
    "product mcp": {
      "command": "swagger-mcp",
      "args": [
        "--spec",
        "http://localhost:9000/openapi.json",
        "--name",
        "product-mcp",
        "--server-url",
        "http://localhost:9000",
        "--header",
        "X-Some-Header:your-value",
        "--header",
        "X-Some-Other-Header:your-value"
      ]
    }
  }
}
```

### Server URLs

If the OpenAPI spec already contains a specific server URL, you don't have to provide it as a command line argument. But if you do, the command line `--server-url` overrides all endpoints.

### Constant Values

If you want to always automatically provide a value for a parameter, you can use the `--const` option. You can include as many `--const` options as you need.

```json
{
  "mcpServers": {
    "product mcp": {
      "command": "swagger-mcp",
      "args": [
        "--spec",
        "http://localhost:9000/openapi.json",
        "--name",
        "product-mcp",
        "--server-url",
        "http://localhost:9000",
        "--const",
        "parameter-name:your-value",
        "--const",
        "parameter-name2:your-value2"
      ]
    }
  }
}
```

## Supported Features

- All HTTP methods (GET, POST, PUT, DELETE, etc.)
- Path parameters
- Query parameters
- Textual Multi-Part Request Body Fields
- JSON Request body
- Bearer Token Authentication
- Custom Headers
- Constant Values

## Limitations

- Endpoints that have recursive schema references are not yet supported.
- Cursor MCP integration is very early and frankly broken.
- We will never support automatic OAuth workflow execution. If the OAuth workflow creates a bearer token, you must obtain this token yourself and provide it as a command line argument.
- We do not support Swagger/OpenAPI specifications spread across multiple files.
- We do not support path variable substitution in server URLs (but we do support path variables in endpoints).
- In general, we do not support all Swagger/OpenAPI features. The Swagger/OpenAPI standard is vast, and support for more obscure features will be added as needed.

## Help

If you have trouble spinning up a server, try the following command:

```bash
REAL_LOGGER=true swagger-mcp-parse-dry-run ...
```

Include this information in any issue you file. If you find a Swagger API specification that is not supported and you can't use any of the available parameters for a workaround, please file an issue.

## Roadmap

- Support recursive schema references
- Support path variable substitution in server URLs
- Revamp the `--cursor` mode to better work around Cursor's limitations
- Provide support for MCP resources

## Command Line Options

- `--spec` (required): Path or URL to your OpenAPI/Swagger specification
- `--name` (required): Name for your MCP server
- `--server-url`: Base URL for API calls (overrides servers defined in spec)
- `--bearer-token`: Bearer token for authenticated requests
- `--additional-headers`: JSON string of additional headers to include in all requests
- `--include-pattern`: Regex pattern to include only specific endpoint paths (e.g., `/api/v1/.*`)
- `--exclude-pattern`: Regex pattern to exclude specific endpoint paths (e.g., `/internal/.*`)
- `--header`: `key:value` pair of an extra header to include with all requests. Can be included multiple times.
- `--const`: `key:value` pair of a constant value to always use for a parameter. Can be included multiple times.
- `--cursor`: Run in cursor mode

### Authentication Examples

```json
{
  "mcpServers": {
    "product mcp": {
      "command": "swagger-mcp",
      "args": [
        "--spec",
        "http://localhost:9000/openapi.json",
        "--name",
        "product-mcp",
        "--server-url",
        "http://localhost:9000",
        "--bearer-token",
        "your-token-here",
        "--cursor"
      ]
    }
  }
}
```

```json
{
  "mcpServers": {
    "product mcp": {
      "command": "swagger-mcp",
      "args": [
        "--spec",
        "http://localhost:9000/openapi.json",
        "--name",
        "product-mcp",
        "--server-url",
        "http://localhost:9000",
        "--header",
        "X-API-Key:your-key",
        "--cursor"
      ]
    }
  }
}
```

## Other Fun Servers

### Countries

```json
{
  "mcpServers": {
    "countries": {
      "command": "swagger-mcp",
      "args": [
        "--spec",
        "https://restcountries.com/openapi/rest-countries-3.1.yml",
        "--name",
        "countries",
        "--server-url",
        "https://restcountries.com/",
        "--const",
        "fields:name",
        "--cursor"
      ]
    }
  }
}
```

TODO: PokeAPI

TODO: Slack

TODO: Petstore

## For Developers

### Installation

For development, install with development dependencies:

```bash
# Clone the repository
git clone https://github.com/context-labs/swagger-mcp.git
cd swagger-mcp

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

For a global installation on your local machine, use:

```bash
bash scripts/install-global.sh
```

### Unit Tests

```bash
pytest swagger_mcp/tests/unit -v
```

### Integration Tests

```bash
pytest swagger_mcp/tests/integration -v --capture=no --log-cli-level=INFO
```

### MCP Inspector (For interactive exploration of the MCP Server)

You'll have to do a global installation of your latest code first (`bash scripts/install-global.sh`), then you can run the inspector script.

You'll see the server type STDIO and the command `swagger-mcp` pre-filled.

```bash
bash scripts/inspector.sh
```

Click "Connect" and then "List Tools" to begin interacting with your MCP Server.

### Logging

To run the server with logs enabled, set the `REAL_LOGGER` environment variable to `true`:

```bash
REAL_LOGGER=true swagger-mcp --spec http://localhost:9000/openapi.json --name product-mcp --server-url http://localhost:9000
```
