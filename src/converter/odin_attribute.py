import numpy as np

from .odin_constants import OdinAttributeFormat, OdinAttributeType


class OdinAttribute:
    def __init__(
        self, type: OdinAttributeType, format: OdinAttributeFormat, offset: int
    ) -> None:
        self.offset = offset
        self.format = format
        self.type = type
        self._dtype = self.format.to_numpy_dtype()
        self._elements_count = self.format.to_element_count()
        self._normalized = self.type.is_normalized()

    @property
    def data_type(self) -> np.dtype:
        return self._dtype

    @property
    def elements_count(self) -> int:
        return self._elements_count

    def read(self, data: bytes, offset: int) -> np.ndarray:
        match self.format:
            case OdinAttributeFormat.NormalizedWeightVector:
                value = np.frombuffer(data, dtype=np.uint32, offset=offset, count=1)[0]
                x = (value >> 21) * 0.0002442
                y = ((value >> 10) & 0x7FF) * 0.0002442
                z = (value & 0x3FF) * 0.0002442
                array = np.array([((1.0 - x) - y) - z, x, y, z], dtype=self._dtype)
            case _:
                array = np.frombuffer(
                    data, dtype=self._dtype, offset=offset, count=self._elements_count
                )

        if self._normalized and np.issubdtype(self._dtype, np.integer):
            info = np.iinfo(self._dtype)
            array = array.astype(np.float32) / info.max

        return array
