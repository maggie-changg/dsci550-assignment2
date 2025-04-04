# DSCI550 Large Scale Data Extraction & Analysis for Haunted Places

**Repository for DSCI 550 Group 2**  
**Collaborators:** Eleanor Bi, Maggie Chang, Jessica Deng, Tarun Jagadish, Aaron Kuo, Hengxiao Zhu

---

## Project Overview

This project explores the intersection of large-scale data extraction and AI-driven multimedia analysis in the context of haunted places. We investigate geographic, thematic, and visual patterns across thousands of haunted place descriptions using natural language processing, image generation, and captioning technologies. By combining text and image modalities, we uncover both spatial and narrative consistencies in the portrayal of hauntings.

---

## Key Achievements

- **Geographic Analysis**: Identified location patterns and correlations in haunted place reports
- **Named Entity Recognition**: Extracted and analyzed entities using SpaCy
- **AI Image Generation**: Created visual representations of haunted locations using Stable Diffusion
- **Image Analysis**: Applied Tika's image captioning and object detection to analyze generated visuals
- **Pattern Discovery**: Uncovered thematic and geographic clusters of paranormal phenomena

---

## Division of Work

### Content Areas

1. **Text Analysis & Location Extraction (Maggie Chang, Jessica Deng)**
   - Implementation of GeoTopicParser for location extraction
   - Named Entity Recognition using SpaCy
   - Analysis of geographic patterns and correlations
   - Entity categorization and validation
   - Geographic clustering analysis

2. **Image Generation & Prompt Engineering (Eleanor Bi, Hengxiao Zhu)**
   - Creation of text prompts from haunted place descriptions
   - Generation of images using Stable Diffusion
   - Image storage and management
   - Conversion of text descriptions to visual representations
   - Evaluation of image quality and relevance

3. **Image Analysis & Object Detection (Tarun Jagadish, Aaron Kuo)**
   - Implementation of Tika Image Dockers
   - Image captioning using Show & Tell
   - Object detection using Inception REST service
   - Integration of image analysis results with dataset
   - Comparison of image content with textual descriptions

---

## Technologies Used

### Text Processing
- **Apache Tika**: Document parsing and metadata extraction
- **GeoTopicParser**: Location extraction and geocoding
- **SpaCy**: Named entity recognition (NER)

### Image Processing
- **Stable Diffusion**: AI-based image generation
- **Apache Tika Dockers**:
  - **Show & Tell**: Image captioning
  - **Inception REST**: Object detection

---

## Key Findings

### Geographic Patterns

Our analysis revealed significant geographic clustering in haunted place reports:

- Certain locations appear frequently in the data (15-20 separate entries), including:
  - Stann Creek District
  - Washington
  - Prince George's County
  - Kentucky

- Major urban hotspots emerged with multiple unique haunted locations:
  - Los Angeles (58 locations)
  - San Antonio (50 locations)
  - Columbus (39 locations)

- 1,696 cities had multiple haunted place entries, suggesting non-random distribution

### Entity Recognition Analysis

SpaCy NER provided valuable insights into the dataset:

- Identified various location types:
  - **GPE**: Countries, cities, or states
  - **LOC**: Non-country/city/state locations (e.g., "Rogue River")
  - **FAC**: Specific buildings or infrastructure (e.g., "Garden City High School")

- 22% of entries (2,381 rows) contained at least one location-related entity

- Some limitations were observed:
  - Occasional misclassification (e.g., "Hell's Bridge" labeled as an organization)
  - Time entities captured relative references missed by date parsers
  - Variable reliability for witness count validation

### Image Analysis

Our implementation of AI image generation and analysis revealed:

- Image captions typically captured general scenes but lacked specificity for haunted themes
- Object detection identified contextually relevant items but sometimes overgeneralized
- Black and white images were correctly identified as such
- Visual ambiguity (e.g., low lighting, shadows) occasionally led to misinterpretations
- Caption models tended to produce similar variations regardless of confidence levels

---

## Implementation Details

### Data Processing Pipeline

1. **Dataset Preparation**:
   - Created v2 version of our dataset from Assignment 1
   - Added columns for GeoTopic data, SpaCy entities, image references, captions, and detected objects

2. **Location Extraction**:
   - Implemented GeoTopicParser to identify location mentions
   - Extracted and geocoded locations from text descriptions

3. **Entity Recognition**:
   - Applied SpaCy to identify entities in haunted place descriptions
   - Categorized entities (persons, organizations, dates, locations)

4. **Image Generation**:
   - Created prompts from haunted place descriptions
   - Generated corresponding images using Stable Diffusion

5. **Image Analysis**:
   - Processed generated images with Tika's Show & Tell for captions
   - Used Tika's Inception REST service for object detection
   - Integrated results back into the dataset

### Thematic Analysis

Our keyword analysis identified common terms across haunted place descriptions:
- "room"
- "floor"
- "school"
- "ghost"
- "night"

These recurring terms suggest consistent narrative patterns in paranormal storytelling across different geographic locations.

---

## Challenges and Limitations

### Technical Challenges

- **GeoTopicParser Setup**: Initial configuration required troubleshooting errors and server setup
- **SpaCy Limitations**: Pre-trained model occasionally misclassified entities
- **Image Caption Quality**: Captions often remained vague or overly general
- **Object Detection Precision**: Detection sometimes identified contextually similar but absent objects

### Data Challenges

- Entity recognition for witness validation was inconsistent
- Some location names were misclassified
- Image captions rarely highlighted haunted or paranormal themes
- Caption models relied heavily on easily detectable features

---

## Project Structure
```
project/
│
├── data/
│   ├── raw/                     # Original haunted places dataset
│   ├── processed/               # Enhanced dataset with new features
│   └── images/                  # Generated haunted place images
│
├── source_code/
│   ├── geolocation/             # GeoTopicParser implementation
│   ├── entity_recognition/      # SpaCy implementation
│   ├── image_generation/        # Stable Diffusion scripts
│   └── image_analysis/          # Tika image captioning and object detection
│
├── notebooks/                   # Analysis notebooks
│
├── results/                     # Visualizations and analysis outputs
│
├── README.md                    # Project documentation
└── requirements.txt             # Project dependencies
```
---

## Getting Started

### Prerequisites
- Python 3.8+
- Apache Tika
- GeoTopicParser and Lucene GeoGazetteer
- SpaCy
- Stable Diffusion
- Docker for Tika image services

### Installation

```bash
# Clone the repository
git clone https://github.com/[username]/dsci550-haunted-places.git

# Install dependencies
pip install -r requirements.txt

# Set up GeoTopicParser
# Instructions at https://cwiki.apache.org/confluence/display/tika/GeoTopicParser

# Install SpaCy
pip install spacy
python -m spacy download en_core_web_sm

# Set up Tika Image Dockers
git clone https://github.com/USCDataScience/tika-dockers.git
# Follow instructions for Docker setup
```
---

## Conclusion

Our multi-modal analysis of haunted places revealed significant geographic and thematic patterns. The combination of NLP techniques, entity recognition, and image analysis provided complementary insights into the dataset. While we encountered some technical limitations with pre-trained models and general-purpose image captioning, the overall approach successfully identified spatial clusters and narrative consistencies in haunted place reports.

The project demonstrates the value of combining text and image analysis for pattern discovery in domain-specific datasets. Future work could explore fine-tuning models for paranormal or haunting-specific content to improve entity recognition and image captioning relevance.
