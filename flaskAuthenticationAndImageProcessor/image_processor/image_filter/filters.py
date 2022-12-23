from PIL import Image
import numpy as np
from PIL import ImageFilter


class Filter:

    def __init__(self, image) -> None:
        super().__init__()
        self.image = image

    def filter(self, **kwargs) -> Image:
        """
        Filter image
        :param kwargs:
        :return: Image
        """
        pass


class Rgb(Filter):
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB')


class Rgba(Filter):
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGBA')


class Greyscale(Filter):
    def filter(self, **kwargs) -> Image:
        return self.image.convert('L')


class HandDrawn(Filter):
    def filter(self, **kwargs) -> Image:
        a = np.asarray(self.image.convert('L')).astype('float')

        depth = 10.  # (0-100)
        grad = np.gradient(a)
        grad_x, grad_y = grad
        grad_x = grad_x * depth / 100.
        grad_y = grad_y * depth / 100.
        A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
        uni_x = grad_x / A
        uni_y = grad_y / A
        uni_z = 1. / A

        vec_el = np.pi / 2.2
        vec_az = np.pi / 4.
        dx = np.cos(vec_el) * np.cos(vec_az)
        dy = np.cos(vec_el) * np.sin(vec_az)
        dz = np.sin(vec_el)

        b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)
        b = b.clip(0, 255)

        im = Image.fromarray(b.astype('uint8'))
        return im


class EdgeCurve(Filter):
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB').filter(ImageFilter.FIND_EDGES)


class Blur(Filter):
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB').filter(ImageFilter.BLUR)


class Contour(Filter):
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB').filter(ImageFilter.CONTOUR)


class EdgeEnhance(Filter):
    def filter(self, **kwargs) -> Image:
        if 'more' in kwargs:
            return self.image.convert('RGB').filter(ImageFilter.EDGE_ENHANCE_MORE)
        else:
            return self.image.convert('RGB').filter(ImageFilter.EDGE_ENHANCE)


class Emboss(Filter):
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB').filter(ImageFilter.EMBOSS)


class Smooth(Filter):
    def filter(self, **kwargs) -> Image:
        if 'more' in kwargs:
            return self.image.convert('RGB').filter(ImageFilter.SMOOTH_MORE)
        else:
            return self.image.convert('RGB').filter(ImageFilter.SMOOTH)


class Sharpen(Filter):
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB').filter(ImageFilter.SHARPEN)


class GaussianBlur(Filter):
    def filter(self, **kwargs) -> Image:
        if 'radius' in kwargs:
            r = int(kwargs['radius'])
        else:
            r = 2
        return self.image.convert('RGB').filter(ImageFilter.GaussianBlur(radius=r))


class MinFilter(Filter):
    def filter(self, **kwargs) -> Image:
        if 'size' in kwargs:
            s = int(kwargs['size'])
        else:
            s = 3
        return self.image.convert('RGB').filter(ImageFilter.MinFilter(size=s))


class MedianFilter(Filter):
    def filter(self, **kwargs) -> Image:
        if 'size' in kwargs:
            s = int(kwargs['size'])
        else:
            s = 3
        return self.image.convert('RGB').filter(ImageFilter.MedianFilter(size=s))


class MaxFilter(Filter):
    def filter(self, **kwargs) -> Image:
        if 'size' in kwargs:
            s = int(kwargs['size'])
        else:
            s = 3
        return self.image.convert('RGB').filter(ImageFilter.MaxFilter(size=s))


class ModeFilter(Filter):
    def filter(self, **kwargs) -> Image:
        if 'size' in kwargs:
            s = int(kwargs['size'])
        else:
            s = 3
        return self.image.convert('RGB').filter(ImageFilter.ModeFilter(size=s))


class UnsharpMask(Filter):
    def filter(self, **kwargs) -> Image:
        if 'radius' in kwargs:
            r = int(kwargs['radius'])
        else:
            r = 2
        if 'percent' in kwargs:
            p = int(kwargs['percent'])
        else:
            p = 150
        if 'threshold' in kwargs:
            t = int(kwargs['threshold'])
        else:
            t = 3
        return self.image.convert('RGB').filter(ImageFilter.UnsharpMask(radius=r, percent=p, threshold=t))


class Emboss45d(Filter):
    def filter(self, **kwargs) -> Image:
        class Emboss45DegreeFilter(ImageFilter.BuiltinFilter):
            name = "Emboss_45_degree"
            filterargs = (3, 3), 1, 0, (
                -1, -1, 0,
                -1, 1, 1,
                0, 1, 1
            )
        return self.image.convert('RGB').filter(Emboss45DegreeFilter)


class SharpEdge(Filter):
    def filter(self, **kwargs) -> Image:
        class SharpEdgeFilter(ImageFilter.BuiltinFilter):
            name = "Sharp_Edge"
            filterargs = (3, 3), 1, 0, (
                1, 1, 1,
                1, -7, 1,
                1, 1, 1
            )
        return self.image.convert('RGB').filter(SharpEdgeFilter)


class SharpCenter(Filter):
    def filter(self, **kwargs) -> Image:
        class SharpCenterFilter(ImageFilter.BuiltinFilter):
            name = "Sharp_Center"
            filterargs = (3, 3), -1, 0, (
                1, 1, 1,
                1, -9, 1,
                1, 1, 1
            )
        return self.image.convert('RGB').filter(SharpCenterFilter)


class EmbossAsymmetric(Filter):
    def filter(self, **kwargs) -> Image:
        class EmbossAsymmetricFilter(ImageFilter.BuiltinFilter):
            name = "Emboss_Asymmetric"
            filterargs = (3, 3), 1, 0, (
                2, 0, 0,
                0, -1, 0,
                0, 0, -1
            )
        return self.image.convert('RGB').filter(EmbossAsymmetricFilter)
