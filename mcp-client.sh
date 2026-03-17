#!/bin/bash
# MCP Client Helper Script
# 用于调用 xiaohongshu-mcp HTTP 服务

MCP_URL="http://localhost:18060/mcp"
SESSION_ID=""

# 初始化会话
init_session() {
    local response=$(curl -s -X POST "$MCP_URL" \
        -H "Content-Type: application/json" \
        -d '{
            "jsonrpc":"2.0",
            "id":1,
            "method":"initialize",
            "params":{
                "protocolVersion":"2024-11-05",
                "capabilities":{},
                "clientInfo":{"name":"xhs-publisher","version":"1.0"}
            }
        }')
    echo "$response" >&2

    # 发送 initialized 通知
    curl -s -X POST "$MCP_URL" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' > /dev/null
}

# 调用 MCP 工具
call_tool() {
    local tool_name="$1"
    local arguments="$2"

    if [ -z "$arguments" ]; then
        arguments="{}"
    fi

    local response=$(curl -s -X POST "$MCP_URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"jsonrpc\":\"2.0\",
            \"id\":2,
            \"method\":\"tools/call\",
            \"params\":{
                \"name\":\"$tool_name\",
                \"arguments\":$arguments
            }
        }")

    echo "$response"
}

# 主逻辑
case "$1" in
    init)
        init_session
        ;;
    call)
        if [ -z "$2" ]; then
            echo "Usage: $0 call <tool_name> [arguments_json]"
            exit 1
        fi
        call_tool "$2" "$3"
        ;;
    *)
        echo "Usage: $0 {init|call <tool_name> [arguments_json]}"
        exit 1
        ;;
esac
