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
        }
    }
}