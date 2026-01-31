#!/usr/bin/env python3
"""
Build House Example

This example uses the SketchUp MCP `eval_ruby` API to create a simple
house model with walls, a gable roof, and two window frames.

Requirements: SketchUp with the MCP server running and reachable via
`mcp.client.Client("sketchup")`.
"""

import json
import logging
from mcp.client import Client

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BuildHouseExample")

RUBY_CODE = """
model = Sketchup.active_model
entities = model.active_entities

# House dimensions (in SketchUp units)
width = 400
depth = 300
height = 200
roof_h = 100

# Create main house group (walls)
house = entities.add_group
he = house.entities

# Base rectangle and extrude to create walls
p1 = [0, 0, 0]
p2 = [width, 0, 0]
p3 = [width, depth, 0]
p4 = [0, depth, 0]
base_face = he.add_face(p1, p2, p3, p4)
base_face.pushpull(height)

# Create a simple gable roof as a separate group
roof = entities.add_group
re = roof.entities

a = [0, 0, height]
b = [width, 0, height]
c = [width, depth, height]
d = [0, depth, height]
# Ridge points (along X axis, centered in Y)
r1 = [0, depth / 2.0, height + roof_h]
r2 = [width, depth / 2.0, height + roof_h]

# Two sloped faces
re.add_face(d, c, r2, r1)
re.add_face(a, b, r2, r1)

# Create two simple window frames on the front wall (y = 0)
# Window 1
w1 = he.add_group
we1 = w1.entities
wf1 = we1.add_face([50, -2, 80], [110, -2, 80], [110, -2, 140], [50, -2, 140])
wf1.pushpull(4)

# Window 2
w2 = he.add_group
we2 = w2.entities
wf2 = we2.add_face([250, -2, 80], [310, -2, 80], [310, -2, 140], [250, -2, 140])
wf2.pushpull(4)

# Return the created house group's entity ID as a string
house.entityID.to_s
"""


def main():
    client = Client("sketchup")
    if not client.is_connected:
        logger.error("Failed to connect to the SketchUp MCP server.")
        return

    logger.info("Connected to SketchUp MCP server. Sending build-house Ruby code...")
    response = client.eval_ruby(code=RUBY_CODE)

    try:
        result = json.loads(response)
        if result.get("success"):
            logger.info(f"House created. Result: {result.get('result')}")
        else:
            logger.error(f"SketchUp error: {result.get('error')}")
    except json.JSONDecodeError:
        logger.error(f"Failed to parse response from MCP: {response}")


if __name__ == "__main__":
    main()
