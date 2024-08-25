from typing import Self
import enum
import math
import numpy as np
import numpy.typing as npt

class Color:
    class ColorType(enum.Enum):
        HSL = enum.auto()
        HSV = enum.auto()
        RGB = enum.auto()

    __slots__ = (
        "values",
        "color_type",
    )

    def __init__(self, values: npt.NDArray[np.uint8 | np.float32], color_type: ColorType) -> None:
        self.values = values
        self.color_type = color_type

    @classmethod
    def from_rgb(cls, red: int, green: int, blue: int) -> Self:
        return cls(np.array((red, green, blue), ndmin=2), cls.ColorType.RGB)

    @classmethod
    def from_rgb_array(cls, rgb: npt.NDArray[np.uint8]) -> Self:
        return cls(rgb, cls.ColorType.RGB)

    @classmethod
    def from_hsl(cls, hue: int, saturation: int, lightness: int) -> Self:
        return cls(np.array((hue, saturation, lightness), ndmin=2), cls.ColorType.HSL)

    @classmethod
    def from_hsl_array(cls, hsl: npt.NDArray[np.float32]) -> Self:
        return cls(hsl, cls.ColorType.HSL)

    def as_rgb(self) -> npt.NDArray[np.float32]:
        if self.color_type == self.ColorType.RGB:
            return self.values
        elif self.color_type == self.ColorType.HSL:
            chroma = (1 - np.abs(2 * self.values[:, 2] - 1)) * self.values[:, 1]
            hue_prime = (self.values[:, 0] % 360) / 60
            x = chroma * (1 - np.abs(hue_prime % 2 - 1))

            zeros = np.zeros(self.values[:, 0].shape)
            m = np.array(self.values[:, 2] - chroma / 2, ndmin=2).T

            # todo! make this faster using some kind of numpy vectorization.
            colors = np.stack([
                {
                    0: [c, x, z],
                    1: [x, c, z],
                    2: [z, c, x],
                    3: [z, x, c],
                    4: [x, z, c],
                    5: [c, z, x],
                }[int(h)]
                for h, c, x, z in zip(hue_prime, chroma, x, zeros)
            ])

            return ((colors + m) * 255).astype(np.uint8)
        else:
            raise ValueError()

    def as_hsl(self) -> npt.NDArray[np.float32]:
        if self.color_type == self.ColorType.HSL:
            return self.values
        elif self.color_type == self.ColorType.RGB:
            rgb = self.values / 255
            colors_min = np.min(rgb, 1)
            colors_max = np.max(rgb, 1)
            lightness = (colors_max + colors_min) / 2
            chroma = colors_max - colors_min

            lightness[np.isclose(lightness, 0)] += 1e-6
            lightness[np.isclose(lightness, 1)] -= 1e-6
            saturation = 2 * (colors_max - lightness) / (1 - np.abs(2 * lightness - 1))

            value_channel = np.argmax(rgb, 1)
            hue = np.empty(saturation.shape)
            for (i, (r, g, b)) in enumerate(rgb):
                if math.isclose(chroma[i], 0, rel_tol=1e-6):
                    hue[i] = 0
                elif value_channel[i] == 0:
                    hue[i] = 60 * (((g - b) / chroma[i]) % 6)
                elif value_channel[i] == 1:
                    hue[i] = 60 * (((b - r) / chroma[i]) + 2)
                elif value_channel[i] == 2:
                    hue[i] = 60 * (((r - g) / chroma[i]) + 4)
                else:
                    hue[i] = 0

            return np.stack([hue, saturation, lightness], axis=1)
        else:
            raise ValueError()
