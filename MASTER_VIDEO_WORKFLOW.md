# Master Video Workflow: The Official @sticklit Stickman Production Pipeline
## The 100% Exact Formula for Viral Minimalist Stick Figure Book Summaries

> **Core Model Identity:**  
> Clean, humorous, insightful 2D stick-figure book summaries in the exact **`@sticklit`** style:  
> - **Canvas:** Borderless pure white background (`#FFFFFF`) with abundant negative space.  
> - **Character Design:** Minimalist 2D cartoon stick figures with clean black ink outlines, white circular heads, expressive eyebrows/pupils, messy hair, and flat solid color clothes.  
> - **Props & Metaphors:** Single high-contrast symbolic props isolated on white (treadmills, umbrellas, scales, mountains, books). No full-bleed environmental art.  
> - **Subtitles:** 2–4 word natural phrased chunks in **pure white** with a clean black outline, floating on white space.

---

### Step 0: Deep Book Research
Before writing:
1. Identify the core philosophical/psychological paradox (e.g. chasing happiness makes you miserable, control creates anxiety, assets vs. liabilities).
2. Character lore: How to represent the protagonist as an expressive stick figure (hair shape, clothing color, key props).
3. Visual metaphors: Translate abstract psychological concepts into simple physical dilemmas (hamster wheel on treadmill, pulling strings, falling through bridge, carrying boulder, umbrella in rain).
4. Extract the exact book title, author, and book cover design for Scene 01.

---

### Step 1 & 2: Autonomous Script Drafting & Selection (Internal)
- Internally draft 3 script angles (Version A, B, C):
  - **Target Runtime:** ~2m 30s to 2m 50s (~380–430 spoken words at ~150 WPM) or tight 2m 00s (~320–340 words).
  - Structure: Hook (0–5s) $\rightarrow$ The Core Lie/Trap $\rightarrow$ The Protagonist's Discovery $\rightarrow$ The Mechanical/Philosophical Rules $\rightarrow$ The Life-Changing Epiphany $\rightarrow$ Book Callout $\rightarrow$ Ending Takeaway.
- Automatically score and select the highest-converting script without cluttering chat.

---

### Step 3: Immediate Audio Synthesis & Phrased Alignment
1. **TTS Synthesis:** Synthesize with **Deepgram Aura-2** (`aura-2-thalia-en` or `aura-2-orpheus-en`).
2. **Word Alignment:** Transcribe with **Deepgram Nova-2** to get millisecond word timestamps.
3. **Phrased Subtitle Pre-Computation (`phrased_subtitles.ass`):**
   - **Chunking:** Natural 2–4 word phrases (never single-word).
   - **Font:** Arial Rounded MT Bold or Montserrat, 80pt bold.
   - **Colors:** **Pure White primary fill** (`&H00FFFFFF&`), clean black outline (`&H00000000&`, 3.5px border), no shadow box.
   - **Placement:** Centered in lower-third (`Alignment=2`, `MarginV=240`), resting on white negative space.
4. **Exact Cue Detection (`exact_cues.json`):**
   - Automatically pre-compute cut points for each visual beat.

---

### Step 4: The @sticklit Prompt Architecture (Output Batches)
Prompts are delivered in two clean batches (Scenes 01–20, Scenes 21–End) both in chat and in 1-click `.txt` files.

#### The Mandatory Prompt Prefix (Prepended to Every Prompt):
```text
9:16 vertical 2D minimalist cartoon stick-figure illustration in the exact @sticklit style. 
Pure borderless white background (#FFFFFF) with abundant clean negative space. 
Crisp solid black ink outlines, flat solid color fills, zero 3D rendering, zero gradients, 
zero background clutter, no floor planes, no wall textures. Near the top center, small subtle text: '@sticklit'.
```

#### Standard Scene 01 Architecture (The Title Card):
- **Top Center:** Bold hand-drawn comic title centered on pure white:
  ```text
  [Book Title]
  [Author]
  in two minutes
  ```
- **Lower Corner:** Crisp, isolated rectangular graphic of the official book cover.
- **Center:** The main stick figure caught in the core dilemma/metaphor of the book (e.g. facing a fork in the road, trapped in strings, or looking at a broken object).

#### Standard Body Scenes (Visual Metaphors):
- Stick figure actively performing the spoken verb with expressive cartoon face (sweat drops, furrowed brows, happy closed eyes, confident smirk).
- Isolated props only (a wooden work table, a treadmill, an open umbrella, a cash box).

#### Standard Penultimate & Ending Scenes:
- **Penultimate Scene:** Stick figure hero holding the physical book cover, pointing down (`👇`) toward a minimalist banner: *"Get the complete book — link pinned in the top comment"*.
- **Final Scene:** Clean white minimalist end screen: *"Thanks for watching! Follow for more"*, with like/share/comment icons and sponsor badge.

---

### Step 5: User Image Ingestion
- User generates the images in Nano Banana and pastes the download folder path.

---

### Step 6 to 9: 1-Click Unified Assembly & QA
- `organize_images.py` maps images sequentially.
- FFmpeg compiles the CFR 30.00 fps master MP4:
  - White canvas alignment.
  - Burns in 2–4 word white/black phrased subtitles.
  - Mixes ducked ambient background music (-19 dB).
- Automated extraction of 6 verification snapshots to confirm 100% sync.
- Delivery of the final Master MP4 file!
