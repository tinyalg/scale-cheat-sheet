import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
from matplotlib.lines import Line2D

# Cスタートの鍵盤マッピング (C D E F G A B)
c_note_mapping = {
    0: (True, 0), 1: (False, 0), 2: (True, 1), 3: (False, 1),
    4: (True, 2), 5: (True, 3), 6: (False, 2), 7: (True, 4),
    8: (False, 3), 9: (True, 5), 10: (False, 4), 11: (True, 6)
}
c_black_positions = [0.7, 1.7, 3.7, 4.7, 5.7]

# Fスタートの鍵盤マッピング (F G A B C D E)
f_note_mapping = {
    5: (True, 0), 6: (False, 0), 7: (True, 1), 8: (False, 1),
    9: (True, 2), 10: (False, 2), 11: (True, 3), 0: (True, 4),
    1: (False, 3), 2: (True, 5), 3: (False, 4), 4: (True, 6)
}
f_black_positions = [0.7, 1.7, 2.7, 4.7, 5.7]

# Key names with relative minors
key_names = [
    "C / Am",
    "Db / Bbm",
    "D / Bm",
    "Eb / Cm",
    "E / C#m",
    "F / Dm",
    "Gb / Ebm",
    "G / Em",
    "Ab / Fm",
    "A / F#m",
    "Bb / Gm",
    "B / G#m"
]

# Correct scale notes for each of the 12 keys based on music theory
scale_labels = [
    ["C", "D", "E", "F", "G", "A", "B"],          # C Major (0)
    ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],     # Db Major (1)
    ["D", "E", "F#", "G", "A", "B", "C#"],        # D Major (2)
    ["Eb", "F", "G", "Ab", "Bb", "C", "D"],       # Eb Major (3)
    ["E", "F#", "G#", "A", "B", "C#", "D#"],      # E Major (4)
    ["F", "G", "A", "Bb", "C", "D", "E"],         # F Major (5)
    ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],    # Gb Major (6)
    ["G", "A", "B", "C", "D", "E", "F#"],         # G Major (7)
    ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],      # Ab Major (8)
    ["A", "B", "C#", "D", "E", "F#", "G#"],       # A Major (9)
    ["Bb", "C", "D", "Eb", "F", "G", "A"],        # Bb Major (10)
    ["B", "C#", "D#", "E", "F#", "G#", "A#"]      # B Major (11)
]

# Intervals for a major scale in semitones
major_intervals = [0, 2, 4, 5, 7, 9, 11]

# Display order sorted by Circle of Fifths logic (4x3 grid)
display_order = [
    5,  0,  7,   # F,  C,  G
    10, 9,  2,   # Bb, A,  D
    3,  4,  11,  # Eb, E,  B
    8,  1,  6    # Ab, Db, Gb
]

# 追加: black_positionsを引数で受け取るように変更
def draw_keyboard(ax, title, white_colors, black_colors, white_labels, black_labels, w_is_root, b_is_root, w_hatches, b_hatches, black_positions):
    """Draws a one-octave keyboard with circled note labels"""
    # Draw white keys
    for i in range(7):
        rect = patches.Rectangle((i, 0), 1, 4, linewidth=1.2, edgecolor='black', facecolor=white_colors[i], hatch=w_hatches[i], zorder=1)
        ax.add_patch(rect)
        
        if white_labels[i]:
            f_size = 11 if w_is_root[i] else 9
            pad_size = 0.4 if w_is_root[i] else 0.3
            l_weight = 1.5 if w_is_root[i] else 1.0
            y_pos = 0.68 if w_is_root[i] else 0.6  # Slightly elevate root notes
            
            ax.text(i + 0.5, y_pos, white_labels[i], ha='center', va='center', fontsize=f_size, fontweight='bold', zorder=3,
                    bbox=dict(boxstyle=f"circle,pad={pad_size}", fc="white", ec="black", lw=l_weight))

    # Draw black keys (位置を動的に変更)
    for i, pos in enumerate(black_positions):
        rect = patches.Rectangle((pos, 1.5), 0.6, 2.5, linewidth=1.2, edgecolor='black', facecolor=black_colors[i], hatch=b_hatches[i], zorder=2)
        ax.add_patch(rect)
        
        if black_labels[i]:
            f_size = 10 if b_is_root[i] else 8
            pad_size = 0.3 if b_is_root[i] else 0.2
            l_weight = 1.5 if b_is_root[i] else 1.0
            y_pos = 2.36 if b_is_root[i] else 2.3  # Slightly elevate root notes
            
            ax.text(pos + 0.3, y_pos, black_labels[i], ha='center', va='center', fontsize=f_size, fontweight='bold', zorder=4,
                    bbox=dict(boxstyle=f"circle,pad={pad_size}", fc="white", ec="black", lw=l_weight))

    ax.set_xlim(0, 7)
    ax.set_ylim(0, 4)
    ax.axis('off')
    ax.set_title(title, fontsize=12, weight='bold', bbox=dict(facecolor='white', edgecolor='none', pad=3.0))


