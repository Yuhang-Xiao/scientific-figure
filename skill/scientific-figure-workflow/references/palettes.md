# Scientific Figure Palettes

Use role-based palettes. Choose colors for background, text, primary signal, secondary groups, muted context, warnings, positive/negative states, and panel fills.

Before drawing, ask the user to choose a palette unless they already supplied one.

## Okabe-Ito / Wong

Best for categorical labels, model groups, flow branches, and colorblind-aware scientific diagrams.

```text
Black      #000000
Orange     #E69F00
Sky blue   #56B4E9
Bluish green #009E73
Yellow     #F0E442
Blue       #0072B2
Vermillion #D55E00
Reddish purple #CC79A7
```

Suggested roles: near-white background, dark gray text, blue or bluish green primary route, orange/vermilion intervention, purple secondary method, yellow only for small highlights.

## Paul Tol Bright

Best for polished multi-category figures where the palette needs to feel vivid but still journal-safe.

```text
Blue    #4477AA
Cyan    #66CCEE
Green   #228833
Yellow  #CCBB44
Red     #EE6677
Purple  #AA3377
Gray    #BBBBBB
```

Suggested roles: blue primary pipeline, cyan measurement/inputs, green successful outputs, red risk/error, gray context.

## Viridis / Cividis Family

Best for ordered values, heatmaps, gradients, confidence, intensity, and model performance maps.

Viridis anchors:

```text
#440154 #3B528B #21918C #5EC962 #FDE725
```

Use Cividis instead when yellow-green contrast is too strong or when print accessibility is critical.

## ColorBrewer Set2

Best for gentle categorical panels, study arms, sample groups, or method families.

```text
#66C2A5 #FC8D62 #8DA0CB #E78AC3 #A6D854 #FFD92F #E5C494 #B3B3B3
```

Use muted fills with dark labels. Avoid using all colors at equal saturation in one dense figure.

## Minimal Journal

Best for serious manuscripts, methods diagrams, and black-and-white-compatible layouts.

```text
Background #FFFFFF or #F7F8FA
Text       #222222
Rules      #BFC5CC
Muted fill #EEF2F5
Primary blue #2F6BFF
Primary green #1B9E77
Primary orange #D95F02
```

Use one primary accent per figure unless the scientific meaning requires more.

References:
- https://www.nature.com/articles/nmeth.1618
- https://personal.sron.nl/~pault/
- https://colorbrewer2.org/
- https://matplotlib.org/stable/users/explain/colors/colormaps.html
