from typing import Any

import msgpack


class PackageDeliveryManager:
    __slots__ = []
    
    @staticmethod
    def pack_data(data: Any) -> bytes:
        try:
            return msgpack.packb(data, use_bin_type=True)

        except Exception as e:
            raise ValueError(f"Error packing data: {e}")
    
    @staticmethod
    def unpack_data(data: bytes) -> Any:
        try:
            return msgpack.unpackb(data, raw=False)

        except Exception as e:
            raise ValueError(f"Error unpacking data: {e}")
