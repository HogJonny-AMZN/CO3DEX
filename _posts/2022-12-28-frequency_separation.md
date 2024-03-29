---
layout: post
title:  "Image Frequency Separation, for Macro Color and Detail Mapping"
summary: "Understanding Frequency Separation"
author: hogjonny
date: '2022-12-29 15:52:00 -0600'
category: techart
thumbnail: /assets/img/posts/2022-12-28-frequency_separation-assets/Photoshop_r2L3xh6UTS.gif
keywords: highpass,frequency,seperation,photoshop,terrain
permalink: /blog/Understanding_Frequency_Separation/
usemathjax: true
---

# Welcome to the Co3deX

Hello and welcome to the Open 3D Engine CO3DEX, a blog of my Journey's in Real-time 3D Graphics, Design Technology and Technical Art. My name is Jonny Galloway, I work for @AWSCloud & my opinions are my own.

## Understanding Image Frequency Separation

### Macro Color and Detail Mapping

This article helps us understand the importance of *Frequency Separation* (FS), which is a technique used in image editing to separate the high-frequency details, such as texture and blemishes, from the low-frequency information, such as color and tone. This allows the editor to make adjustments to these different elements separately, allowing for more precise and targeted edits. For example, the Image Author could use frequency separation to smooth out the skin tone of a portrait without losing the texture of the skin, or to remove blemishes without affecting the overall skin tone. The technique involves creating two layers in the image, one for the high frequencies and one for the low frequencies, and then using blurring and other techniques to separate the two layers. Frequency separation can be a useful tool in a variety of editing situations, including portrait retouching, product photography, and landscape editing.

As noted above, the frequency separation technique which is most often used in retouching photos; however, it can also be a useful technique to understand and apply technically to the creating of textures for use in shading techniques.  For example, as we will explore, frequency separation can be used as part of a workflow for generating macro color maps and high-frequency terrain detail materials for use in 3D graphics.  You may already know about *high pass filtering* and this is also related to that (for instance, *high pass terrain detail maps.*)  First we will explain frequency separation as a concept, then we will utilize it with a terrain detail texture.

## Basic Frequency Separation

Let's take a working example:

We have a colorful image with lots of color and detail, we are going to separate out the low frequency and high frequency data.

This is a manual process for separating low / high frequency in an image editor like Photoshop.  YES, there is a *high pass* filter available in Photoshop but ...

1. It doesn't give us the matching low pass (although there is another process we could use to get that by removing the high pass from original, to generate the low pass, and we will cover that later)

2. The other benefit here is having full control over the low pass data (and we get to understand HOW the high pass filter actually works)

### Layer Setup

Here is our original image, we are going to prepare the frequency separation in a manner that is similar to photo retouching.  Below this table of images are the instructions for how to generate each layer.  

| Layer 1                                                                                                                        | Layer 2                                                                                                                        | Layer 3                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/000.png" width="300px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/001.png" width="300px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/002.png" width="300px" title="" alt="" data-align="inline"> |

This image I generated using https://beta.dreamstudio.ai/dream with the following prompt "A colorful explosion of quantum particles in a swirling flow. Use a rainbow of color values, including blues, greens, reds, and yellows.  With high contrast. Make the center the brightest, where sun like particle has exploded yellow photons. High-def, high resolution.  3D simulation. Trending on ArtStation." And then I tweaked it some in Photoshop (The images I had originally used, I am not sure if they were licensed.)

#### Layer 1

1.  The original image is in the default "Layer 1"

#### Layer 2

1. Duplicate the original image into a new layer called "Layer 2"
2. In "Layer 2" apply a Gaussian blur filter, I used a value of 16 for the blur kernel.

**Note:** The higher the blur...

- The less information in the low pass
- *More* information in the high pass

**Alternatively:** You could find the average single color value of the entire image, and then use this solid color as the low pass. This will maximize the amount of detail and color variance that remains in the *high pass* detail.

#### Layer 3

Now we are going to generate the *high pass*

1. Duplicate the original "Layer 1" again, into a new "Layer 3", and make sure it is on the top of the layer stack
2. In Photoshop, with "Layer 3" selected...
3. Use the menu option:
   1. Image > Apply Image

