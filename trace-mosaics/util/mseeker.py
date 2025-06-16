import os;from PIL import Image;import numpy as np;import matplotlib.pyplot as plt;import math
#def find(pic):img=Image.open(pic).convert("L");data=np.array(img).astype(int);y,x,max_pos=0,0,np.unravel_index(np.argmax(data),data.shape);print(data[y][x],f'\nx: {max_pos[1]} |y: {max_pos[0]}')

"""
NOTES:
|adjustable variables:
|- gap_threshold
||} gap_threshold is the amount of pixels to be considered dups and deleted
|- error_threshold
||} error_threshold is the margin of error needed for images with possible compresion
|- margin_steps
||} margin_steps is to increas the perimeter of possible areas, incase the code doesnt get all of the ROI
|- SNAP_STD_THRESHOLD
||} agressive snapping if std is within specification
|- peak_threshold_multiplier
||} to be honest i forgot what this is for

first version by: acedatique

revisions by:
acedatique v0.1
acedatique v0.2
acedatique with ChatGpt as assistant v0.3
acedatique v0.4

rough mosiac detector, to use please import this python file and activate it by doing: test(image) in a different python file with this file imported


WIP:
errors, only works with decent non compressed looking files
very poorly built

comments by author:
i couldnt find this anywhere else so i did it myself please dont judge
when i code i dont comment, mainly becuase i realised if i dont comment ill look at everything agian and make changes with any new knowledge ive gained and usually turns out better then when i make comments.  im a bad programer and unfortanatly if your looking for mosiac detectors thats not ai i was the only one who attempted, feel free to fork or help me learn and improve this.  If you fork please give me credit and also let me know so i can see and learn from what you did differently.  when you credit me i am not claiming your work but rather i wanna see who i inspired and i wanna see this project through.

this works by shifting pixels left and down and look for "spikes" within the rgb spectrum and assumes it as possible mosiac areas, then i clean the noises out and verify the best looking possible data which is the biggest list then verify smaller ones and if fails then remove it and if other groups succeeds then add that as verified and add missing lines incase of missed spikes which would happen if mosiac squares are same colors as its partners.  there is a lot of margin of erros and set sizes becuase i wanted it to be automatic but got lazy once i realise that this project was fighting be for every electron my pc breathes.  so now its simi automatic where you MIGHT need to change some numbers around.


to save your time the most you will have to look for is in cleaner or grouping.  
test is to setup the procesing and add rough lines
cleaner is used to clean up noisyness via clustered lines
grouping is the verification and adding of lines
"""
def cleaner(x_grid, gap_threshold=10):
    if not x_grid:
        return []
    cleaned = [x_grid[0]]
    for x in x_grid[1:]:
        if abs(x - cleaned[-1]) > gap_threshold:
            cleaned.append(x)
    test = grouping(cleaned)
    return test

def grouping(t, error_threshold=0.05):
    if not t:
        return []
    groups = []
    current_group = [t[0]]
    for i in range(1, len(t)):
        prev_val = current_group[-1]
        curr_val = t[i]
        diff = abs(curr_val - prev_val)
        base = abs(prev_val)
        lower_bound = base * (1 - error_threshold)
        upper_bound = base * (1 + error_threshold)
        if lower_bound <= curr_val <= upper_bound:
            current_group.append(curr_val)
        else:
            groups.append(current_group)
            current_group = [curr_val]
    groups.append(current_group)
    print(f'GROUPS: {groups}')
    largest_group = max(groups, key=len) if groups else []
    if len(largest_group) >= 2:
        spacings = [abs(largest_group[i] - largest_group[i-1]) for i in range(1, len(largest_group))]
        avg_spacing = math.ceil(sum(spacings) / len(spacings))
    else:
        avg_spacing = 0
    print(f'LIST: {spacings}\nAVG: {avg_spacing}')
    verified=[]
    for i in range(0,len(groups)):
        if len(groups[i]) <= 1:
            continue
        elif len(groups[i]) >1:
            for I in range(1, len(groups[i])):
                Lowervalue = abs(groups[i][I]-groups[i][I-1]) * (1 - error_threshold)
                Uppervalue = abs(groups[i][I]-groups[i][I-1]) * (1 + error_threshold)
                if Lowervalue <= avg_spacing <= Uppervalue:
                    verified.append(groups[i])
                    break
    print(f'VERIFIED: {verified}')
    verified_lines = sorted({v for group in verified for v in group})
    estimated_lines = set()
    for i in range(len(verified_lines) - 1):
        start = verified_lines[i]
        end = verified_lines[i + 1]
        gap = end - start
        if gap > avg_spacing * 1.1:
            steps = int(round(gap / avg_spacing)) - 1
            for step in range(1, steps + 1):
                candidate = int(round(start + step * avg_spacing))
                if candidate not in verified_lines and start < candidate < end:
                    estimated_lines.add(candidate)
    margin_steps = 4
    for group in verified:
        if not group:
            continue
        min_val = min(group)
        max_val = max(group)
        for step in range(1, margin_steps + 1):
            candidate = min_val - step * avg_spacing
            if candidate not in verified_lines and candidate not in estimated_lines and candidate >= 0:
                estimated_lines.add(candidate)
        for step in range(1, margin_steps + 1):
            candidate = max_val + step * avg_spacing
            if candidate not in verified_lines and candidate not in estimated_lines:
                estimated_lines.add(candidate)
    all_lines = sorted(set(verified_lines).union(estimated_lines))
    print(f'Final grid lines with filled gaps between verified groups only: {all_lines}')
    return all_lines

