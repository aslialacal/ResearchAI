# Replace streamlit_app.py with this improved version:

import streamlit as st
import requests
import time
from pathlib import Path

st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🔬 ResearchAI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Multi-Agent Autonomous Research Assistant</p>', unsafe_allow_html=True)

# Sidebar with improved design
with st.sidebar:
    st.markdown("### 🔬 ResearchAI")
    
    st.header("⚙️ Configuration")
    
    max_papers = st.slider(
        "Papers to retrieve",
        min_value=5,
        max_value=20,
        value=10,
        help="More papers = more comprehensive but slower"
    )
    
    api_url = st.text_input(
        "API Endpoint",
        value="http://localhost:8000",
        help="Leave as default unless using remote server"
    )
    
    st.markdown("---")
    st.markdown("### 📊 System Stats")
    st.info("**Data Sources:** 4 APIs  \n**Coverage:** 450M+ papers  \n**Cost:** ~$0.01/query")
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    - Use specific academic terms
    - Include field context
    - Try 2-5 keywords
    - Use quotes for exact phrases
    """)

# Main tabs with icons
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Research Query",
    "📝 Paper Review", 
    "📚 Documentation",
    "🎯 Examples"
])

# ================== TAB 1: RESEARCH ==================
with tab1:
    st.header("Academic Literature Search")
    st.markdown("Search across arXiv, PubMed, Semantic Scholar, and OpenAlex")
    
    # Example queries
    with st.expander("💡 See example queries"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Computer Science:**")
            st.code("transformer architectures in NLP")
            st.code("federated learning privacy")
        with col2:
            st.markdown("**Biomedical:**")
            st.code("CRISPR gene editing off-target effects")
            st.code("mRNA vaccine immunogenicity")
    
    st.markdown("---")
    
    # Search input
    query = st.text_input(
        "🔎 Enter your research question",
        placeholder="e.g., 'quantum error correction topological codes'",
        help="Be specific and use academic terminology for best results"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_button = st.button("🚀 Start Research", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.rerun()
    
    if search_button:
        if not query.strip():
            st.error("⚠️ Please enter a research query")
        elif len(query.strip()) < 10:
            st.warning("💡 Try a more detailed query (at least 10 characters)")
        else:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Searching
                status_text.markdown("🔍 **Step 1/6:** Searching 4 academic databases...")
                progress_bar.progress(10)
                time.sleep(0.5)
                
                # Make API call
                response = requests.post(
                    f"{api_url}/research",
                    json={"query": query, "max_papers": max_papers},
                    timeout=180
                )
                
                progress_bar.progress(20)
                status_text.markdown("💾 **Step 2/6:** Storing in vector database...")
                time.sleep(0.5)
                
                progress_bar.progress(40)
                status_text.markdown("🎯 **Step 3/6:** Finding most relevant papers...")
                time.sleep(0.5)
                
                progress_bar.progress(60)
                status_text.markdown("🤖 **Step 4/6:** AI summarization in progress...")
                time.sleep(1)
                
                progress_bar.progress(80)
                status_text.markdown("🔬 **Step 5/6:** Synthesizing findings...")
                time.sleep(0.5)
                
                progress_bar.progress(90)
                status_text.markdown("✅ **Step 6/6:** Fact-checking and generating report...")
                time.sleep(0.5)
                
                if response.status_code == 200:
                    progress_bar.progress(100)
                    status_text.empty()
                    
                    result = response.json()
                    
                    # Success message with metrics
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success(f"✅ {result['message']}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📄 Papers Found", result.get('papers_found', 'N/A'))
                    with col2:
                        st.metric("💰 API Cost", f"${result.get('cost', 0):.4f}")
                    with col3:
                        st.metric("⏱️ Time", f"~{max_papers * 3}s")
                    with col4:
                        st.metric("🌐 Sources", "4 APIs")
                    
                    st.markdown("---")
                    
                    # Read report files
                    report_path = result['report_file']
                    txt_path = Path(report_path)
                    md_path = txt_path.with_suffix('.md')
                    pdf_path = txt_path.with_suffix('.pdf')
                    
                    with open(report_path, 'r', encoding='utf-8') as f:
                        txt_content = f.read()
                    
                    # Download buttons
                    st.markdown("### 📥 Download Report")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            label="📄 Download TXT",
                            data=txt_content,
                            file_name=txt_path.name,
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with col2:
                        if md_path.exists():
                            with open(md_path, 'r', encoding='utf-8') as f:
                                md_content = f.read()
                            st.download_button(
                                label="📝 Download Markdown",
                                data=md_content,
                                file_name=md_path.name,
                                mime="text/markdown",
                                use_container_width=True
                            )
                    
                    with col3:
                        if pdf_path.exists():
                            with open(pdf_path, 'rb') as f:
                                pdf_content = f.read()
                            st.download_button(
                                label="📕 Download PDF",
                                data=pdf_content,
                                file_name=pdf_path.name,
                                mime="application/pdf",
                                use_container_width=True
                            )
                    
                    st.markdown("---")
                    
                    # Display report with tabs
                    view_tab1, view_tab2 = st.tabs(["📄 Report View", "🔤 Raw Text"])
                    
                    with view_tab1:
                        st.markdown(txt_content)
                    
                    with view_tab2:
                        st.code(txt_content, language=None)
                    
                else:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
            
            except requests.exceptions.ConnectionError:
                progress_bar.empty()
                status_text.empty()
                st.error("❌ **Connection Error:** Cannot reach API. Make sure FastAPI is running on http://localhost:8000")
                st.info("💡 **Troubleshooting:**  \n1. Open terminal  \n2. Navigate to ResearchAI/src  \n3. Run: `python api.py`")
            
            except requests.exceptions.Timeout:
                progress_bar.empty()
                status_text.empty()
                st.error("⏱️ **Timeout:** Request took too long. Try reducing the number of papers.")
            
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ **Unexpected Error:** {str(e)}")
                with st.expander("🐛 Debug Information"):
                    st.code(str(e))

# ================== TAB 2: REVIEW ==================
with tab2:
    st.header("Automated Manuscript Review")
    st.markdown("Upload your manuscript for pre-submission feedback with automated analysis")
    
    st.markdown('<div class="info-box">ℹ️ <b>What this does:</b> Analyzes structure, citations, readability, and provides AI-generated feedback</div>', unsafe_allow_html=True)
    
    # Input options with better UX
    col1, col2 = st.columns([3, 1])
    
    with col1:
        manuscript_title = st.text_input(
            "📑 Manuscript Title",
            placeholder="Enter your paper title (optional)",
            help="This appears in the review report"
        )
    
    with col2:
        input_method = st.radio("Input Method:", ["📝 Paste", "📁 Upload"], horizontal=True)
    
    manuscript_text = ""
    
    if "📝" in input_method:
        manuscript_text = st.text_area(
            "Paste your manuscript below:",
            height=400,
            placeholder="Include: Abstract, Introduction, Methodology, Results, Discussion, Conclusion, References...",
            help="Paste the full text of your manuscript"
        )
        char_count = len(manuscript_text)
        st.caption(f"Character count: {char_count} | Word count: ~{char_count // 5}")
    
    else:
        uploaded_file = st.file_uploader(
            "Upload manuscript file",
            type=['txt'],
            help="Upload a .txt file containing your manuscript"
        )
        if uploaded_file:
            manuscript_text = uploaded_file.read().decode('utf-8')
            st.success(f"✅ Loaded {len(manuscript_text)} characters (~{len(manuscript_text) // 5} words)")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        review_button = st.button("🔍 Generate Review", type="primary", use_container_width=True)
    
    if review_button:
        if len(manuscript_text.strip()) < 100:
            st.error("⚠️ Manuscript too short. Please provide at least 100 characters.")
        else:
            with st.spinner("🤖 AI is analyzing your manuscript..."):
                progress = st.progress(0)
                
                try:
                    progress.progress(25)
                    time.sleep(0.3)
                    
                    response = requests.post(
                        f"{api_url}/review",
                        params={
                            "title": manuscript_title or "Untitled Manuscript",
                            "text": manuscript_text
                        },
                        timeout=120
                    )
                    
                    progress.progress(75)
                    time.sleep(0.3)
                    
                    if response.status_code == 200:
                        progress.progress(100)
                        time.sleep(0.2)
                        progress.empty()
                        
                        result = response.json()
                        
                        st.markdown('<div class="success-box">✅ <b>Review completed successfully!</b></div>', unsafe_allow_html=True)
                        
                        # Metrics dashboard
                        st.markdown("### 📊 Automated Analysis")
                        analysis = result['review']['automated_analysis']
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            score = analysis['structure']['completeness_score']
                            st.metric(
                                "Structure Score",
                                f"{score}%",
                                delta=f"{score - 85}%" if score < 85 else "Good"
                            )
                        
                        with col2:
                            density = analysis['citations']['density_per_1000_words']
                            st.metric(
                                "Citation Density",
                                f"{density:.1f}",
                                delta="per 1k words"
                            )
                        
                        with col3:
                            words = analysis['readability']['word_count']
                            st.metric("Word Count", f"{words:,}")
                        
                        with col4:
                            avg_sent = analysis['readability']['avg_sentence_length']  # Changed from 'average_sentence_length'
                            st.metric("Avg Sentence", f"{avg_sent:.1f} words")
                        
                        st.markdown("---")
                        
                        # Detailed sections in tabs
                        section_tabs = st.tabs(["📋 Full Review", "🏗️ Structure", "📚 Citations", "📖 Readability"])
                        
                        with section_tabs[0]:
                            st.markdown(result['formatted_report'])
                        
                        with section_tabs[1]:
                            struct = analysis['structure']
                            st.markdown(f"**Completeness Score:** {struct['completeness_score']}%")
                            st.markdown("**Sections Found:**")
                            for section, found in struct['sections_found'].items():
                                icon = "✅" if found else "❌"
                                st.markdown(f"{icon} {section.replace('_', ' ').title()}")
                        
                        with section_tabs[2]:
                            cites = analysis['citations']
                            st.metric("Total References", cites['total_citations'])
                            st.metric("Density (per 1000 words)", f"{cites['density_per_1000_words']:.2f}")
                            
                            if cites['density_per_1000_words'] < 10:
                                st.warning("⚠️ Citation density is low. Consider adding more references.")
                            elif cites['density_per_1000_words'] > 50:
                                st.warning("⚠️ Citation density is very high. Ensure proper balance.")
                            else:
                                st.success("✅ Citation density is reasonable.")
                        
                        with section_tabs[3]:
                            read = analysis['readability']
                            st.metric("Total Word Count", f"{read['word_count']:,}")
                            st.metric("Average Sentence Length", f"{read['avg_sentence_length']:.1f} words")
                            st.markdown(f"**Assessment:** {read['clarity_assessment']}")
                        
                        # Download button
                        st.markdown("---")
                        st.download_button(
                            label="📥 Download Review Report",
                            data=result['formatted_report'],
                            file_name=f"review_{manuscript_title[:30] or 'manuscript'}.txt",
                            mime="text/plain",
                            use_container_width=False
                        )
                    
                    else:
                        progress.empty()
                        st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Make sure FastAPI is running.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Disclaimer
    st.markdown("---")
    st.warning("⚠️ **Disclaimer:** This is an automated pre-review tool for preliminary feedback. It does not replace human peer review.")

# ================== TAB 3: DOCUMENTATION ==================
with tab3:
    st.header("📚 System Documentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What is ResearchAI?
        
        ResearchAI is a multi-agent autonomous research system that automates academic literature review:
        
        **Core Capabilities:**
        - 🔍 Multi-source paper search
        - 🧠 Semantic similarity matching
        - 📝 AI-powered summarization
        - 🔬 Cross-paper synthesis
        - ✅ Automated fact-checking
        - 📊 Manuscript review
        - 📄 Multi-format export (TXT/MD/PDF)
        
        ### 🏗️ System Architecture
        
        **6-Step Pipeline:**
        1. **Search** - Query 4 APIs simultaneously
        2. **Store** - Save to vector database
        3. **Retrieve** - Semantic similarity search
        4. **Summarize** - AI extracts key findings
        5. **Synthesize** - Cross-paper analysis
        6. **Fact-Check** - Verify consensus/contradictions
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Data Sources
        
        | Source | Coverage | Specialty |
        |--------|----------|-----------|
        | **arXiv** | 2.3M+ | CS, Physics, Math |
        | **PubMed** | 36M+ | Biomedical |
        | **Semantic Scholar** | 200M+ | All fields |
        | **OpenAlex** | 250M+ | Citations |
        
        ### ⚙️ Technology Stack
        
        - **Backend:** FastAPI + Python
        - **Frontend:** Streamlit
        - **Vector DB:** ChromaDB
        - **Embeddings:** Sentence-Transformers
        - **LLM:** OpenAI GPT-3.5-turbo
        - **Cost:** ~$0.01 per research query
        
        ### 🚀 Performance
        
        - **Speed:** 30-60 seconds per query
        - **Accuracy:** Semantic matching
        - **Scalability:** Handles 5-20 papers
        - **Cost-effective:** < $1 for 100 queries
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Usage Tips
    
    **For Best Results:**
    - ✅ Use specific academic terminology
    - ✅ Include domain context (e.g., "in machine learning")
    - ✅ Try 3-5 keywords per query
    - ✅ Use quotes for exact phrases
    - ❌ Avoid casual language
    - ❌ Don't use overly broad terms
    
    **Query Examples:**
    - Good: "transformer attention mechanisms for machine translation"
    - Bad: "how do transformers work"
    """)

