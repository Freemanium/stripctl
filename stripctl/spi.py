from spidev import SpiDev
from typing import Union, List

DEFAULT_FREQ = 8*1000**2 # 8MHz

class SPIError(RuntimeError):
    def __init__(self, bus_index: int, dev_index: int):
        self.bus_index = bus_index
        self.dev_index = dev_index
        super().__init__(f'SPI device not found (bus_index={bus_index} device_index={dev_index})')

class SPI:
    def __init__(self, bus_index: int, dev_index: int, freq: int = DEFAULT_FREQ):
        self.bus = bus_index
        self.dev = dev_index
        self.freq = freq
        self._spi = None

        self._open()
    
    def __del__(self):
        self._close()
    
    def _open(self):
        if not self._spi:
            self._spi = SpiDev()
            try:
                self._spi.open(self.bus, self.dev)
            except FileNotFoundError:
                raise SPIError(self.bus, self.dev)
            self._spi.max_speed_hz = self.freq
    
    def _close(self):
        if self._spi:
            self._spi.close()
            self._spi = None
        
    def send(self, data: Union[bytes, List[int]]):
        self._spi.writebytes2(bytes(data))