There are different settings for this dialog depending on whether you are working with 9-bit or 16-bit color values:

##### High Pass, 8-bit Color

These settings are for an image with 8-bit color.

In the dialog set it up like the following:

- Layer: (use layer 2)
- Offset: (use 128)
- Blending: (use subtract)
- Scale: (use 2)

This will get you a high pass image like the one viewed above in Layer 3

<img src="/assets/img/posts/2022-12-28-frequency_separation-assets/003.png" title="" alt="" data-align="inline">

##### High Pass, 16-bit Color

Note: the scale add offset is different for a 16-bit image.

In the dialog set it up like the following:

- Check invert
- Offset: 0
- Blending mode: Add
- Scale: 2

<img src="/assets/img/posts/2022-12-28-frequency_separation-assets/004.png" title="" alt="" data-align="inline">

This should yield similar results.

### Layer Blending

Now, it is possible to combine the _low pass_ "layer 2" and the _high pass_ "layer 3"

In Photoshop, with "Layer 3" selected, set the layer blend mode of the *high pass to Linear light*

<img src="/assets/img/posts/2022-12-28-frequency_separation-assets/005.png" width="65%" title="" alt="" data-align="inline">

As you can see in the screenshot we've restored the original image fidelity by properly blending the low + high pass frequencies back together.  This is exactly the type of situation that may occur during the shading of a material, skip ahead to the section "Blending Math".

## Tiling Textures

**NOTE:  If you are working with tiling image, such as repeating Terrain Detail Textures!**

You will want to use the following steps in order to make sure that both the low pass and high pass will continue to properly tile after the frequency splitting happens:

- Select All
- Edit > Define Pattern ...
  - Save the base image as a pattern
- Image > Canvas Size
  - Width/Height 300%
- Edit > Fill ...
  - Contents: Patterns
  - Custom Pattern: (select the pattern you made previously from the base image)
  - Note:  This fills the image with the pattern, consider it a 3x3 tiled version of you image ... so we can work on the center tile.
- ... now follow the steps up above for splitting the image frequencies ...
- Image > Canvas Size
  - Width/Height: 33.33 ***percent***, or resolutions in **_pixels_**, in this case 1024
  - This will preserve the original center tile, and crop out the border tiles

### ***Why***

- Because these steps, allow the Gaussian blur to take into account the wrapped tiling along the adjacent borders.
- So when the *low pass* (blur) is calculated, the pixel information wraps, then when it's subtracted and cropped both the *low pass* and the *high pass* will still tile properly.

## Blending Math

[Linear Light](https://en.wikipedia.org/wiki/Blend_modes#Dodge_and_burn): this blend mode combines *Linear Dodge* and *Linear Burn* (re-scaled so that neutral colors become middle gray). Dodge is applied when the value on the top layer is lighter than middle gray, and burn applies when the top layer value is darker. The calculation simplifies to the sum of the bottom layer and twice the top layer, subtract 1. This mode decreases the contrast.

Let's explore how that can happen (here's the missing math in GLSL shader code):

**LinearLight**

```glsl
/*
** Basic math
*/
#define BlendAddf(base, blend)          min(base + blend, 1.0)
#define BlendSubstractf(base, blend)    max(base + blend - 1.0, 0.0)

/*
** Redefined in Photoshop terms
*/
#define BlendLinearDodgef               BlendAddf
#define BlendLinearBurnf                BlendSubstractf


/* Linear Light */
#define BlendLinearLightf(base, blend)  (blend < 0.5 ? BlendLinearBurnf(base, (2.0 * blend)) : BlendLinearDodgef(base, (2.0 * (blend - 0.5))))
```

Here is the equivalent blending code from the Lumberyard *Terrain.fxc* fragment shader:

**Lumberyard, terrain.fxc**

```hlsl
// Put back in gamma space to keep look of old blending modes (Note this assumes SRGB always enabled)
baseColor.xyz = sqrt(baseColor.xyz);

// material color is offseted from base
pPass.cDiffuseMap.xyz = saturate(baseColor.xyz + ((pPass.cDiffuseMap-0.5h) * DetailTextureStrength));

// Put back in linear space (Note this assumes SRGB always enabled)
pPass.cDiffuseMap.xyz *= pPass.cDiffuseMap.xyz;
```

