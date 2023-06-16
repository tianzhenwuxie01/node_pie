import json
from pathlib import Path
import bpy
import nodeitems_utils

colours = {
    "Attribute": "attribute",
    "Color": "color",
    "Curve": "geometry",
    "Geometry": "geometry",
    "Input": "input",
    "Instances": "geometry",
    "Material": "geometry",
    "Mesh": "geometry",
    "Point": "geometry",
    "Curve Primitives": "geometry",
    "Mesh Primitives": "geometry",
    "Text": "geometry",
    "Texture": "texture",
    "Utilities": "converter",
    "Vector": "vector",
    "Volume": "geometry",
    "Layout": "layout",
    # 3.4+
    "Mesh Topology": "input",
    "Curve Topology": "input",
    "UV": "converter",
}
overrides = {}
color_overrides = {
    "Input": "input",
    "FunctionNode": "converter",
    "GeometryNodeStringJoin": "converter",
    "ShaderNodeValToRGB": "converter",
    "ShaderNodeCombineXYZ": "converter",
    "ShaderNodeSeparateXYZ": "converter",
    "GeometryNodeSplineParameter": "input",
    "GeometryNodeSplineLength": "input",
    "GeometryNodeCurveHandleTypeSelection": "input",
    "GeometryNodeCurveEndpointSelection": "input",
}

data = {}


def main():

    for area in bpy.context.window.screen.areas:
        print(area.type)
        if area.type == "NODE_EDITOR":
            with bpy.context.temp_override(area=area):
                cats = list(nodeitems_utils.node_categories_iter(bpy.context))
                for cat in cats:
                    if cat.name not in colours.keys():
                        continue
                    items = []
                    for item in cat.items(bpy.context):
                        if not isinstance(item, nodeitems_utils.NodeItem):
                            continue
                        settings = item.settings
                        data_item = {"name": item.label, "identifier": item.nodetype}
                        if settings:
                            data_item["settings"] = settings
                        if item.nodetype in color_overrides:
                            data_item["colour"] = color_overrides[item.nodetype]
                        items.append(data_item)
                    data[cat.identifier] = {"name": cat.name, "colour": colours[cat.name], "items": items}

                selected_nodes = bpy.context.selected_nodes
                items = []
                for node in selected_nodes:
                    data_item = {"name": node.bl_label, "identifier": node.bl_idname}
                    items.append(data_item)
                print(json.dumps(items, indent=2))

    # if data:
    #     fpath = Path(__file__).parent / "node_layout2.json"
    #     with open(fpath, "w") as f:
    #         json.dump(data, f, indent=2)

    #     print("Dumped!")
    # print(data)


# bpy.app.timers.register(main)