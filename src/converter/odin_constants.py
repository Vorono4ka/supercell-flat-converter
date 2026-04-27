from enum import IntEnum

import numpy as np


class OdinAttributeType(IntEnum):
    a_pos = 0
    a_normal = 1
    a_uv0 = 2
    a_uv1 = 3
    a_color = 4
    a_boneindex = 5
    a_boneweights = 6
    a_tangent = 7
    a_colorMul = 8
    a_colorAdd = 9
    a_model = 10
    a_model2 = 11
    a_model3 = 12
    a_binormal = 13
    a_skinningOffsets = 14
    a_color1 = 15

    def to_attribute_name(self) -> str:
        return {
            OdinAttributeType.a_pos: "POSITION",
            OdinAttributeType.a_normal: "NORMAL",
            OdinAttributeType.a_boneindex: "JOINTS_0",
            OdinAttributeType.a_boneweights: "WEIGHTS_0",
            OdinAttributeType.a_uv0: "TEXCOORD_0",
            OdinAttributeType.a_uv1: "TEXCOORD_1",
            OdinAttributeType.a_color: "COLOR_0",
            OdinAttributeType.a_color1: "COLOR_1",
            OdinAttributeType.a_tangent: "TANGENT",
            # OdinAttributeType.a_colorAdd: 'COLOR_1',
            # OdinAttributeType.a_colorMul: 'COLOR_2',
        }[self]

    def is_normalized(self) -> bool:
        return {
            OdinAttributeType.a_pos: False,
            OdinAttributeType.a_normal: True,
            OdinAttributeType.a_boneindex: False,
            OdinAttributeType.a_boneweights: False,
            OdinAttributeType.a_uv0: True,
            OdinAttributeType.a_uv1: True,
            OdinAttributeType.a_color: False,
            OdinAttributeType.a_color1: False,
            OdinAttributeType.a_tangent: False,
        }[self]


class OdinAttributeFormat(IntEnum):
    UByteVector4 = 3
    ColorRGBA = 9
    UByteVector3 = 12
    ShortVector2 = 22
    FloatVector2 = 29
    FloatVector3 = 30
    NormalizedWeightVector = 36

    def is_normalized(self) -> bool:
        return {
            OdinAttributeFormat.FloatVector3: False,
            OdinAttributeFormat.UByteVector3: False,
            OdinAttributeFormat.UByteVector4: False,
            OdinAttributeFormat.ShortVector2: True,
            OdinAttributeFormat.NormalizedWeightVector: False,
            OdinAttributeFormat.FloatVector2: False,
            OdinAttributeFormat.ColorRGBA: True,
        }[self]

    def to_accessor_type(self) -> str:
        return {
            OdinAttributeFormat.FloatVector3: "VEC3",
            OdinAttributeFormat.UByteVector3: "VEC3",
            OdinAttributeFormat.ShortVector2: "VEC2",
            OdinAttributeFormat.UByteVector4: "VEC4",
            OdinAttributeFormat.NormalizedWeightVector: "VEC4",
            OdinAttributeFormat.FloatVector2: "VEC2",
            OdinAttributeFormat.ColorRGBA: "VEC4",
        }[self]

    def to_accessor_component(self) -> int:
        return {
            OdinAttributeFormat.FloatVector3: 5126,
            OdinAttributeFormat.UByteVector3: 5120,
            OdinAttributeFormat.UByteVector4: 5121,
            OdinAttributeFormat.ShortVector2: 5122,
            OdinAttributeFormat.NormalizedWeightVector: 5126,
            OdinAttributeFormat.FloatVector2: 5126,
            OdinAttributeFormat.ColorRGBA: 5121,
        }[self]

    def to_numpy_dtype(self) -> np.dtype:
        return {
            OdinAttributeFormat.FloatVector3: np.uint32,
            OdinAttributeFormat.UByteVector3: np.byte,
            OdinAttributeFormat.UByteVector4: np.ubyte,
            OdinAttributeFormat.ShortVector2: np.short,
            OdinAttributeFormat.NormalizedWeightVector: np.float32,
            OdinAttributeFormat.FloatVector2: np.float32,
            OdinAttributeFormat.ColorRGBA: np.ubyte,
        }[self]

    def to_element_count(self) -> int:
        return {
            OdinAttributeFormat.FloatVector3: 3,
            OdinAttributeFormat.UByteVector3: 3,
            OdinAttributeFormat.UByteVector4: 4,
            OdinAttributeFormat.NormalizedWeightVector: 4,
            OdinAttributeFormat.FloatVector2: 2,
            OdinAttributeFormat.ColorRGBA: 4,
            OdinAttributeFormat.ShortVector2: 2,
        }[self]
