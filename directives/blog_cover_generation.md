# Blog Cover Photo Generation Directive

## Goal
Generate natural, clean, attention-grabbing cover photos for blog articles using Nano Banana Pro (Gemini 3 Pro Image). Each cover should be relevant to the article's title and content.

## Inputs
- **Article title**: The headline of the blog post
- **Article content**: The full text content (used to understand context)
- **Output path**: Where to save the generated image

## Tools/Scripts
- `execution/generate_blog_cover.py` - Main script for generating cover images

## Process

### Step 1: Analyze Article Content
Extract key themes from the article:
- Main topic (FERS, TSP, Social Security, etc.)
- Emotional tone (educational, urgent, reassuring)
- Key concepts or imagery that could be visualized

### Step 2: Generate Image Prompt
Create a descriptive prompt that:
- Describes a scene relevant to the article topic
- Uses natural, clean aesthetics (avoid overly branded/corporate looks)
- Requests photorealistic, editorial photography style
- Leaves space for potential text overlay
- Avoids text in the image itself (we'll overlay text separately if needed)

### Step 3: Call Nano Banana Pro API
- Model: `gemini-3-pro-image-preview`
- Aspect ratio: `16:9` (optimal for blog cards)
- Image size: `2K` for high quality
- Response modality: `IMAGE`

### Step 4: Save Output
- Save to `public/images/blog/covers/{slug}.png`
- Log success/failure

## Prompt Engineering Guidelines

### Good Prompts (Natural & Clean)
```
"A serene morning scene of a professional reviewing documents at a sunlit desk,
with a cup of coffee nearby. Warm natural lighting, shallow depth of field,
editorial photography style. The mood is contemplative and optimistic."
```

### Avoid
- Overly corporate stock photo aesthetics
- Busy, cluttered compositions
- Text or words in the image
- Obviously AI-generated artifacts
- Unnatural colors or lighting

### Topic-Specific Imagery Ideas
- **FERS/Retirement**: Peaceful retirement scenes, morning routines, nature walks, family moments
- **TSP/Investing**: Growth imagery (plants, sunrise), charts on screens (subtle), planning sessions
- **Tax Strategy**: Organized desk scenes, calculators, paperwork in natural light
- **Federal News**: Washington DC landmarks (subtle), official buildings, newspapers
- **Social Security**: Multigenerational family scenes, comfortable home settings

## Output
- PNG file at specified path
- Aspect ratio: 16:9
- Resolution: 2K (approximately 2048x1152)

## Edge Cases
- **API rate limits**: Wait and retry with exponential backoff
- **Content policy rejection**: Try alternate prompt focusing on abstract/metaphorical imagery
- **Generation failure**: Log error, skip article, continue with others

## Environment Variables Required
- `GEMINI_API_KEY` - Google Gemini API key

## Example Usage
```bash
python execution/generate_blog_cover.py --slug "fers-retirement-planning" --title "FERS Retirement Planning Guide" --content "Article content here..."
```

Or batch mode:
```bash
python execution/generate_blog_cover.py --batch --input articles.json
```
