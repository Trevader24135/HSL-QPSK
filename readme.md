# HSL-QPSK

Perform QPSK modulation on arbitrary data and hide that modulated data in an
image as cycling HSL colors!

Currently the Hue stays fixed, while the saturation and lightness are modulated
using the In-Phase and Quadrature channels respectively, but there's nothing to
say that this couldn't be done a different way.

The default output image is an animated PNG image, which not too many
applications support. The output can be viewed in most web browsers, or it could
simply be converted to something like a GIF, with a bit of a hit to the quality.