# ================== TAB 4: EXAMPLES ==================
with tab4:
    st.header("🎯 Example Queries & Results")
    
    examples = [
        {
            "field": "Computer Science",
            "query": "few-shot learning meta-learning",
            "description": "Research on learning from limited examples",
            "expected": "Papers on MAML, prototypical networks, matching networks"
        },
        {
            "field": "Biomedical",
            "query": "CAR-T cell therapy solid tumors",
            "description": "Cancer immunotherapy research",
            "expected": "Clinical trials, tumor microenvironment challenges"
        },
        {
            "field": "Physics",
            "query": "topological quantum error correction surface codes",
            "description": "Quantum computing fault tolerance",
            "expected": "Papers on stabilizer codes, logical qubits"
        },
        {
            "field": "Neuroscience",
            "query": "default mode network resting state fMRI",
            "description": "Brain network connectivity studies",
            "expected": "Papers on DMN, functional connectivity, neuroimaging"
        }
    ]
    
    for i, ex in enumerate(examples, 1):
        with st.expander(f"📌 Example {i}: {ex['field']}"):
            st.markdown(f"**Query:** `{ex['query']}`")
            st.markdown(f"**Description:** {ex['description']}")
            st.markdown(f"**Expected Results:** {ex['expected']}")
            
            if st.button(f"🚀 Try This Query", key=f"try_{i}"):
                st.info(f"Copy this query and paste in the Research tab: `{ex['query']}`")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        "<p style='text-align: center; color: gray; font-size: 0.9rem;'>ResearchAI v1.0 | Powered by OpenAI GPT-3.5</p>",
        unsafe_allow_html=True
    )