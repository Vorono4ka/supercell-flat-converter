import argparse
import json
import math
import os
from json import JSONEncoder

from gltf import GlTF

from .odin import SupercellOdinGLTF


def process_object_json(obj):
    if isinstance(obj, dict):
        return {k: process_object_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [process_object_json(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return 0.0
    return obj


class ObjectProcessor(JSONEncoder):
    def encode(self, obj, *args, **kwargs):
        return super().encode(process_object_json(obj), *args, **kwargs)


debug = False

required_folders = {
    "sc_input": "In-SC-glTF",
    "sc_output": "Out-SC-glTF",
    "def_input": "In-glTF",
    "def_output": "Out-glTF",
}

if debug:
    required_folders["in_debug"] = "In-Debug"
    required_folders["out_debug"] = "Out-Debug"


def decode(post_process: bool) -> None:
    files = os.scandir(required_folders["sc_input"])

    for file_entry in files:
        print(f'Working on "{file_entry.name}"', end="")
        gltf = GlTF.parse(file_entry.path)

        if post_process:
            odin = SupercellOdinGLTF(gltf)
            gltf = odin.remove_odin()

        if debug:
            for chunk in gltf.chunks:
                if chunk.name != "JSON":
                    continue

                file = open(
                    os.path.join(required_folders["out_debug"], file_entry.name)
                    + ".json",
                    "wb",
                )
                if isinstance(chunk.data, bytes):
                    file.write(chunk.data)
                else:
                    file.write(
                        bytes(
                            json.dumps(chunk.data, cls=ObjectProcessor, indent=4),
                            "utf8",
                        )
                    )

                break

        print(f'\rSuccessful: "{file_entry.name}"')

        gltf.write(os.path.join(required_folders["def_output"], file_entry.name))


# def encode() -> None:
#     files = os.scandir(required_folders["def_input"])
#
#     for filepath in files:
#         print(f"Reading: {filepath.name}")
#         gltf = glTF()
#
#         with open(filepath.path, "rb") as file:
#             gltf.read(file.read())
#
#         for chunk in gltf.chunks:
#             chunk.serialize_json()
#
#         if debug:
#             open(
#                 os.path.join(required_folders["in_debug"], f"{filepath.name}.bin"),
#                 "wb",
#             ).write([chunk.data for chunk in gltf.chunks if chunk.name == "FLA2"][0])
#
#         print(f"Successful: {filepath.name}")
#
#         with open(
#             os.path.join(required_folders["sc_output"], filepath.name), "wb"
#         ) as file:
#             file.write(gltf.write())


def main() -> None:
    for name in required_folders.values():
        os.makedirs(name, exist_ok=True)

    parser = argparse.ArgumentParser(
        prog="scglTF Converter",
        description="Tool for converting Supercell glTF files to usual ones and vice versa",
    )

    parser.add_argument("mode", type=str, choices=["decode", "decodeRaw"])  # , "encode"

    args = parser.parse_args()
    match args.mode:
        case "decode":
            decode(post_process=True)
        case "decodeRaw":
            decode(post_process=False)
        # case "encode":
        #     encode()


if __name__ == "__main__":
    main()
