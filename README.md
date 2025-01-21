# RAG-Based Document Retriever

## Overview

This application is a Retrieval-Augmented Generation (RAG) based document retriever designed to process and retrieve data from various document formats. It is developed using **Python Flask** for the backend and a **ReactJS**-based frontend for a seamless and interactive user experience. The application supports diverse document types, including:

- **Audio**
- **Video**
- **Images**
- **Texts**
- **Webpages**

## Key Features

### 1. Dual Output Modes
The application provides two types of outputs based on user queries:

#### **A. Webpage-Based Output**
- Accumulates all relevant data extracted from the documents.
- Provides:
  - Detailed insights based on the query.
  - Paths to the relevant documents.
  - Links to external internet-based resources.

#### **B. Interactive Graph Output**
- Visualizes the **top 10 results** based on their relevance.
- Uses a custom metric called **strengthMatch** to rank and display results.
  - **strengthMatch** calculates the relevancy of a document to the user's search term.
- Presents data in an interactive graph format for better understanding and exploration.

### 2. Supported Formats
The application can analyze and retrieve data from:
- Text documents (e.g., PDFs, Word documents)
- Images (using OCR for text extraction)
- Audio and Video files (using transcription services)
- Webpages (scraped and indexed for queries)

### 3. User-Friendly Interface
- **Frontend:** Built with ReactJS for an intuitive, responsive, and modern user interface.
- **Backend:** Powered by Python Flask to handle complex queries efficiently.

## Application Workflow

1. **Data Ingestion**
   - Accepts multiple document types via file upload or URL input.
   - Processes files using specialized libraries and tools:
     - Audio/Video: Transcribed using online Speech Vector Transformer models downloaded from `HuggingFace`
     - Images: Processed with OCR libraries utilizes `easyocr`.
     - Webpages: Scraped and parsed using `BeautifulSoup`.

2. **Query Handling**
   - Users input a query via the interface.
   - The system searches for relevant data across all ingested documents.

3. **Relevancy Calculation**
   - Each document is scored based on its match to the query using:
     - Text similarity metrics (e.g., cosine similarity).
     - Advanced transformer-based **Sentence-BERT** for semantic analysis.
   - The results are ranked based on the **strengthMatch** score.

4. **Data Presentation**
   - **Webpage-Based Output:** Displays a comprehensive report including document paths, extracted data, and external links.
   - **Graph Output:** Shows an interactive visualization of the top 10 results based on their relevance.

## Technical Stack

### Backend
- **Python Flask:** API development and server-side logic.
- **NLP and Machine Learning Libraries:**
  - `transformers` for leveraging pre-trained models like `Llama2.3B`
  - `nltk` for natural language processing tasks.
  - `faiss` for efficient vector-based search.
  - `langchain` for LangChain APIs for RAG

### Frontend
- **ReactJS:** For a dynamic and responsive user interface.
- **D3.js:** For interactive graph visualizations.

### Additional Tools and Services
- **Database:**
  - Currently using `CSV` file format for storing document metadata.
- **File Storage:**
  - Currently using a Separate directory as this has not been deployed yet.
- **Logging and Monitoring:**
  -  `Flask-Logging` for debugging and performance tracking.

## Future Enhancements
- **Real-Time Collaboration:** Allow multiple users to collaborate on queries and data visualization.
- **Advanced Search Features:**
  - Utilizes DFS on Knowledge Graphs
  - Fuzzy search capabilities.
- **Enhanced Visualizations:**
  - Add filtering and grouping options to the graph output.
- **Integration with External APIs:**
  - Incorporate more robust transcription and translation services.

## How to Use the Application
1. Upload documents or provide URLs for the content you want to analyze.
2. Input your query into the search bar.
3. Choose your desired output format:
   - Webpage-based output.
   - Interactive graph visualization.
4. View and interact with the results.

---

## Conclusion
This RAG-based document retriever is a powerful tool for analyzing and extracting insights from heterogeneous document types. Its dual-output design ensures both detailed analysis and high-level visualization, making it suitable for a variety of use cases such as research, legal document analysis, and multimedia data exploration.

**Developed By:** Kunj Joshi
