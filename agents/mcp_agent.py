#!/usr/bin/env python3
"""
MCP Agent - zarządza połączeniami MCP
"""

import asyncio
from typing import Dict, List
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)


class MCPAgent:
    """Agent do zarządzania połączeniami i komunikacją MCP"""
    
    def __init__(self):
        self.mcp_server = StdioServerParameters(
            command="python3",
            args=["mcp_server_minesweeper.py"]
        )
        self.connection_pool = []
        logger.info("🔧 MCPAgent initialized")
    
    async def list_tools(self) -> Dict:
        """Lista dostępnych narzędzi MCP"""
        logger.info("🔍 Listing MCP tools")
        
        try:
            async with stdio_client(self.mcp_server) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    
                    tools_list = [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "input_schema": tool.inputSchema
                        }
                        for tool in tools.tools
                    ]
                    
                    return {
                        "status": "success",
                        "agent": "mcp",
                        "tools": tools_list,
                        "count": len(tools_list)
                    }
        except Exception as e:
            logger.error("❌ Error listing tools: %s", e)
            return {
                "status": "error",
                "agent": "mcp",
                "error": str(e)
            }
    
    async def list_resources(self) -> Dict:
        """Lista dostępnych zasobów MCP"""
        logger.info("📚 Listing MCP resources")
        
        try:
            async with stdio_client(self.mcp_server) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    resources = await session.list_resources()
                    
                    resources_list = [
                        {
                            "uri": resource.uri,
                            "name": resource.name,
                            "description": getattr(resource, 'description', None)
                        }
                        for resource in resources.resources
                    ]
                    
                    return {
                        "status": "success",
                        "agent": "mcp",
                        "resources": resources_list,
                        "count": len(resources_list)
                    }
        except Exception as e:
            logger.error("❌ Error listing resources: %s", e)
            return {
                "status": "error",
                "agent": "mcp",
                "error": str(e)
            }
    
    async def get_server_info(self) -> Dict:
        """Pobierz informacje o serwerze MCP"""
        logger.info("ℹ️  Getting MCP server info")
        
        try:
            async with stdio_client(self.mcp_server) as (read, write):
                async with ClientSession(read, write) as session:
                    init_result = await session.initialize()
                    
                    tools = await session.list_tools()
                    resources = await session.list_resources()
                    
                    return {
                        "status": "success",
                        "agent": "mcp",
                        "server_info": {
                            "protocol_version": init_result.protocolVersion,
                            "capabilities": init_result.capabilities,
                            "tools_count": len(tools.tools),
                            "resources_count": len(resources.resources)
                        }
                    }
        except Exception as e:
            logger.error("❌ Error getting server info: %s", e)
            return {
                "status": "error",
                "agent": "mcp",
                "error": str(e)
            }
    
    async def health_check(self) -> Dict:
        """Sprawdź health MCP servera"""
        try:
            result = await self.get_server_info()
            
            if result["status"] == "success":
                return {
                    "status": "ok",
                    "protocol_version": result["server_info"]["protocol_version"]
                }
            else:
                return {
                    "status": "error",
                    "error": result.get("error", "Unknown error")
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