And here is the equivalent blending code for the Open 3D Engine StandradPBR material code, found in the following file [BlendUtility.azsli](https://github.com/o3de/o3de/blob/development/Gems/Atom/Feature/Common/Assets/ShaderLib/Atom/Features/BlendUtility.azsli):

**BlendUtility.azsli**

```hlsl
/*
 * Copyright (c) Contributors to the Open 3D Engine Project.
 * For complete copyright and license terms please see the LICENSE at the root of this distribution.
 *
 * SPDX-License-Identifier: Apache-2.0 OR MIT
 *
 */

#pragma once

#include <Atom/Features/ColorManagement/TransformColor.azsli>

enum class TextureBlendMode { Multiply, LinearLight, Lerp, Overlay };

// See https://en.wikipedia.org/wiki/Blend_modes#Dodge_and_burn
float3 TextureBlend_LinearLight(float3 base, float3 mask)
{
    return saturate(base + 2 * mask - 1);
}

...

//! General purpose utility function for applying a blend between two colors. Note that the order of the colors is not commutative (for most blend modes).
//! @param color - The main color or target color for the blend
//! @param blendColor - The secondary color that will be blended into the main color
//! @param factor - A factor that controls the blend. The specific behavior depends on the blend mode.
//! @param blendMode - Indicates the type of blend to perform
//! @return the resulting blended color
float3 ApplyTextureBlend(float3 color, float3 blendColor, float factor, TextureBlendMode blendMode)
{
    ...

    else
    {
        // To get blend behavior that mimics photoshop, convert to sRGB
        float3 blendColorSRGB = TransformColor(blendColor, ColorSpaceId::ACEScg, ColorSpaceId::SRGB);
        float3 colorSRGB = TransformColor(color, ColorSpaceId::ACEScg, ColorSpaceId::SRGB);

        float3 finalColor = colorSRGB;

        if(blendMode == TextureBlendMode::LinearLight)
        {
            finalColor = TextureBlend_LinearLight(colorSRGB, blendColorSRGB);
        }

        ...

        // Convert back to ACEScg
        finalColor = TransformColor(finalColor, ColorSpaceId::SRGB, ColorSpaceId::ACEScg);

        // Apply factor
        finalColor = lerp(color, finalColor, factor);

        return finalColor;
    }
}
```

## Recombinatorial Examples

Now that we briefly covered the math, let's try out some other tests with combining the low-pass (color) an high-pass (detail.) This technique provides a lot of flexibility, that actually relates to usage within 3D graphics, such as terrain workflows.  In games, we might feed multiple textures of different resolutions, to different parts of the rendering system, where they are then recombined during shading. And the color of pixels may change as we transition across regions of the terrain.

An example might be...

1. A low-resolution [Terrain Macro Material color texture map](https://www.o3de.org/docs/user-guide/components/reference/terrain/terrain-macro-material/)
   
   1 x 1 texel per-meter in world-space
   
   fed to the terrain system (along with macro height, macro normal map, etc.)

2. A high-frequency [Terrain Detail Material](https://www.o3de.org/docs/user-guide/components/reference/terrain/terrain-detail-material/)
   
   2048 resolution texels per-meter in world-space
   
   the low-frequency macro color and the high-frequency detail texture are combined during shading.

Some of the benefits of taking this approach:

- Terran Macro Color can be drawn in the distance without the Detail Texture and appear correct
- Detail textures can use a LinearLight blend to combine high-frequency details with the underlying macro color (with stable visual results)
- Detail texturing can blend in/out over distance smoothly, triangles in the background can render with less shading instructions (should equal performance gains)
- Detail texturing can blend nicely with modulation and variance in the macro color (e.g. blending along an area where the macro color grades from a light brown to dark brown)
- We can independently manage the resolution of the macro textures and detail materials (which also means we have better control over memory footprints)

We can mimic some of what happens during shading within Photoshop, lets' explore some of these aspects to better understand them.

### Low-Resolution Color

In this example, we are going to muck around with the low pass *and crunch it down* to a much smaller image, then reconstruct the image from two maps of different resolutions. Theoretically, we will loose some information which may decrease aspects like the fidelity, quality and overall data integrity of the image (but hey, we do that ALL the time in real time graphics.)

| Original                                                                                                                       | Downsampled                                                                                                                    | Interpolated                                                                                                                   | Reconstruction                                                                                                                 | Difference                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| Low-pass, 1024px                                                                                                               | Low-pass, 64px                                                                                                                 | Low-pass, bilinear, 1024px                                                                                                     | Blended Reconstruction                                                                                                         | Difference                                                                                                                     |
| <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/006.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/007.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/008.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/009.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/010.png" width="200px" title="" alt="" data-align="inline"> |

As you can see in the final reconstructed image, and the Difference next to it, there is not any perceptible loss in quality (the Difference appears black) - in fact, you have to maximize the leveling of the histogram to visually see where the differences might be, here is an example:

<img src="/assets/img/posts/2022-12-28-frequency_separation-assets/difference.png" title="" width="65%" alt="" data-align="inline">

One more try, how low can we go?  Let's drop the low-pass from 1024 pixels, to 16x16, before recombining.

| Original                                                                                                                       | Downsampled                                                                                                                    | Interpolated                                                                                                                   | Reconstruction                                                                                                                 | Difference                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
|                                                                                                                                |                                                                                                                                |                                                                                                                                |                                                                                                                                |                                                                                                                                |
| <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/011.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/012.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/013.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/014.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/015.png" width="200px" title="" alt="" data-align="inline"> |

There, now we are really starting to see a perceptible difference in integrity, and the quality is arguably diminished ... but the fidelity as far as using it is _good enough to me._ This is basically what will occur in the rendering engine, when a triangle/quad is rendered and reconstructs shading with low-res terrain macro color (1 texel per-meter) and a high-resolution detail texture (2048 textels per-meter)

### Results

Here are all three reconstructions again side-by-side, each is the final reconstructed resolution of 1024 pixels, only the resolution and up-sampling of the low-pass was altered.

| Original                                                                                                                       | 64x64 bilinear                                                                                                                 | 16x16 bilinear                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| Low-pass: 1024                                                                                                                 | Low-pass: 64                                                                                                                   | Low-pass: 16                                                                                                                   |
| High-pass: 1024                                                                                                                | High-pass: 1024                                                                                                                | High-pass: 1024                                                                                                                |
| <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/016.png" width="256px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/009.png" width="256px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/014.png" width="256px" title="" alt="" data-align="inline"> |

Looking left to right here, I have a hard time picking out the differences.  I have to put them into Photoshop layers to compare them before it's obvious.

### Color Alteration

This is a pretty flexible technique, as the high pass frequency can be applied across a wide range of shifts in the low pass base colors and still arrive at decent looking results.  The idea here, would be hue shifts in areas of the terrain where the macro color is changing. Here are a few extreme examples:

| Original                                                                                                                       | Downsampled                                                                                                                    | Interpolated                                                                                                                   | Reconstruction                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| 1024 pixels                                                                                                                    | 32 x 32 pixels                                                                                                                 | Bilinear upscale                                                                                                               | Blended                                                                                                                        |
| <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/019.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/020.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/021.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/022.png" width="200px" title="" alt="" data-align="inline"> |

And in this next version, we are simple going to hue shift our original low pass colors

| Original                                                                                                                       | Downsampled                                                                                                                    | Interpolated                                                                                                                   | Reconstruction                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| 1024 pixels                                                                                                                    | 32 x 32 pixels                                                                                                                 | Bilinear upscale                                                                                                               | Blended                                                                                                                        |
| <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/023.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/024.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/025.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/026.png" width="200px" title="" alt="" data-align="inline"> |

As you can see, we can make pretty abrupt and wild changes to the base color, and still arrive at visually interesting results!

### High Pass Filter

Now let's briefly explore how we can use Photoshop's built-in *high pass filter* to generate our *high pass detail map*, then apply that back to the original to generate the matching *low pass macro texture*

| 1.Generate High-Pass                                                                                                           | 2.Linear Burn                                                                                                                  | 3.Linear Add                                                                                                                   | 4.Low-Pass A                                                                                                                   | 5.Low-Pass B                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/027.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/028.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/029.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/030.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/031.png" width="200px" title="" alt="" data-align="inline"> |

#### 1. Generate High-Pass

Leave the original unaltered image in the default Photoshop layer "background".

duplicate the original image into "Layer 1", we will use this layer to generate the high-pass.

Use "Layer 1" to generate the high-pass using the filter method

Filter > Other > High Pass

- I used a radius of 16 in these examples
- However, you can use any size kernel, like 32 or more
- The best results, are tuning this value based on the variation within the textures color and details

#### 2. Linear Burn

- Duplicate the High-Pass (Layer 1) into "Layer 2"
- You can hide "Layer 1", we aren't going to directly use the high-pass in this example
- Level the Image in "Layer 2":
  - Output Levels: 0 ... 128
- Invert the Image
- Set the Layer to *Linear Burn*

<img src="/assets/img/posts/2022-12-28-frequency_separation-assets/032.png" title="" alt="" data-align="inline">

#### 3. Linear Add

- Duplicate the High Pass (Layer 1) again into "Layer 3""
- Level the Image in "Layer 3":
  - Output Levels: 128 ... 255
- Invert the Image
- Set the Layer to *Linear Dodge (Add)*

<img src="/assets/img/posts/2022-12-28-frequency_separation-assets/033.png" title="" alt="" data-align="inline">

#### 4. Low-Pass A

As you can see, we are pretty close to the simple Gaussian Blurred Low Pass Method (close enough that after down-sampling and interpolation the errors might be removed.)

But as you can see in the image to the right, the error are a result of the *order of operation* ...

#### 5. Low-Pass B (Alt, re-order layers)

Swap the ordering of Layer 2 & 3

Now the error show up in the upper ranges!

This is why I prefer the other method, it gives you full control over separating the *high pass* ... and generating a usable *low pass*. It's less steps and the blending can be done in a single operation (LinearLight) without introducing any errors.

**Note**: There is a REALLY good chance, there is a more correct and error free way to handle this approach, which I simply haven't figured out yet. And I am guessing, it would be fairly easy to write a Python script or some code that would do all of this work and spit out the separated frequencies.

## Terrain Macro Color and Detail Materials

To use frequency separation for the purpose of Terrain Detail Materials, you would typically start by obtaining an image of the terrain that you want to create a color map and high-frequency detail material for. This image could be a photograph or a scan of real-world terrain (such as Quixel materials), or it could be a digital image that you have created or obtained from another source.  Next, you would use the frequency separation technique to create two layers in the image: one for the high frequencies and one for the low frequencies. The high frequency layer would contain the detail and texture information, while the low frequency layer would contain the color and tone information. You could then use the high frequency layer to generate a high-frequency detail material for the terrain, and the low frequency layer to generate a macro color map. These materials could then be used in a 3D graphics application to create a detailed and realistic representation of the terrain.

That is the gist, when we talk scanned materials, photogrammetry, or Physically Based Rendering (PBR), there is more to it than that, but those concepts and details are outside the scope of this article.

This approach works well for creating detail materials for terrain, here is the original cry doc that covers this:

*[Creating Terrain Textures and Materials - CRYENGINE 3 Manual - Documentation](http://docs.cryengine.com/display/SDKDOC2/Creating+Terrain+Textures+and+Materials)*

Note: the more *homogeneous (in overall color)* your terrain detail texture is, the more successful this approach.

Let's do something similar to their doc, but we will use this freely available texture set: [polyhaven.com/a/cobblestone_floor_04]([http://docs.cryengine.com/display/SDKDOC2/Creating+Terrain+Textures+and+Materials](https://polyhaven.com/a/cobblestone_floor_04))

1.  Downlaod the texture set (.zip)
2. Unpack the .zip
3. We are only going to use the color map for this example (the other textures can be loaded into a PBR material.)
4. These files should be renamed if you are going to use them in Open 3D Engine, due to naming conventions, our filemask suffix's need to be last to inform the asset processor ho to handle the texture channel type (basecolor, normal, roughness, etc.)  I recommend making the same naming fix to all of the texture image files.
5. Rename from this:  cobblestone_floor_04_diff_1k.jpg
6. To this: cobblestone_floor_04_1k_diff.jpg
7. Follow the steps for the "frequency separation workflow"

| Source                                                                                                                                 | Low-Pass                                                                                                                               | High-Pass                                                                                                                              | Reconstructed                                                                                                                          |
| -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/texture_040.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/texture_041.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/texture_042.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/texture_043.png" width="200px" title="" alt="" data-align="inline"> |
|                                                                                                                                        |                                                                                                                                        |                                                                                                                                        | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/texture_046.png" width="200px" title="" alt="" data-align="inline"> |
| <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/texture_040.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/texture_044.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/texture_042.png" width="200px" title="" alt="" data-align="inline"> | <img src="/assets/img/posts/2022-12-28-frequency_separation-assets/texture_045.png" width="200px" title="" alt="" data-align="inline"> |

- Above in the top row is the low-pass color map, which we resized to 32x32 pixels and then resized back to the target resolution with bilinear sampling.
- In the bottom row, we have used the average macro color instead for the low-pass.
- In the far right column, we compare the two reconstructions, and the resulting differences between them.

As you can see in the diff on the right, there is almost no perceptible difference between the low-pass and using a single averaged color (some macro contrast is lost, the overall result is more homogeneous.)  These results may vary of course depending on the amount of change in color and details across the image map. And it reiterate an important point, you may want to play with the blur size kernel to get the best results per image. Since that quality result may be subjective, automation pipelines may not be able to easily apply the best fit; seems like this is an opportunity for a future learning model that can make this best guess. 

## FAQ

**Q: Sniff test ... why should I care about this?**

**A**: This ia a flexible and common approach to _terrain detail_ mapping:

CryEngine reference: _[Creating Terrain Textures and Materials - CRYENGINE 3 Manual - Documentation](http://docs.cryengine.com/display/SDKDOC2/Creating+Terrain+Textures+and+Materials)_

Splitting frequencies gets us:

1. Low-Pass Color
   1. This can be used directly as a texture input, for example in a terrain generator, or the o3de Terrain Macro Material
   2. Can be used to find the average color (down-sample to 1x1), this value can be placed into the color swatch of a StandardPBR material (or Terrain Detail Material)
   3. Or we could use the low pass, to generate a color ramp (and a matching height map), which can be used as input in programs like World Machine to use in *Colorization: Working with Texture Color Ramps* (<-- future article to write.)
2. High-Pass, High-Frequency Detail
   1. Load the high-pass as the basecolor texture in a StandardPBR material and set the Blend mode to LinearLight.
   2. This same approach can be used as the detail texture for a standard material, for instance
   3. Use the StandardPBR/TerrainDetailMaterial and blend the material across terrain, including good results when the macro color shifts (for example: an area that transitions from a light brown to a dark brown.)

Q: Where to next?

A: There are a lot of ideas for where this can lead, here are some:

- You could turn these steps into a Photoshop Action, this should allow you to automate running them on any image within Photoshop.
  - [Automate your edits with Photoshop actions.](https://www.adobe.com/products/photoshop/actions.html#:~:text=Adobe%20Photoshop%20actions%20are%20a,they%20help%20you%20automate%20tasks.)
- Once you've done that, you can use Actions in bulk automation (process a whole folder)
  - Photoshop > File > automation > Batch...
  - [Processing Batch Files](https://helpx.adobe.com/photoshop/using/processing-batch-files.html)
- Once you have a Photoshop Action, that could be made into a Photoshop Droplet.  This would allow you to integrate into a pipeline and external automation.
  - Photoshop > File > automation > Create Droplet
  - [How and Why to Use Droplets](https://www.slrlounge.com/photoshop-tips-how-and-why-to-use-droplets/)
- Write a Python image utility script that does all this work (with PIL, or OpenImageIO)
- Make that py script into a Dockable Utility Panel tool that is integrated into the Editor and/or Content Tools and Workflows.

**Q: Can I just use the High Pass Filter in Photoshop?**

**A:** Yes. See the section above titled 'High Pass Filter'?

- If you don't care about retrieving the low-pass color, then this is fine (and much quicker to perform)
- You can also derive a low-pass color map this way (but it's clunky as shown above)

**Q: What does LinearLight mean?**

**A:** This is covered above, but here is a synopsis:

Speak like an artist... artists that use Photoshop, speak in the terms of Photoshop and Image Editing.  In Photoshop ...

*LinearLight uses a combination of the **Linear** Dodge **blend mode** on the lighter pixels, and the **Linear** Burn **blend mode** on the darker pixels (a half-strength application of both **modes**). Similar to the Vivid **Light blend mode** in overdrive, and typically results in a more extreme effect.*

**Q: Can you tell me how the blending math works?**

**A:** Yes, this is also covered above, but if you want a general crash course on the math here is reference for how to do a lot of _Photoshop style_ blending and maths, in shader code:

[PhotoshopMathFP.hlsl · cplotts/WPFSLBlendModeFx](https://github.com/cplotts/WPFSLBlendModeFx/blob/master/PhotoshopMathFP.hlsl)

**Q: Do I need to use Photoshop?**

**A:** No. Most popular image editors will handle this, but you may need to google how.  But other applications, such as Adobe Substance 3D Designer, also have ways to work with generating high-pass detail textures (see next question.)

**Q: Can I do something similar with Adobe Substance 3D Designer?**

**A:** Yes. Substance 3D Designer has nodes that perform similar functions to a High Pass Filter:

- [Highpass, Substance 3D Designer](https://substance3d.adobe.com/documentation/sddoc/highpass-159449203.html)
- [Luminance Highpass, Substance 3D Designer](https://substance3d.adobe.com/documentation/sddoc/luminance-highpass-159449246.html)

**Q: Can you give me a rundown on 'Frequency separation' in game and real-time 3D content, versus it's use on photo retouching?**

**A:** Yes. There are a lot of areas it can be used, here are a few examples:

- Separate macro color and high frequency detail, as described in this document: make a macro color texture, make a detail texture for terrain.
- It's a viable approach to storing color as split-values for a PBR material (Quixel's native data is stored this way), in this sense there may be situations where it is a valued feature (1 texture, 2 jackets of slightly different hues)
- This approach can also be used as an optimization, it's possible that the high-pass texture may have less visual compression artifacts (it thus may help combat DXT and other compression artifacts.)
- It can be used to generate high-frequency detail textures for other non-terrain workflows as well, such as repeat patterns for blue jeans, other cloth, and leathers, etc.
- It can similar be used in skin shading workflows, for instance highpass wrinkles and pore maps.
- Image balance: get rid of uneven light and shadow in a material.  The game material example above, shows this, we lost some contrast and things became more homogeneous, but in actuality that made the end results higher quality as the tiling-repeat of those materials will be less visually obvious.

## Reference

Cry doc ref related to this:

- [Terrain.Layer Shader - CRYENGINE 3 Manual - Documentation](http://docs.cryengine.com/display/SDKDOC2/Terrain.Layer+Shader)
- [Creating Terrain Textures and Materials - CRYENGINE 3 Manual - Documentation](http://docs.cryengine.com/display/SDKDOC2/Creating+Terrain+Textures+and+Materials)
- [Painting Terrain - CRYENGINE 3 Manual - Documentation](http://docs.cryengine.com/display/SDKDOC2/Painting+Terrain)

General:

- [The Power of the High Pass Filter](https://www.gamedeveloper.com/art/the-power-of-the-high-pass-filter)
- [How to Retouch Skin Using Frequency Separation in Photoshop](https://www.makeuseof.com/photoshop-how-to-retouch-skin-frequency-separation/)
- [Inverted High Pass (IHP) Retouching Tutorial — Retoucher — Daniel Meadows](https://www.dmd-digital-retouching.com/blog/inverted-high-pass-ihp-retouching-tutorial/)
- [grunge highpass and lowpass textures](https://blog.stockvault.net/freebies/grunge-highpass-and-lowpass-textures/)

---

```python
import logging as _logging
_PKGNAME = 'co3dex'
_LOGGER = _logging.getLogger(_PKGNAME)
_LOGGER.info(f'Initializing: {_PKGNAME} ... Frequency Seperation')
```

---