def test(pic):
    SNAP_STD_THRESHOLD = 0.0
    peak_threshold_multiplier = 2.0
    im = Image.open(pic).convert('RGB')
    width, height = im.size
    im2 = im.transform(im.size, Image.AFFINE, (1, 0, 1, 0, 1, 1))
    arr1 = np.asarray(im, dtype=np.int16)
    arr2 = np.asarray(im2, dtype=np.int16)
    diff = np.abs(arr1 - arr2).astype(np.uint8)
    diff_sum = np.sum(diff, axis=2)

    # --- X-Axis (Vertical gridlines detection) ---
    column_sums = np.sum(diff_sum, axis=0)[:-1]
    mean = np.mean(column_sums)
    threshold_x = mean * peak_threshold_multiplier
    peaks_x = [i for i, v in enumerate(column_sums) if v > threshold_x]
    grid_x = cleaner(peaks_x)
    peak_spacing = np.diff(peaks_x)
    mean_spacing_x = np.mean(peak_spacing) if len(peak_spacing) > 0 else 0
    std_spacing_x = np.std(peak_spacing) if len(peak_spacing) > 0 else 0
    print('[X Axis] mean gap:', mean_spacing_x, 'std:', std_spacing_x)
    if peaks_x and std_spacing_x < SNAP_STD_THRESHOLD:
        base_x = peaks_x[0]
        snapped_x = list(range(base_x, width, round(mean_spacing_x)))
        print('[X Axis] Snapping enabled.')
    else:
        snapped_x = grid_x
        print('[X Axis] Snapping disabled. Using raw peaks.')

    # --- Y-Axis (Horizontal gridlines detection) ---
    row_sums = np.sum(diff_sum, axis=1)[:-1]
    mean_y = np.mean(row_sums)
    threshold_y = mean_y * peak_threshold_multiplier
    peaks_y = [i for i, v in enumerate(row_sums) if v > threshold_y]
    spacing_y = np.diff(peaks_y)
    mean_spacing_y = np.mean(spacing_y) if len(spacing_y) > 0 else 0
    std_spacing_y = np.std(spacing_y) if len(spacing_y) > 0 else 0
    print('[Y Axis] mean gap:', mean_spacing_y, 'std:', std_spacing_y)
    if peaks_y and std_spacing_y < SNAP_STD_THRESHOLD:
        base_y = peaks_y[0]
        snapped_y = list(range(base_y, height, round(mean_spacing_y)))
        print('[Y Axis] Snapping enabled.')
    else:
        snapped_y = cleaner(peaks_y)
        print('[Y Axis] Snapping disabled. Using raw peaks.')
    print("Peaks X:", peaks_x)
    print("X Gaps:", np.diff(peaks_x))

    # --- Plot column-wise intensity (X) ---
    plt.figure(figsize=(12, 4))
    plt.plot(column_sums, label='Column intensity difference')
    plt.axhline(mean, color='green', linestyle='--', label='Mean')
    plt.axhline(mean * 2, color='red', linestyle='--', label='Threshold (mean × 2)')
    plt.title("Column-wise Intensity (X axis)")
    plt.xlabel("X coordinate (columns)")
    plt.ylabel("Intensity sum")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Plot row-wise intensity (Y) ---
    plt.figure(figsize=(4, 6))
    plt.plot(row_sums, range(len(row_sums)), label='Row intensity difference')
    plt.axvline(mean_y, color='green', linestyle='--', label='Mean')
    plt.axvline(mean_y * 2, color='red', linestyle='--', label='Threshold (mean × 2)')
    plt.gca().invert_yaxis()
    plt.title("Row-wise Intensity (Y axis)")
    plt.ylabel("Y coordinate (rows)")
    plt.xlabel("Intensity sum")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Overlay gridlines on the original image ---
    plt.figure(figsize=(8, 8))
    plt.imshow(im)
    for x in snapped_x:
        plt.axvline(x, color='red', linestyle='--', alpha=0.6)
    for y in snapped_y:
        plt.axhline(y, color='blue', linestyle='--', alpha=0.6)
    plt.title("Snapped Pixelation Grid Overlay")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