# Create a 4x3 grid and set figsize to A4 portrait (8.27 x 11.69 inches)
fig, axes = plt.subplots(4, 3, figsize=(8.27, 11.69))
axes_flat = axes.flatten()

# Draw connection lines for the Circle of Fifths
path_indices = [0, 1, 2, 5, 4, 7, 8, 11, 10, 9, 6, 3, 0]

for i in range(len(path_indices) - 1):
    start_idx = path_indices[i]
    end_idx = path_indices[i+1]
    
    sr, sc = divmod(start_idx, 3)
    er, ec = divmod(end_idx, 3)
    
    # Determine anchor points based on direction
    if sr == er and sc < ec:    # Right
        xyA, xyB = (1.0, 0.5), (0.0, 0.5)
    elif sr == er and sc > ec:  # Left
        xyA, xyB = (0.0, 0.5), (1.0, 0.5)
    elif sc == ec and sr < er:  # Down
        xyA, xyB = (0.5, 0.0), (0.5, 1.0)
    elif sc == ec and sr > er:  # Up
        xyA, xyB = (0.5, 1.0), (0.5, 0.0)
    
    con = ConnectionPatch(
        xyA=xyA, xyB=xyB,
        coordsA="axes fraction", coordsB="axes fraction",
        axesA=axes_flat[start_idx], axesB=axes_flat[end_idx],
        arrowstyle="-",
        color="#A0A0A0",
        linewidth=5.0,
        zorder=-1
    )
    fig.add_artist(con)


# Render keyboards based on the defined display order
for grid_index, root_note in enumerate(display_order):
    ax = axes_flat[grid_index]
    
    # ここでルート音がF（5）以上かどうかを判定し、マッピングと黒鍵位置を切り替え
    use_f_start = root_note >= 5
    current_mapping = f_note_mapping if use_f_start else c_note_mapping
    current_black_positions = f_black_positions if use_f_start else c_black_positions
    
    w_colors = ['white'] * 7
    b_colors = ['white'] * 5
    w_hatches = ['..'] * 7
    b_hatches = ['..'] * 5
    
    w_labels = [''] * 7
    b_labels = [''] * 5
    w_is_root = [False] * 7
    b_is_root = [False] * 5
    
    for step, interval in enumerate(major_intervals):
        note_index = (root_note + interval) % 12
        is_white, list_index = current_mapping[note_index]  # 切り替えたマッピングを使用
        label_text = scale_labels[root_note][step] 
        
        if is_white:
            w_colors[list_index] = 'white'
            w_hatches[list_index] = None
            w_labels[list_index] = label_text
            if step == 0:
                w_is_root[list_index] = True
        else:
            b_colors[list_index] = 'black'
            b_hatches[list_index] = None
            b_labels[list_index] = label_text
            if step == 0:
                b_is_root[list_index] = True
            
    # black_positions を渡す
    draw_keyboard(ax, key_names[root_note], w_colors, b_colors, w_labels, b_labels, w_is_root, b_is_root, w_hatches, b_hatches, current_black_positions)

# Add main title
fig.suptitle('Scale Cheat Sheet', fontsize=24, fontweight='bold', y=0.96)

# Add descriptive text below title
legend_text = (
    "Solid keys: Notes in the scale   |   Larger circle: Root note (Major)\n"
    "Dotted keys: Non-scale notes (indicates a whole step between scale notes)"
)
fig.text(0.5, 0.92, legend_text, ha='center', va='top', fontsize=10, style='italic', color='#333333')

# Fine-tune margins and spacing for the portrait layout
plt.subplots_adjust(top=0.83, bottom=0.05, left=0.05, right=0.95, hspace=0.35)

# Add legend for the Circle of Fifths line
legend_elements = [
    Line2D([0], [0], color="#A0A0A0", lw=4.0, linestyle="-", label=": Moves along the Circle of Fifths")
]
fig.legend(
    handles=legend_elements,
    loc="upper right",
    frameon=False,
    facecolor="white",
    edgecolor="black",
    bbox_to_anchor=(0.67, 0.899),
    prop={"style": "italic", "size": 10}
)

# Draw dashed boundaries separating flat/sharp key regions
line_style = {
    "color": "#B0B0B0",
    "linestyle": "--", 
    "linewidth": 2.0,
    "zorder": 0,
    "transform": fig.transFigure # Use figure coordinates (0.0 to 1.0)
}

fig.add_artist(Line2D([0.345, 0.345], [0.65, 0.24], **line_style))  # Vertical line
fig.add_artist(Line2D([0.345, 0.39], [0.65, 0.65], **line_style))   # Top horizontal hook
fig.add_artist(Line2D([0.345, 0.39], [0.24, 0.24], **line_style))   # Bottom horizontal hook

# Save outputs
plt.savefig('scale_cheat_sheet_v2.png', dpi=300, bbox_inches='tight')
plt.savefig('scale_cheat_sheet_v2.pdf')
print("Successfully generated the dynamic F/C start Scale Cheat Sheet!")