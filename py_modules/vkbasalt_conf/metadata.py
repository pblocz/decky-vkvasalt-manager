meta_configuration = {
    "global_configuration": {
        "effects": {
            "type": "string",
            "description": "Colon separated list of effects to use. Effects will be run in order from left to right. One effect can be run multiple times.",
            "hints": [
                "cas - Contrast Adaptive Sharpening",
                "dls - Denoised Luma Sharpening", 
                "fxaa - Fast Approximate Anti-Aliasing",
                "smaa - Enhanced Subpixel Morphological Antialiasing",
                "lut - Color LookUp Table"
            ],
            "default_value": "cas",
            "valid_values": ["cas", "dls", "fxaa", "smaa", "lut"]
        },
        "reshadeTexturePath": {
            "type": "string",
            "description": "Path to reshade shaders textures directory",
            "default_value": "/path/to/reshade-shaders/Textures"
        },
        "reshadeIncludePath": {
            "type": "string", 
            "description": "Path to reshade shaders include directory",
            "default_value": "/path/to/reshade-shaders/Shaders"
        },
        "depthCapture": {
            "type": "string",
            "description": "Enable or disable depth capture",
            "default_value": "off",
            "valid_values": ["on", "off"]
        },
        "toggleKey": {
            "type": "string",
            "description": "Key that toggles the effects on/off",
            "default_value": "Home"
        },
        "enableOnLaunch": {
            "type": "boolean",
            "description": "Sets if the effects are enabled when started",
            "default_value": True
        }
    },
    "shaders": {
        "cas": {
            "description": "Contrast Adaptive Sharpening - AMD's sharpening algorithm that enhances image clarity by increasing contrast in areas where it's most beneficial, while avoiding over-sharpening artifacts.",
            "casSharpness": {
                "type": "float",
                "description": "Specifies the amount of sharpening in the CAS shader",
                "hints": [
                    "0.0 less sharp, less artefacts, but not off",
                    "1.0 maximum sharp more artefacts",
                    "negative values sharpen even less, up to -1.0 make a visible difference"
                ],
                "default_value": 0.4,
                "range": (-1.0, 1.0)
            }
        },
        "dls": {
            "description": "Denoised Luma Sharpening - A sharpening filter that enhances image details while reducing noise and grain artifacts through intelligent denoising.",
            "dlsSharpness": {
                "type": "float",
                "description": "Specifies the amount of sharpening in the Denoised Luma Sharpening shader. Increase to sharpen details within the image.",
                "hints": [
                    "0.0 less sharp, less artefacts, but not off",
                    "1.0 maximum sharp more artefacts"
                ],
                "default_value": 0.5,
                "range": (0.0, 1.0)
            },
            "dlsDenoise": {
                "type": "float", 
                "description": "Specifies the amount of denoising in the Denoised Luma Sharpening shader. Increase to limit how intensely film grain within the image gets sharpened.",
                "hints": [
                    "0.0 min",
                    "1.0 max"
                ],
                "default_value": 0.17,
                "range": (0.0, 1.0)
            }
        },
        "fxaa": {
            "description": "Fast Approximate Anti-Aliasing - NVIDIA's post-processing anti-aliasing technique that smooths jagged edges with minimal performance impact by analyzing pixel patterns.",
            "fxaaQualitySubpix": {
                "type": "float",
                "description": "Can effect sharpness",
                "hints": [
                    "1.00 - upper limit (softer)",
                    "0.75 - default amount of filtering", 
                    "0.50 - lower limit (sharper, less sub-pixel aliasing removal)",
                    "0.25 - almost off",
                    "0.00 - completely off"
                ],
                "default_value": 0.75,
                "range": (0.0, 1.0)
            },
            "fxaaQualityEdgeThreshold": {
                "type": "float",
                "description": "The minimum amount of local contrast required to apply algorithm",
                "hints": [
                    "0.333 - too little (faster)",
                    "0.250 - low quality",
                    "0.166 - default", 
                    "0.125 - high quality",
                    "0.063 - overkill (slower)"
                ],
                "default_value": 0.125,
                "range": (0.063, 0.333)
            },
            "fxaaQualityEdgeThresholdMin": {
                "type": "float",
                "description": "Trims the algorithm from processing darks",
                "hints": [
                    "0.0833 - upper limit (default, the start of visible unfiltered edges)",
                    "0.0625 - high quality (faster)",
                    "0.0312 - visible limit (slower)",
                    "Due to current implementation you likely want to set this to zero",
                    "Tune by looking at mostly non-green content, then start at zero and increase until aliasing is a problem"
                ],
                "default_value": 0.0312,
                "range": (0.0, 0.0833)
            }
        },
        "smaa": {
            "description": "Enhanced Subpixel Morphological Antialiasing - An advanced anti-aliasing technique that provides superior edge quality compared to FXAA by using morphological pattern detection and subpixel information.",
            "smaaEdgeDetection": {
                "type": "string",
                "description": "Changes the edge detection shader",
                "hints": [
                    "luma - default",
                    "color - might catch more edges, but is more expensive"
                ],
                "default_value": "luma",
                "valid_values": ["luma", "color"]
            },
            "smaaThreshold": {
                "type": "float",
                "description": "Specifies the threshold or sensitivity to edges. Lowering this value you will be able to detect more edges at the expense of performance.",
                "hints": [
                    "0.1 is a reasonable value, and allows to catch most visible edges",
                    "0.05 is a rather overkill value, that allows to catch 'em all"
                ],
                "default_value": 0.05,
                "range": (0.0, 0.5)
            },
            "smaaMaxSearchSteps": {
                "type": "integer",
                "description": "Specifies the maximum steps performed in the horizontal/vertical pattern searches",
                "hints": [
                    "4 - low",
                    "8 - medium", 
                    "16 - high",
                    "32 - ultra"
                ],
                "default_value": 32,
                "range": (0, 112)
            },
            "smaaMaxSearchStepsDiag": {
                "type": "integer", 
                "description": "Specifies the maximum steps performed in the diagonal pattern searches",
                "hints": [
                    "0 - low, medium",
                    "8 - high",
                    "16 - ultra"
                ],
                "default_value": 16,
                "range": (0, 20)
            },
            "smaaCornerRounding": {
                "type": "integer",
                "description": "Specifies how much sharp corners will be rounded",
                "hints": [
                    "25 is a reasonable value"
                ],
                "default_value": 25,
                "range": (0, 100)
            }
        },
        "lut": {
            "description": "Color LookUp Table - A color grading technique that maps input colors to output colors using a predefined table, allowing for cinematic color correction and artistic color effects.",
            "lutFile": {
                "type": "string",
                "description": "Path to the LUT file that will be used. Supported are .CUBE files and .png with width == height * height",
                "default_value": "/path/to/lut"
            }
        },
        "adaptivesharpen": {
            "description": "Adaptive Sharpen - A sophisticated sharpening algorithm that enhances image details by analyzing edge characteristics and applying adaptive sharpening curves to avoid over-sharpening artifacts.",
            "curve_height": {
                "type": "float",
                "description": "Main control of sharpening strength",
                "default_value": 1.0,
                "range": (0.01, 2.0)
            },
            "curveslope": {
                "type": "float", 
                "description": "Sharpening curve slope, high edge values",
                "default_value": 0.5,
                "range": (0.01, 2.0)
            },
            "L_overshoot": {
                "type": "float",
                "description": "Max light overshoot before compression",
                "default_value": 0.003,
                "range": (0.001, 0.1)
            },
            "L_compr_low": {
                "type": "float",
                "description": "Light compression, default (0.167=~6x)",
                "default_value": 0.167,
                "range": (0.0, 1.0)
            },
            "L_compr_high": {
                "type": "float",
                "description": "Light compression, surrounded by edges (0.334=~3x)",
                "default_value": 0.334,
                "range": (0.0, 1.0)
            },
            "D_overshoot": {
                "type": "float",
                "description": "Max dark overshoot before compression",
                "default_value": 0.009,
                "range": (0.001, 0.1)
            },
            "D_compr_low": {
                "type": "float",
                "description": "Dark compression, default (0.250=4x)",
                "default_value": 0.250,
                "range": (0.0, 1.0)
            },
            "D_compr_high": {
                "type": "float",
                "description": "Dark compression, surrounded by edges (0.500=2x)",
                "default_value": 0.500,
                "range": (0.0, 1.0)
            },
            "scale_lim": {
                "type": "float",
                "description": "Abs max change before compression",
                "default_value": 0.1,
                "range": (0.01, 1.0)
            },
            "scale_cs": {
                "type": "float",
                "description": "Compression slope above scale_lim",
                "default_value": 0.056,
                "range": (0.0, 1.0)
            },
            "pm_p": {
                "type": "float",
                "description": "Power mean p-value",
                "default_value": 0.7,
                "range": (0.01, 1.0)
            }
        },
        "clarity": {
            "description": "Clarity - Enhances image detail and local contrast using unsharp mask techniques with customizable blend modes and masking options.",
            "ClarityRadius": {
                "type": "integer",
                "description": "Higher values will increase the radius of the effect",
                "hints": ["0|1|2|3|4"],
                "default_value": 3,
                "range": (0, 4)
            },
            "ClarityOffset": {
                "type": "float",
                "description": "Additional adjustment for the blur radius. Increasing the value will increase the radius",
                "default_value": 2.0,
                "range": (1.0, 5.0)
            },
            "ClarityBlendMode": {
                "type": "string",
                "description": "Blend modes determine how the clarity mask is applied to the original image",
                "hints": ["Soft Light", "Overlay", "Hard Light", "Multiply", "Vivid Light", "Linear Light", "Addition"],
                "default_value": "Hard Light",
                "valid_values": ["Soft Light", "Overlay", "Hard Light", "Multiply", "Vivid Light", "Linear Light", "Addition"]
            },
            "ClarityBlendIfDark": {
                "type": "integer",
                "description": "Any pixels below this value will be excluded from the effect. Set to 50 to target mid-tones",
                "default_value": 50,
                "range": (0, 255)
            },
            "ClarityBlendIfLight": {
                "type": "integer",
                "description": "Any pixels above this value will be excluded from the effect. Set to 205 to target mid-tones",
                "default_value": 205,
                "range": (0, 255)
            },
            "ClarityViewBlendIfMask": {
                "type": "boolean",
                "description": "The mask used for BlendIf settings. The effect will not be applied to areas covered in black",
                "default_value": False
            },
            "ClarityStrength": {
                "type": "float",
                "description": "Adjusts the strength of the effect",
                "default_value": 0.4,
                "range": (0.0, 1.0)
            },
            "ClarityDarkIntensity": {
                "type": "float",
                "description": "Adjusts the strength of dark halos",
                "default_value": 0.4,
                "range": (0.0, 1.0)
            },
            "ClarityLightIntensity": {
                "type": "float",
                "description": "Adjusts the strength of light halos",
                "default_value": 0.0,
                "range": (0.0, 1.0)
            },
            "ClarityViewMask": {
                "type": "boolean", 
                "description": "The mask is what creates the effect. View it when making adjustments to get a better idea of how your changes will affect the image",
                "default_value": False
            }
        },
        "lumasharpen": {
            "description": "Luma Sharpen - Sharpens the image by blurring the original pixel with surrounding pixels and subtracting the blur, similar to Unsharp Mask in Photoshop but applied in luma to avoid color artifacts.",
            "sharp_strength": {
                "type": "float",
                "description": "Strength of the sharpening",
                "default_value": 0.65,
                "range": (0.1, 3.0)
            },
            "sharp_clamp": {
                "type": "float",
                "description": "Limits maximum amount of sharpening a pixel receives. This helps avoid 'haloing' artifacts which would otherwise occur when you raised the strength too much",
                "default_value": 0.035,
                "range": (0.0, 1.0)
            },
            "pattern": {
                "type": "string",
                "description": "Choose a sample pattern",
                "hints": [
                    "Fast - faster but slightly lower quality",
                    "Normal - normal quality",
                    "Wider - less sensitive to noise but also to fine details",
                    "Pyramid shaped - slightly more aggressive look"
                ],
                "default_value": "Normal",
                "valid_values": ["Fast", "Normal", "Wider", "Pyramid shaped"]
            },
            "offset_bias": {
                "type": "float",
                "description": "Offset bias adjusts the radius of the sampling pattern. Pattern designed for offset bias of 1.0",
                "default_value": 1.0,
                "range": (0.0, 6.0)
            },
            "show_sharpen": {
                "type": "boolean",
                "description": "Visualize the strength of the sharpen. This is useful for seeing what areas the sharpening affects the most",
                "default_value": False
            }
        },
        "vibrance": {
            "description": "Vibrance - Intelligently boosts the saturation of pixels so pixels that had little color get a larger boost than pixels that had a lot, avoiding oversaturation.",
            "Vibrance": {
                "type": "float",
                "description": "Intelligently saturates (or desaturates if you use negative values) the pixels depending on their original saturation",
                "default_value": 0.75,
                "range": (-1.0, 1.0)
            },
            "VibranceRGBBalance": {
                "type": "float3",
                "description": "A per channel multiplier to the Vibrance strength so you can give more boost to certain colors over others. This is handy if you are colorblind and less sensitive to a specific color",
                "default_value": [1.0, 1.0, 1.0],
                "range": (0.0, 10.0)
            }
        },
        "curves": {
            "description": "Curves - Uses S-curves to increase contrast without clipping highlights and shadows, offering various mathematical formulas for different contrast characteristics.",
            "Mode": {
                "type": "string",
                "description": "Choose what to apply contrast to",
                "default_value": "Luma",
                "valid_values": ["Luma", "Chroma", "Both Luma and Chroma"]
            },
            "Formula": {
                "type": "string",
                "description": "The contrast s-curve formula to use",
                "hints": [
                    "Sine - smooth curve", 
                    "Abs split - sharp transitions",
                    "Smoothstep - balanced approach",
                    "Exp formula - exponential curve",
                    "Simplified Catmull-Rom - fastest performance",
                    "Perlins Smootherstep - very smooth",
                    "Abs add - alternative sharp method",
                    "Technicolor Cinestyle - cinema look",
                    "Parabola - mathematical curve",
                    "Half-circles - circular curves",
                    "Polynomial split - complex curve"
                ],
                "default_value": "Simplified Catmull-Rom (0,0,1,1)",
                "valid_values": ["Sine", "Abs split", "Smoothstep", "Exp formula", "Simplified Catmull-Rom (0,0,1,1)", "Perlins Smootherstep", "Abs add", "Technicolor Cinestyle", "Parabola", "Half-circles", "Polynomial split"]
            },
            "Contrast": {
                "type": "float",
                "description": "The amount of contrast you want",
                "default_value": 0.65,
                "range": (-1.0, 1.0)
            }
        },
        "border": {
            "description": "Border - Adds customizable borders around the image, useful for fixing light borders in some games or creating cinematic letterboxing effects.",
            "border_width": {
                "type": "float2",
                "description": "Border size measured in pixels. If set to zero then the ratio will be used instead",
                "default_value": [0.0, 0.0],
                "range": (0.0, 1920.0)
            },
            "border_ratio": {
                "type": "float",
                "description": "Set the desired ratio for the visible area",
                "default_value": 2.35
            },
            "border_color": {
                "type": "float3",
                "description": "Color of the border",
                "default_value": [0.0, 0.0, 0.0],
                "range": (0.0, 1.0)
            }
        },
        "daltonize": {
            "description": "Daltonize - Simulates and compensates for color blindness using the daltonization algorithm, helping colorblind users see colors more distinctly.",
            "Type": {
                "type": "string",
                "description": "Type of color blindness to simulate or compensate for",
                "hints": [
                    "Protanopia - reds are greatly reduced (1% men)",
                    "Deuteranopia - greens are greatly reduced (1% men)", 
                    "Tritanopia - blues are greatly reduced (0.003% population)"
                ],
                "default_value": "Protanopia",
                "valid_values": ["Protanopia", "Deuteranopia", "Tritanopia"]
            }
        },
        "levels": {
            "description": "Levels - Allows you to set new black and white levels to increase contrast, useful for expanding TV range (16-235) to PC range (0-255).",
            "BlackPoint": {
                "type": "integer",
                "description": "The black point is the new black - literally. Everything darker than this will become completely black",
                "default_value": 16,
                "range": (0, 255)
            },
            "WhitePoint": {
                "type": "integer",
                "description": "The new white point. Everything brighter than this becomes completely white",
                "default_value": 235,
                "range": (0, 255)
            },
            "HighlightClipping": {
                "type": "boolean",
                "description": "Colors between the two points will be stretched, which increases contrast, but details above and below the points are lost (clipping). This setting marks the pixels that clip",
                "hints": [
                    "Red: Some detail is lost in the highlights",
                    "Yellow: All detail is lost in the highlights", 
                    "Blue: Some detail is lost in the shadows",
                    "Cyan: All detail is lost in the shadows"
                ],
                "default_value": False
            }
        },
        "technicolor": {
            "description": "Technicolor - Emulates the classic Technicolor film look with enhanced color separation and saturation using color filters.",
            "Power": {
                "type": "float",
                "description": "Power of the Technicolor effect",
                "default_value": 4.0,
                "range": (0.0, 8.0)
            },
            "RGBNegativeAmount": {
                "type": "float3",
                "description": "RGB negative amounts for color separation",
                "default_value": [0.88, 0.88, 0.88]
            },
            "Strength": {
                "type": "float",
                "description": "Adjust the strength of the effect",
                "default_value": 0.4,
                "range": (0.0, 1.0)
            }
        },
        "sepia": {
            "description": "Sepia/Tint - Applies a sepia tone or custom color tint to the image for vintage or artistic effects.",
            "Tint": {
                "type": "float3",
                "description": "Color tint to apply to the image",
                "default_value": [0.55, 0.43, 0.42],
                "range": (0.0, 1.0)
            },
            "Strength": {
                "type": "float",
                "description": "Adjust the strength of the effect",
                "default_value": 0.58,
                "range": (0.0, 1.0)
            }
        },
        "filmgrain": {
            "description": "Film Grain - Adds realistic film grain noise to the image using Gaussian noise algorithms with signal-to-noise ratio controls.",
            "Intensity": {
                "type": "float",
                "description": "How visible the grain is. Higher is more visible",
                "default_value": 0.5,
                "range": (0.0, 1.0)
            },
            "Variance": {
                "type": "float",
                "description": "Controls the variance of the Gaussian noise. Lower values look smoother",
                "default_value": 0.4,
                "range": (0.0, 1.0)
            },
            "Mean": {
                "type": "float",
                "description": "Affects the brightness of the noise",
                "default_value": 0.5,
                "range": (0.0, 1.0)
            },
            "SignalToNoiseRatio": {
                "type": "integer",
                "description": "Higher Signal-to-Noise Ratio values give less grain to brighter pixels. 0 disables this feature",
                "default_value": 6,
                "range": (0, 16)
            }
        },
        "cartoon": {
            "description": "Cartoon - Creates a cartoon-like effect by filtering out faint edges and enhancing stronger ones for a stylized appearance.",
            "Power": {
                "type": "float",
                "description": "Amount of effect you want",
                "default_value": 1.5,
                "range": (0.1, 10.0)
            },
            "EdgeSlope": {
                "type": "float",
                "description": "Raise this to filter out fainter edges. You might need to increase the power to compensate. Whole numbers are faster",
                "default_value": 1.5,
                "range": (0.1, 6.0)
            }
        },
        "crt": {
            "description": "CRT - Simulates the visual characteristics of old cathode ray tube monitors including scanlines, curvature, and phosphor glow.",
            "Amount": {
                "type": "float",
                "description": "Amount of CRT effect you want",
                "default_value": 1.0,
                "range": (0.0, 1.0)
            },
            "Resolution": {
                "type": "float",
                "description": "Input size coefficient (low values gives the 'low-res retro look')",
                "default_value": 1.15,
                "range": (1.0, 8.0)
            },
            "Gamma": {
                "type": "float",
                "description": "Gamma of simulated CRT",
                "default_value": 2.4,
                "range": (0.0, 4.0)
            },
            "MonitorGamma": {
                "type": "float",
                "description": "Gamma of display monitor",
                "default_value": 2.2,
                "range": (0.0, 4.0)
            },
            "Brightness": {
                "type": "float",
                "description": "Used to boost brightness a little",
                "default_value": 0.9,
                "range": (0.0, 3.0)
            },
            "ScanlineIntensity": {
                "type": "integer",
                "description": "Intensity of scanlines",
                "default_value": 2,
                "range": (2, 4)
            },
            "ScanlineGaussian": {
                "type": "boolean",
                "description": "Use the new nongaussian scanlines bloom effect",
                "default_value": True
            },
            "Curvature": {
                "type": "boolean", 
                "description": "Barrel effect",
                "default_value": False
            }
        },
        "dpx": {
            "description": "DPX/Cineon - Film emulation shader that simulates the color grading characteristics of digital cinema cameras and film stocks.",
            "RGB_Curve": {
                "type": "float3",
                "description": "RGB curve adjustment for film emulation",
                "default_value": [8.0, 8.0, 8.0],
                "range": (1.0, 15.0)
            },
            "RGB_C": {
                "type": "float3",
                "description": "RGB C values for color balance",
                "default_value": [0.36, 0.36, 0.34],
                "range": (0.2, 0.5)
            },
            "Contrast": {
                "type": "float",
                "description": "Contrast adjustment",
                "default_value": 0.1,
                "range": (0.0, 1.0)
            },
            "Saturation": {
                "type": "float",
                "description": "Saturation level",
                "default_value": 3.0,
                "range": (0.0, 8.0)
            },
            "Colorfulness": {
                "type": "float",
                "description": "Colorfulness intensity",
                "default_value": 2.5,
                "range": (0.1, 2.5)
            },
            "Strength": {
                "type": "float",
                "description": "Adjust the strength of the effect",
                "default_value": 0.2,
                "range": (0.0, 1.0)
            }
        },
        "fakehdr": {
            "description": "Fake HDR - Simulates HDR (High Dynamic Range) effects by creating bloom and enhancing dynamic range, though not true HDR.",
            "HDRPower": {
                "type": "float",
                "description": "Power of the HDR effect",
                "default_value": 1.3,
                "range": (0.0, 8.0)
            },
            "radius1": {
                "type": "float",
                "description": "First blur radius for bloom effect",
                "default_value": 0.793,
                "range": (0.0, 8.0)
            },
            "radius2": {
                "type": "float",
                "description": "Second blur radius for bloom effect. Raising this seems to make the effect stronger and also brighter",
                "default_value": 0.87,
                "range": (0.0, 8.0)
            }
        },
        "liftgammagain": {
            "description": "Lift Gamma Gain - Professional color grading tool that allows separate control of shadows (lift), midtones (gamma), and highlights (gain) for each RGB channel.",
            "RGB_Lift": {
                "type": "float3",
                "description": "Adjust shadows for red, green and blue",
                "default_value": [1.0, 1.0, 1.0],
                "range": (0.0, 2.0)
            },
            "RGB_Gamma": {
                "type": "float3",
                "description": "Adjust midtones for red, green and blue",
                "default_value": [1.0, 1.0, 1.0],
                "range": (0.0, 2.0)
            },
            "RGB_Gain": {
                "type": "float3",
                "description": "Adjust highlights for red, green and blue",
                "default_value": [1.0, 1.0, 1.0],
                "range": (0.0, 2.0)
            }
        },
        "monochrome": {
            "description": "Monochrome - Converts images to black and white using various film emulation presets and custom conversion values with optional saturation control.",
            "Monochrome_preset": {
                "type": "string",
                "description": "Choose a monochrome preset based on classic B/W camera films",
                "hints": [
                    "Custom - use custom conversion values",
                    "Monitor or modern TV - standard conversion",
                    "Equal weight - simple average",
                    "Various film stocks (Agfa, Ilford, Kodak) - emulate specific film characteristics"
                ],
                "default_value": "Custom",
                "valid_values": ["Custom", "Monitor or modern TV", "Equal weight", "Agfa 200X", "Agfapan 25", "Agfapan 100", "Agfapan 400", "Ilford Delta 100", "Ilford Delta 400", "Ilford Delta 400 Pro & 3200", "Ilford FP4", "Ilford HP5", "Ilford Pan F", "Ilford SFX", "Ilford XP2 Super", "Kodak Tmax 100", "Kodak Tmax 400", "Kodak Tri-X"]
            },
            "Monochrome_conversion_values": {
                "type": "float3",
                "description": "Custom conversion values for RGB to monochrome conversion",
                "default_value": [0.21, 0.72, 0.07],
                "range": (0.0, 1.0)
            }
        },
        "tonemap": {
            "description": "Tonemap - Comprehensive tone mapping shader with gamma, exposure, saturation controls plus defog and bleach effects for cinematic color grading.",
            "Gamma": {
                "type": "float",
                "description": "Adjust midtones. 1.0 is neutral. This setting does exactly the same as the one in Lift Gamma Gain, only with less control",
                "default_value": 1.0,
                "range": (0.0, 2.0)
            },
            "Exposure": {
                "type": "float",
                "description": "Adjust exposure",
                "default_value": 0.0,
                "range": (-1.0, 1.0)
            },
            "Saturation": {
                "type": "float",
                "description": "Adjust saturation",
                "default_value": 0.0,
                "range": (-1.0, 1.0)
            },
            "Bleach": {
                "type": "float",
                "description": "Brightens the shadows and fades the colors",
                "default_value": 0.0,
                "range": (0.0, 1.0)
            },
            "Defog": {
                "type": "float",
                "description": "How much of the color tint to remove",
                "default_value": 0.0,
                "range": (0.0, 1.0)
            },
            "FogColor": {
                "type": "float3",
                "description": "Which color tint to remove",
                "default_value": [0.0, 0.0, 1.0],
                "range": (0.0, 1.0)
            }
        },
        "vignette": {
            "description": "Vignette - Darkens the edges of the image to simulate camera lens vignetting effects with multiple algorithm options and customizable parameters.",
            "Type": {
                "type": "string",
                "description": "Type of vignette algorithm to use",
                "hints": [
                    "Original - classic center-based vignette",
                    "New - round mathematical approach",
                    "TV style - television-like vignette",
                    "Untitled 1-4 - experimental variations"
                ],
                "default_value": "Original",
                "valid_values": ["Original", "New", "TV style", "Untitled 1", "Untitled 2", "Untitled 3", "Untitled 4"]
            },
            "Ratio": {
                "type": "float",
                "description": "Sets a width to height ratio. 1.00 (1/1) is perfectly round, while 1.60 (16/10) is 60% wider than it's high",
                "default_value": 1.0,
                "range": (0.15, 6.0)
            },
            "Radius": {
                "type": "float",
                "description": "Lower values = stronger radial effect from center",
                "default_value": 2.0,
                "range": (-1.0, 3.0)
            },
            "Amount": {
                "type": "float",
                "description": "Strength of black. -2.00 = Max Black, 1.00 = Max White",
                "default_value": -1.0,
                "range": (-2.0, 1.0)
            },
            "Slope": {
                "type": "integer",
                "description": "How far away from the center the change should start to really grow strong (odd numbers cause a larger fps drop than even numbers)",
                "default_value": 2,
                "range": (2, 16)
            },
            "Center": {
                "type": "float2",
                "description": "Center of effect for 'Original' vignette type. 'New' and 'TV style' do not obey this setting",
                "default_value": [0.5, 0.5],
                "range": (0.0, 1.0)
            }
        },
        "4xbrz": {
            "description": "4xBRZ - Pixel art scaling algorithm designed to upscale pixelated games while preserving sharp edges and reducing scaling artifacts.",
            "coef": {
                "type": "float",
                "description": "Strength of the effect (4 or 6 recommended values)",
                "hints": [
                    "Calculate as: Screen Height / Original Game Height",
                    "For 1920x1080: use 6 for most games",
                    "For 1280x720: use 4"
                ],
                "default_value": 2.0,
                "range": (1.0, 10.0)
            }
        },
        "defring": {
            "description": "Defring - Removes color fringing artifacts (chromatic aberration) by adjusting the alignment of RGB color channels.",
            "Type": {
                "type": "string",
                "description": "Defring algorithm type",
                "default_value": "Defring",
                "valid_values": ["Defring"]
            }
        }
    }
}