#!/usr/bin/env python3
"""
Streamlit Web Interface for LNA Bot - AI-Powered Training Recommendations

This application provides a user-friendly web interface for the LNA Bot,
allowing users to upload CSV/Excel files, analyze training needs, and
visualize recommendations.
"""

import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import io
import json
from datetime import datetime

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from lna_bot import LNABot, LNABotError
    from lna_bot.models import LNARecord, LNAAnalysisResult, DatasetSummary, PriorityLevel, CompetencyType, RequestType
except ImportError as e:
    st.error(f"Failed to import LNA Bot modules: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="LNA Bot - Training Recommendations",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'bot' not in st.session_state:
        st.session_state.bot = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'dataset_summary' not in st.session_state:
        st.session_state.dataset_summary = None
    if 'uploaded_file_name' not in st.session_state:
        st.session_state.uploaded_file_name = None
    if 'processing_stats' not in st.session_state:
        st.session_state.processing_stats = None

def initialize_bot():
    """Initialize the LNA Bot with error handling."""
    try:
        if st.session_state.bot is None:
            with st.spinner("Initializing LNA Bot..."):
                st.session_state.bot = LNABot()
        return True
    except Exception as e:
        st.error(f"Failed to initialize LNA Bot: {str(e)}")
        st.error("Please check your configuration files in the 'config' directory.")
        return False

def display_header():
    """Display the application header."""
    st.markdown('<h1 class="main-header">🤖 LNA Bot - AI-Powered Training Recommendations</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Quick info about the bot
    with st.expander("ℹ️ About LNA Bot", expanded=False):
        st.markdown("""
        **LNA Bot** analyzes Learning Need Analysis reports and provides intelligent recommendations for training delivery methods:
        
        - **External Training** (≤10 trainees): Cost-effective for small groups
        - **Special Development Program (SDP)** (11-50 trainees): Balanced approach for medium groups  
        - **In-house Training** (>50 trainees): Efficient for large groups
        - **Niche Competency Override**: SDP recommended for specialized skills regardless of group size
        """)

def file_upload_section():
    """Handle file upload and processing."""
    st.header("📁 File Upload & Analysis")
    
    # Create tabs for file upload and sample datasets
    upload_tab, sample_tab = st.tabs(["📤 Upload Your File", "🎯 Sample Datasets"])
    
    with upload_tab:
        # File upload
        uploaded_file = st.file_uploader(
            "Choose your LNA report file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload a CSV or Excel file containing LNA data"
        )
        
        if uploaded_file is not None:
            process_uploaded_file(uploaded_file)
    
    with sample_tab:
        st.write("**Quick test with pre-configured sample datasets:**")
        st.info("These datasets are designed to showcase different aspects of the LNA Bot's capabilities.")
        
        # Sample dataset options
        sample_datasets = {
            "🏢 Multi-Industry Comprehensive": {
                "file": "comprehensive_multi_industry_lna.csv",
                "description": "25 records across different industries (Healthcare, Technology, Finance)",
                "highlights": "• Mixed training types • 3-280 trainees range • All priority levels",
                "expected": "24% External, 40% SDP, 36% In-house"
            },
            "🚀 Niche Competencies": {
                "file": "niche_competencies_stress_test.csv", 
                "description": "25 records focused on specialized/niche competencies",
                "highlights": "• Quantum Computing, AI Ethics, Blockchain • SDP override testing",
                "expected": "96% SDP (niche override), 4% External"
            },
            "🏭 Large-Scale Training": {
                "file": "large_scale_training_scenarios.csv",
                "description": "25 records with large trainee groups (55-500 people)",
                "highlights": "• Enterprise-scale programs • In-house training focus",
                "expected": "100% In-house (all >50 trainees)"
            },
            "👥 Small Group Edge Cases": {
                "file": "small_group_edge_cases.csv",
                "description": "25 records with very small groups (1-4 trainees)",
                "highlights": "• Individual training • Executive coaching • External focus",
                "expected": "100% External (all ≤10 trainees)"
            },
            "💼 Business Competencies Mix": {
                "file": "business_competencies_mix.csv",
                "description": "25 realistic business competency scenarios",
                "highlights": "• Quality Control, Risk Management • Balanced distribution",
                "expected": "20% External, 48% SDP, 32% In-house"
            },
            "⚠️ Error Handling Test": {
                "file": "data_validation_error_cases.csv",
                "description": "25 records with intentional errors for robustness testing",
                "highlights": "• Missing fields • Invalid values • Error recovery",
                "expected": "60% success rate (15/25 processed)"
            },
            "📊 Excel Multi-Sheet": {
                "file": "multi_sheet_comprehensive_test.xlsx",
                "description": "Excel workbook with 3 sheets (75 total records)",
                "highlights": "• Multi-sheet processing • Combined analysis • Excel functionality",
                "expected": "9% External, 45% SDP, 46% In-house"
            }
        }
        
        # Display sample datasets in a grid
        for name, details in sample_datasets.items():
            with st.expander(f"{name} - {details['description']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Key Features:**")
                    st.write(details['highlights'])
                    st.write(f"**Expected Results:** {details['expected']}")
                
                with col2:
                    dataset_path = Path(f"data/test_datasets/{details['file']}")
                    if st.button(f"📊 Load Dataset", key=f"load_{details['file']}", type="secondary"):
                        if dataset_path.exists():
                            process_sample_dataset(dataset_path, name)
                        else:
                            st.error(f"Sample dataset not found: {dataset_path}")

def process_uploaded_file(uploaded_file):
    """Process an uploaded file."""
    # Display file info
    file_details = {
        "Filename": uploaded_file.name,
        "File Type": uploaded_file.type,
        "File Size": f"{uploaded_file.size} bytes"
    }
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Filename", file_details["Filename"])
    with col2:
        st.metric("File Type", file_details["File Type"])
    with col3:
        st.metric("File Size", file_details["File Size"])
    
    # Process file button
    if st.button("🔍 Analyze File", type="primary"):
        if not initialize_bot():
            return
        
        try:
            with st.spinner("Processing your file... This may take a moment."):
                # Save uploaded file temporarily
                temp_file_path = Path(f"temp_{uploaded_file.name}")
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Analyze the file with statistics
                results, summary, processing_stats = st.session_state.bot.analyze_file_with_stats(temp_file_path)
                
                # Store results in session state
                st.session_state.analysis_results = results
                st.session_state.dataset_summary = summary
                st.session_state.processing_stats = processing_stats
                st.session_state.uploaded_file_name = uploaded_file.name
                
                # Clean up temp file
                temp_file_path.unlink()
                
                # Display processing statistics
                display_processing_statistics(processing_stats, uploaded_file.name)
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            if temp_file_path.exists():
                temp_file_path.unlink()

def process_sample_dataset(dataset_path: Path, dataset_name: str):
    """Process a sample dataset."""
    if not initialize_bot():
        return
    
    try:
        with st.spinner(f"Loading {dataset_name}... This may take a moment."):
            # Analyze the sample dataset with statistics
            results, summary, processing_stats = st.session_state.bot.analyze_file_with_stats(dataset_path)
            
            # Store results in session state
            st.session_state.analysis_results = results
            st.session_state.dataset_summary = summary
            st.session_state.processing_stats = processing_stats
            st.session_state.uploaded_file_name = dataset_path.name
            
            # Display processing statistics
            display_processing_statistics(processing_stats, dataset_name)
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Failed to load {dataset_name}: {str(e)}")


def display_processing_statistics(processing_stats, file_name: str):
    """Display processing statistics and warnings."""
    
    # Success message with statistics
    if processing_stats.success_rate == 100.0:
        st.success(f"✅ **{file_name}** processed successfully! All {processing_stats.successful_records} records loaded.")
    else:
        st.warning(f"⚠️ **{file_name}** processed with some issues. {processing_stats.successful_records} out of {processing_stats.total_rows} records loaded ({processing_stats.success_rate:.1f}% success rate).")
    
    # Show detailed statistics in expandable section if there are issues
    if processing_stats.has_errors or processing_stats.has_warnings:
        with st.expander("📊 Processing Details", expanded=processing_stats.success_rate < 90):
            
            # Processing summary
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rows", processing_stats.total_rows)
            with col2:
                st.metric("✅ Successful", processing_stats.successful_records)
            with col3:
                st.metric("❌ Failed", processing_stats.failed_records)
            with col4:
                st.metric("Success Rate", f"{processing_stats.success_rate:.1f}%")
            
            # Show validation warnings if any
            if processing_stats.has_warnings:
                st.subheader("⚠️ Data Validation Warnings")
                for warning in processing_stats.validation_warnings:
                    st.warning(f"📋 {warning}")
            
            # Show processing errors if any
            if processing_stats.has_errors:
                st.subheader("❌ Processing Errors")
                st.info("The following rows could not be processed due to missing or invalid data:")
                
                for error in processing_stats.processing_errors[:10]:  # Show first 10 errors
                    st.error(f"🔍 {error}")
                
                if len(processing_stats.processing_errors) > 10:
                    st.info(f"... and {len(processing_stats.processing_errors) - 10} more errors")
                
                # Recommendations
                st.subheader("💡 Recommendations")
                st.info("""
                **To improve data quality:**
                - Ensure all required columns are present: Submission, Priority, Competency type, etc.
                - Check date formats (DD/MM/YYYY or similar standard formats)
                - Verify priority levels are: High, Medium, or Low
                - Ensure numeric fields like 'Number of trainees' contain valid numbers
                - Remove or fix rows with missing critical information
                """)
    
    # Show success summary even for perfect processing
    elif processing_stats.success_rate == 100.0:
        with st.expander("📊 Processing Summary"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Records", processing_stats.successful_records)
            with col2:
                st.metric("Success Rate", "100%")

def display_summary_metrics():
    """Display summary metrics from the analysis."""
    if st.session_state.dataset_summary is None:
        return
    
    st.header("📊 Analysis Summary")
    
    summary = st.session_state.dataset_summary
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Records",
            value=summary.total_entries,
            help="Number of LNA records processed"
        )
    
    with col2:
        avg_trainees = summary.average_trainees_per_entry
        st.metric(
            label="Avg. Trainees",
            value=f"{avg_trainees:.1f}",
            help="Average number of trainees per record"
        )
    
    with col3:
        total_trainees = summary.total_trainees
        st.metric(
            label="Total Trainees",
            value=f"{total_trainees:,}",
            help="Total number of trainees across all records"
        )
    
    with col4:
        high_priority = summary.priority_distribution.get('High', 0)
        st.metric(
            label="High Priority",
            value=high_priority,
            help="Number of high priority training requests"
        )

def display_training_distribution():
    """Display training type distribution charts."""
    if st.session_state.dataset_summary is None:
        return
    
    st.header("📈 Training Type Distribution")
    
    summary = st.session_state.dataset_summary
    training_dist = summary.training_type_distribution
    
    if not training_dist:
        st.warning("No training distribution data available.")
        return
    
    # Convert enum keys to string values if needed
    processed_dist = {}
    for k, v in training_dist.items():
        key = k.value if hasattr(k, 'value') else str(k)
        processed_dist[key] = v
    
    training_dist = processed_dist
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        fig_pie = px.pie(
            values=list(training_dist.values()),
            names=list(training_dist.keys()),
            title="Training Type Distribution",
            color_discrete_sequence=['#ff7f0e', '#2ca02c', '#1f77b4']
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart
        fig_bar = px.bar(
            x=list(training_dist.keys()),
            y=list(training_dist.values()),
            title="Training Type Counts",
            color=list(training_dist.keys()),
            color_discrete_sequence=['#ff7f0e', '#2ca02c', '#1f77b4']
        )
        fig_bar.update_layout(showlegend=False, xaxis_title="Training Type", yaxis_title="Count")
        st.plotly_chart(fig_bar, use_container_width=True)

def display_priority_distribution():
    """Display priority level distribution."""
    if st.session_state.dataset_summary is None:
        return
    
    st.header("🎯 Priority Level Analysis")
    
    summary = st.session_state.dataset_summary
    priority_dist = summary.priority_distribution
    
    if not priority_dist:
        st.warning("No priority distribution data available.")
        return
    
    # Convert enum keys to string values if needed
    processed_priority_dist = {}
    for k, v in priority_dist.items():
        key = k.value if hasattr(k, 'value') else str(k)
        processed_priority_dist[key] = v
    
    priority_dist = processed_priority_dist
    
    # Priority distribution chart
    fig = px.bar(
        x=list(priority_dist.keys()),
        y=list(priority_dist.values()),
        title="Priority Level Distribution",
        color=list(priority_dist.keys()),
        color_discrete_map={
            'High': '#dc3545',
            'Medium': '#ffc107', 
            'Low': '#28a745'
        }
    )
    fig.update_layout(showlegend=False, xaxis_title="Priority Level", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

def display_competency_analysis():
    """Display competency-based analysis."""
    if st.session_state.analysis_results is None:
        return
    
    st.header("🎯 Competency Analysis")
    
    results = st.session_state.analysis_results
    
    # Extract competency data
    competency_data = []
    for result in results:
        record = result.record
        recommendation = result.recommendation
        
        competency_data.append({
            'competency': record.targeted_competencies,
            'trainees': record.estimated_trainees,
            'training_type': recommendation.training_type.value if hasattr(recommendation.training_type, 'value') else str(recommendation.training_type),
            'classification': recommendation.competency_classification.value if hasattr(recommendation.competency_classification, 'value') else str(recommendation.competency_classification),
            'demand_score': recommendation.demand_score,
            'department': record.department,
            'priority': record.priority.value if hasattr(record.priority, 'value') else str(record.priority)
        })
    
    df = pd.DataFrame(competency_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Competency classification distribution
        classification_counts = df['classification'].value_counts()
        fig_classification = px.pie(
            values=classification_counts.values,
            names=classification_counts.index,
            title="Competency Classification Distribution",
            color_discrete_map={
                'niche': '#ff7f0e',
                'common': '#2ca02c'
            }
        )
        st.plotly_chart(fig_classification, use_container_width=True)
    
    with col2:
        # Training demand by competency (top 10)
        demand_by_comp = df.groupby('competency')['trainees'].sum().sort_values(ascending=False).head(10)
        fig_demand = px.bar(
            x=demand_by_comp.values,
            y=demand_by_comp.index,
            orientation='h',
            title="Top 10 Competencies by Training Demand",
            labels={'x': 'Total Trainees', 'y': 'Competency'}
        )
        fig_demand.update_layout(height=400)
        st.plotly_chart(fig_demand, use_container_width=True)

def display_departmental_analysis():
    """Display department-based analysis."""
    if st.session_state.analysis_results is None:
        return
    
    st.header("🏢 Departmental Analysis")
    
    results = st.session_state.analysis_results
    
    # Extract departmental data
    dept_data = []
    for result in results:
        record = result.record
        recommendation = result.recommendation
        
        dept_data.append({
            'department': record.department,
            'division': record.division,
            'trainees': record.estimated_trainees,
            'training_type': recommendation.training_type.value if hasattr(recommendation.training_type, 'value') else str(recommendation.training_type),
            'priority': record.priority.value if hasattr(record.priority, 'value') else str(record.priority),
            'competency': record.targeted_competencies
        })
    
    df = pd.DataFrame(dept_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Training demand by department
        dept_demand = df.groupby('department')['trainees'].sum().sort_values(ascending=False)
        fig_dept = px.bar(
            x=dept_demand.values,
            y=dept_demand.index,
            orientation='h',
            title="Training Demand by Department",
            labels={'x': 'Total Trainees', 'y': 'Department'}
        )
        st.plotly_chart(fig_dept, use_container_width=True)
    
    with col2:
        # Training type distribution by department
        dept_training = pd.crosstab(df['department'], df['training_type'])
        fig_stacked = px.bar(
            dept_training,
            title="Training Types by Department",
            labels={'value': 'Count', 'index': 'Department'}
        )
        fig_stacked.update_layout(barmode='stack')
        st.plotly_chart(fig_stacked, use_container_width=True)

def display_cost_analysis():
    """Display cost analysis and projections."""
    if st.session_state.analysis_results is None:
        return
    
    st.header("💰 Cost Analysis & Projections")
    
    results = st.session_state.analysis_results
    
    # Cost estimation factors (these could be configurable)
    cost_factors = {
        'External': {'per_person': 2000, 'fixed_cost': 500},
        'SDP': {'per_person': 1200, 'fixed_cost': 5000},
        'In-house': {'per_person': 800, 'fixed_cost': 15000}
    }
    
    # Calculate costs
    cost_data = []
    total_cost = 0
    
    for result in results:
        record = result.record
        recommendation = result.recommendation
        
        training_type = recommendation.training_type.value if hasattr(recommendation.training_type, 'value') else str(recommendation.training_type)
        trainees = record.estimated_trainees
        
        if training_type in cost_factors:
            per_person = cost_factors[training_type]['per_person']
            fixed = cost_factors[training_type]['fixed_cost']
            estimated_cost = (trainees * per_person) + fixed
        else:
            estimated_cost = trainees * 1000  # Fallback
        
        cost_data.append({
            'id': record.id,
            'competency': record.targeted_competencies,
            'training_type': training_type,
            'trainees': trainees,
            'estimated_cost': estimated_cost,
            'cost_per_person': estimated_cost / trainees if trainees > 0 else 0
        })
        
        total_cost += estimated_cost
    
    cost_df = pd.DataFrame(cost_data)
    
    # Display cost metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Estimated Cost",
            value=f"${total_cost:,.0f}",
            help="Total estimated cost for all training programs"
        )
    
    with col2:
        avg_cost_per_program = total_cost / len(results) if results else 0
        st.metric(
            label="Avg Cost per Program",
            value=f"${avg_cost_per_program:,.0f}",
            help="Average cost per training program"
        )
    
    with col3:
        total_trainees = sum(r.record.estimated_trainees for r in results)
        cost_per_trainee = total_cost / total_trainees if total_trainees > 0 else 0
        st.metric(
            label="Cost per Trainee",
            value=f"${cost_per_trainee:.0f}",
            help="Average cost per individual trainee"
        )
    
    with col4:
        # Cost by training type
        cost_by_type = cost_df.groupby('training_type')['estimated_cost'].sum()
        most_expensive = cost_by_type.idxmax() if not cost_by_type.empty else "N/A"
        st.metric(
            label="Most Expensive Type",
            value=most_expensive,
            help="Training type with highest total cost"
        )
    
    # Cost breakdown charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost by training type
        cost_by_type = cost_df.groupby('training_type')['estimated_cost'].sum()
        fig_cost_type = px.pie(
            values=cost_by_type.values,
            names=cost_by_type.index,
            title="Cost Distribution by Training Type"
        )
        st.plotly_chart(fig_cost_type, use_container_width=True)
    
    with col2:
        # Top 10 most expensive programs
        top_expensive = cost_df.nlargest(10, 'estimated_cost')
        fig_expensive = px.bar(
            top_expensive,
            x='estimated_cost',
            y='competency',
            orientation='h',
            title="Top 10 Most Expensive Programs",
            labels={'estimated_cost': 'Estimated Cost ($)', 'competency': 'Competency'}
        )
        st.plotly_chart(fig_expensive, use_container_width=True)
    
    # Detailed cost table
    with st.expander("📊 Detailed Cost Breakdown"):
        st.dataframe(
            cost_df[['competency', 'training_type', 'trainees', 'estimated_cost', 'cost_per_person']],
            use_container_width=True,
            hide_index=True
        )

def display_detailed_results():
    """Display detailed analysis results in a table."""
    if st.session_state.analysis_results is None:
        return
    
    st.header("📋 Detailed Analysis Results")
    
    results = st.session_state.analysis_results
    
    # Convert results to DataFrame for display
    data = []
    for result in results:
        record = result.record
        recommendation = result.recommendation
        
        data.append({
            'ID': record.id,
            'Competency': record.targeted_competencies,
            'Trainees': record.estimated_trainees,
            'Priority': record.priority.value if hasattr(record.priority, 'value') else str(record.priority),
            'Training Type': recommendation.training_type.value if hasattr(recommendation.training_type, 'value') else str(recommendation.training_type),
            'Classification': recommendation.competency_classification.value if hasattr(recommendation.competency_classification, 'value') else str(recommendation.competency_classification),
            'Demand Score': f"{recommendation.demand_score:.2f}",
            'Department': record.department,
            'Division': record.division
        })
    
    df = pd.DataFrame(data)
    
    # Add filters
    with st.expander("🔍 Filter Results", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            priority_filter = st.multiselect(
                "Priority Level",
                options=df['Priority'].unique(),
                default=df['Priority'].unique()
            )
        
        with col2:
            training_filter = st.multiselect(
                "Training Type",
                options=df['Training Type'].unique(),
                default=df['Training Type'].unique()
            )
        
        with col3:
            classification_filter = st.multiselect(
                "Classification",
                options=df['Classification'].unique(),
                default=df['Classification'].unique()
            )
        
        # Apply filters
        filtered_df = df[
            (df['Priority'].isin(priority_filter)) &
            (df['Training Type'].isin(training_filter)) &
            (df['Classification'].isin(classification_filter))
        ]
    
    # Display filtered results
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Show filtered count
    if len(filtered_df) != len(df):
        st.info(f"Showing {len(filtered_df)} of {len(df)} records")

def single_record_analysis():
    """Interactive single record analysis section."""
    st.header("🔍 Single Record Analysis")
    st.write("Analyze individual training requests in real-time")
    
    if not initialize_bot():
        return
    
    with st.form("single_record_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            competency = st.text_input(
                "Competency Name",
                placeholder="e.g., Patient Safety, Data Analytics, Cloud Computing",
                help="Enter the name of the competency or skill to be trained"
            )
            
            trainees = st.number_input(
                "Number of Trainees",
                min_value=1,
                max_value=1000,
                value=25,
                help="Estimated number of people who need this training"
            )
            
            priority = st.selectbox(
                "Priority Level",
                options=["High", "Medium", "Low"],
                index=1,
                help="How urgent is this training requirement?"
            )
        
        with col2:
            department = st.text_input(
                "Department",
                value="Test Department",
                help="Department requesting the training"
            )
            
            division = st.text_input(
                "Division",
                value="Test Division", 
                help="Division requesting the training"
            )
            
            audience = st.text_input(
                "Target Audience",
                placeholder="e.g., Software Engineers, Managers, All Staff",
                help="Who will receive this training?"
            )
        
        submit_button = st.form_submit_button("🎯 Get Recommendation", type="primary")
        
        if submit_button and competency:
            try:
                with st.spinner("Analyzing your request..."):
                    # Create a single LNA record
                    record = LNARecord(
                        id=f"MANUAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        submission=datetime.now(),
                        priority=PriorityLevel(priority),
                        competency_type=CompetencyType.TECHNICAL,
                        job_families="Manual Entry",
                        targeted_competencies=competency,
                        request_type=RequestType.NEW_TRAINING,
                        targeted_audience=audience or "Manual Entry",
                        estimated_trainees=trainees,
                        comment="Single record analysis via Streamlit interface",
                        year=2024,
                        division=division,
                        department=department,
                        section="Manual Entry"
                    )
                    
                    # Analyze the record
                    result = st.session_state.bot.analyze_single_record(record)
                    
                    # Display results
                    st.success("✅ Analysis Complete!")
                    
                    # Results in columns
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        training_type = result.recommendation.training_type.value if hasattr(result.recommendation.training_type, 'value') else str(result.recommendation.training_type)
                        st.metric(
                            label="Recommended Training",
                            value=training_type,
                            help="Recommended training delivery method"
                        )
                    
                    with col2:
                        classification = result.recommendation.competency_classification.value if hasattr(result.recommendation.competency_classification, 'value') else str(result.recommendation.competency_classification)
                        st.metric(
                            label="Competency Type",
                            value=classification.title(),
                            help="Whether this is a niche or common competency"
                        )
                    
                    with col3:
                        st.metric(
                            label="Demand Score",
                            value=f"{result.recommendation.demand_score:.2f}",
                            help="Priority-based demand score (higher = more urgent)"
                        )
                    
                    with col4:
                        skills_count = len(result.recommendation.associated_skills)
                        st.metric(
                            label="Related Skills",
                            value=skills_count,
                            help="Number of related skills identified"
                        )
                    
                    # Reasoning box
                    st.subheader("🤔 Recommendation Reasoning")
                    st.info(result.recommendation.reasoning)
                    
                    # Associated skills if available
                    if result.recommendation.associated_skills:
                        st.subheader("🎯 Associated Skills")
                        
                        # Show skills in a nice format
                        skills_to_show = result.recommendation.associated_skills[:10]  # Show first 10
                        skills_cols = st.columns(2)
                        
                        for i, skill in enumerate(skills_to_show):
                            with skills_cols[i % 2]:
                                st.write(f"• {skill}")
                        
                        if len(result.recommendation.associated_skills) > 10:
                            with st.expander(f"View all {len(result.recommendation.associated_skills)} skills"):
                                for skill in result.recommendation.associated_skills:
                                    st.write(f"• {skill}")
                    
                    # Cost implications
                    st.subheader("💰 Training Method Implications")
                    
                    implications = {
                        "External": {
                            "icon": "🏢",
                            "cost": "Higher per-person cost",
                            "benefits": "Access to specialized expertise, networking opportunities",
                            "timeline": "Flexible scheduling, immediate availability"
                        },
                        "SDP": {
                            "icon": "🎓", 
                            "cost": "Moderate cost, balanced approach",
                            "benefits": "Customized content, internal knowledge retention",
                            "timeline": "Medium development time, scheduled delivery"
                        },
                        "In-house": {
                            "icon": "🏠",
                            "cost": "Lower per-person cost for large groups",
                            "benefits": "Full customization, internal expertise building",
                            "timeline": "Longer development time, maximum flexibility"
                        }
                    }
                    
                    if training_type in implications:
                        impl = implications[training_type]
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**{impl['icon']} Cost Consideration**")
                            st.write(impl['cost'])
                        
                        with col2:
                            st.write(f"**✅ Key Benefits**")
                            st.write(impl['benefits'])
                        
                        with col3:
                            st.write(f"**⏱️ Timeline**")
                            st.write(impl['timeline'])
                    
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
        
        elif submit_button and not competency:
            st.warning("⚠️ Please enter a competency name to analyze.")

def display_export_options():
    """Display export options for analysis results."""
    if st.session_state.analysis_results is None:
        return
    
    st.header("💾 Export Results")
    
    st.write("Choose your preferred export format:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Export to CSV", type="secondary"):
            # Convert results to CSV
            data = []
            for result in st.session_state.analysis_results:
                record = result.record
                recommendation = result.recommendation
                
                data.append({
                    'id': record.id,
                    'submission': record.submission.strftime('%Y-%m-%d') if record.submission else '',
                    'priority': record.priority.value if hasattr(record.priority, 'value') else str(record.priority),
                    'competency': record.targeted_competencies,
                    'estimated_trainees': record.estimated_trainees,
                    'expected_training_type': recommendation.training_type.value if hasattr(recommendation.training_type, 'value') else str(recommendation.training_type),
                    'reasoning': recommendation.reasoning,
                    'competency_classification': recommendation.competency_classification.value if hasattr(recommendation.competency_classification, 'value') else str(recommendation.competency_classification),
                    'demand_score': recommendation.demand_score,
                    'associated_skills_count': len(recommendation.associated_skills),
                    'department': record.department,
                    'division': record.division,
                    'section': record.section,
                    'job_families': record.job_families,
                    'request_type': record.request_type.value if hasattr(record.request_type, 'value') else str(record.request_type),
                    'targeted_audience': record.targeted_audience
                })
            
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False)
            
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"lna_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Export to JSON", type="secondary"):
            # Create export data structure
            export_data = {
                "metadata": {
                    "total_records": len(st.session_state.analysis_results),
                    "analysis_timestamp": datetime.now().isoformat(),
                    "bot_version": "1.0.0",
                    "source_file": st.session_state.uploaded_file_name
                },
                "summary": {
                    "total_entries": st.session_state.dataset_summary.total_entries,
                    "total_trainees": st.session_state.dataset_summary.total_trainees,
                    "average_trainees": st.session_state.dataset_summary.average_trainees,
                    "training_type_distribution": st.session_state.dataset_summary.training_type_distribution,
                    "priority_distribution": st.session_state.dataset_summary.priority_distribution
                },
                "results": []
            }
            
            for result in st.session_state.analysis_results:
                record = result.record
                recommendation = result.recommendation
                
                export_data["results"].append({
                    "record": {
                        "id": record.id,
                        "submission": record.submission.isoformat() if record.submission else None,
                        "priority": record.priority.value if hasattr(record.priority, 'value') else str(record.priority),
                        "competency_type": record.competency_type.value if hasattr(record.competency_type, 'value') else str(record.competency_type),
                        "job_families": record.job_families,
                        "targeted_competencies": record.targeted_competencies,
                        "request_type": record.request_type.value if hasattr(record.request_type, 'value') else str(record.request_type),
                        "targeted_audience": record.targeted_audience,
                        "estimated_trainees": record.estimated_trainees,
                        "comment": record.comment,
                        "year": record.year,
                        "division": record.division,
                        "department": record.department,
                        "section": record.section
                    },
                    "recommendation": {
                        "training_type": recommendation.training_type.value if hasattr(recommendation.training_type, 'value') else str(recommendation.training_type),
                        "reasoning": recommendation.reasoning,
                        "competency_classification": recommendation.competency_classification.value if hasattr(recommendation.competency_classification, 'value') else str(recommendation.competency_classification),
                        "demand_score": recommendation.demand_score,
                        "associated_skills": recommendation.associated_skills
                    }
                })
            
            json_str = json.dumps(export_data, indent=2)
            
            st.download_button(
                label="⬇️ Download JSON",
                data=json_str,
                file_name=f"lna_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("📊 Export to Excel", type="secondary"):
            # Create comprehensive Excel export with multiple sheets
            data = []
            
            # Cost estimation factors
            cost_factors = {
                'External': {'per_person': 2000, 'fixed_cost': 500},
                'SDP': {'per_person': 1200, 'fixed_cost': 5000},
                'In-house': {'per_person': 800, 'fixed_cost': 15000}
            }
            
            for result in st.session_state.analysis_results:
                record = result.record
                recommendation = result.recommendation
                
                training_type = recommendation.training_type.value if hasattr(recommendation.training_type, 'value') else str(recommendation.training_type)
                trainees = record.estimated_trainees
                
                # Calculate estimated cost
                if training_type in cost_factors:
                    per_person = cost_factors[training_type]['per_person']
                    fixed = cost_factors[training_type]['fixed_cost']
                    estimated_cost = (trainees * per_person) + fixed
                else:
                    estimated_cost = trainees * 1000  # Fallback
                
                data.append({
                    'ID': record.id,
                    'Submission Date': record.submission.strftime('%Y-%m-%d') if record.submission else '',
                    'Priority': record.priority.value if hasattr(record.priority, 'value') else str(record.priority),
                    'Competency': record.targeted_competencies,
                    'Estimated Trainees': record.estimated_trainees,
                    'Recommended Training Type': training_type,
                    'Competency Classification': recommendation.competency_classification.value if hasattr(recommendation.competency_classification, 'value') else str(recommendation.competency_classification),
                    'Demand Score': recommendation.demand_score,
                    'Estimated Cost ($)': estimated_cost,
                    'Cost per Trainee ($)': estimated_cost / trainees if trainees > 0 else 0,
                    'Department': record.department,
                    'Division': record.division,
                    'Section': record.section,
                    'Job Families': record.job_families,
                    'Request Type': record.request_type.value if hasattr(record.request_type, 'value') else str(record.request_type),
                    'Target Audience': record.targeted_audience,
                    'Reasoning': recommendation.reasoning,
                    'Associated Skills Count': len(recommendation.associated_skills),
                    'Year': record.year,
                    'Comment': record.comment
                })
            
            # Create main dataframe
            main_df = pd.DataFrame(data)
            
            # Create summary dataframe
            summary_data = {
                'Metric': [
                    'Total Records',
                    'Total Trainees', 
                    'Average Trainees per Record',
                    'Total Estimated Cost ($)',
                    'Average Cost per Record ($)',
                    'Average Cost per Trainee ($)',
                    'External Training Programs',
                    'SDP Programs',
                    'In-house Training Programs',
                    'High Priority Records',
                    'Medium Priority Records',
                    'Low Priority Records',
                    'Niche Competencies',
                    'Common Competencies'
                ],
                'Value': [
                    len(st.session_state.analysis_results),
                    st.session_state.dataset_summary.total_trainees,
                    f"{st.session_state.dataset_summary.average_trainees_per_entry:.2f}",
                    f"{main_df['Estimated Cost ($)'].sum():,.0f}",
                    f"{main_df['Estimated Cost ($)'].mean():,.0f}",
                    f"{main_df['Estimated Cost ($)'].sum() / main_df['Estimated Trainees'].sum():.0f}",
                    len(main_df[main_df['Recommended Training Type'] == 'External']),
                    len(main_df[main_df['Recommended Training Type'] == 'SDP']),
                    len(main_df[main_df['Recommended Training Type'] == 'In-house']),
                    len(main_df[main_df['Priority'] == 'High']),
                    len(main_df[main_df['Priority'] == 'Medium']),
                    len(main_df[main_df['Priority'] == 'Low']),
                    len(main_df[main_df['Competency Classification'] == 'niche']),
                    len(main_df[main_df['Competency Classification'] == 'common'])
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            
            # Create cost breakdown dataframe  
            cost_breakdown_data = []
            training_types = main_df['Recommended Training Type'].unique()
            
            for training_type in training_types:
                type_data = main_df[main_df['Recommended Training Type'] == training_type]
                total_cost = type_data['Estimated Cost ($)'].sum()
                total_trainees = type_data['Estimated Trainees'].sum()
                
                cost_breakdown_data.append({
                    'Training Type': training_type,
                    'Number of Programs': len(type_data),
                    'Total Cost ($)': total_cost,
                    'Average Cost per Program ($)': type_data['Estimated Cost ($)'].mean(),
                    'Total Trainees': total_trainees,
                    'Cost per Trainee ($)': total_cost / total_trainees if total_trainees > 0 else 0
                })
            
            cost_breakdown_df = pd.DataFrame(cost_breakdown_data)
            
            # Create Excel file in memory
            output = io.BytesIO()
            
            # Use ExcelWriter to create multi-sheet Excel file
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Write main results
                main_df.to_excel(writer, sheet_name='Analysis Results', index=False)
                
                # Write summary
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Write cost breakdown
                cost_breakdown_df.to_excel(writer, sheet_name='Cost Breakdown', index=False)
                
                # Write detailed skills for top 10 records
                top_records = main_df.nlargest(10, 'Demand Score')[['ID', 'Competency', 'Demand Score']].copy()
                skills_data = []
                
                for result in st.session_state.analysis_results:
                    if result.record.id in top_records['ID'].values:
                        for skill in result.recommendation.associated_skills:
                            skills_data.append({
                                'Record ID': result.record.id,
                                'Competency': result.record.targeted_competencies,
                                'Associated Skill': skill
                            })
                
                if skills_data:
                    skills_df = pd.DataFrame(skills_data)
                    skills_df.to_excel(writer, sheet_name='Associated Skills', index=False)
            
            # Convert to bytes
            processed_data = output.getvalue()
            
            st.download_button(
                label="⬇️ Download Excel (.xlsx)",
                data=processed_data,
                file_name=f"lna_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col4:
        if st.button("📋 Advanced Excel Export", type="secondary"):
            # Create advanced Excel export with xlsxwriter for enhanced features
            data = []
            
            # Cost estimation factors
            cost_factors = {
                'External': {'per_person': 2000, 'fixed_cost': 500},
                'SDP': {'per_person': 1200, 'fixed_cost': 5000},
                'In-house': {'per_person': 800, 'fixed_cost': 15000}
            }
            
            for result in st.session_state.analysis_results:
                record = result.record
                recommendation = result.recommendation
                
                training_type = recommendation.training_type.value if hasattr(recommendation.training_type, 'value') else str(recommendation.training_type)
                trainees = record.estimated_trainees
                
                # Calculate estimated cost
                if training_type in cost_factors:
                    per_person = cost_factors[training_type]['per_person']
                    fixed = cost_factors[training_type]['fixed_cost']
                    estimated_cost = (trainees * per_person) + fixed
                else:
                    estimated_cost = trainees * 1000
                
                data.append({
                    'ID': record.id,
                    'Submission': record.submission.strftime('%Y-%m-%d') if record.submission else '',
                    'Priority': record.priority.value if hasattr(record.priority, 'value') else str(record.priority),
                    'Competency': record.targeted_competencies,
                    'Trainees': record.estimated_trainees,
                    'Training_Type': training_type,
                    'Classification': recommendation.competency_classification.value if hasattr(recommendation.competency_classification, 'value') else str(recommendation.competency_classification),
                    'Demand_Score': recommendation.demand_score,
                    'Estimated_Cost': estimated_cost,
                    'Cost_per_Trainee': estimated_cost / trainees if trainees > 0 else 0,
                    'Department': record.department,
                    'Division': record.division,
                    'Section': record.section,
                    'Reasoning': recommendation.reasoning
                })
            
            df = pd.DataFrame(data)
            
            # Create Excel file with xlsxwriter for advanced formatting
            output = io.BytesIO()
            
            try:
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    # Write main data
                    df.to_excel(writer, sheet_name='LNA Analysis Results', index=False)
                    
                    # Get workbook and worksheet for formatting
                    workbook = writer.book  # type: ignore
                    worksheet = writer.sheets['LNA Analysis Results']  # type: ignore
                    
                    # Define formats
                    header_format = workbook.add_format({  # type: ignore
                        'bold': True,
                        'text_wrap': True,
                        'valign': 'top',
                        'fg_color': '#4472C4',
                        'font_color': 'white',
                        'border': 1
                    })
                    
                    currency_format = workbook.add_format({'num_format': '$#,##0'})  # type: ignore
                    number_format = workbook.add_format({'num_format': '#,##0'})  # type: ignore
                
                # Apply header formatting
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # Apply currency formatting to cost columns
                cost_col = df.columns.get_loc('Estimated_Cost')
                cost_per_trainee_col = df.columns.get_loc('Cost_per_Trainee')
                trainees_col = df.columns.get_loc('Trainees')
                demand_col = df.columns.get_loc('Demand_Score')
                
                worksheet.set_column(cost_col, cost_col, 15, currency_format)
                worksheet.set_column(cost_per_trainee_col, cost_per_trainee_col, 15, currency_format)
                worksheet.set_column(trainees_col, trainees_col, 10, number_format)
                worksheet.set_column(demand_col, demand_col, 12, number_format)
                
                # Auto-adjust column widths
                for i, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).map(len).max(),
                        len(col)
                    )
                    worksheet.set_column(i, i, min(max_length + 2, 50))
                
                    # Add conditional formatting for priority
                    priority_col = df.columns.get_loc('Priority')
                    worksheet.conditional_format(1, priority_col, len(df), priority_col, {  # type: ignore
                        'type': 'text',
                        'criteria': 'containing',
                        'value': 'High',
                        'format': workbook.add_format({'bg_color': '#ffcccc'})  # type: ignore
                    })
                    
                    # Add data validation for training types (informational)
                    training_type_col = df.columns.get_loc('Training_Type')
                    worksheet.conditional_format(1, training_type_col, len(df), training_type_col, {  # type: ignore
                        'type': 'text',
                        'criteria': 'containing',
                        'value': 'External',
                        'format': workbook.add_format({'bg_color': '#e6f3ff'})  # type: ignore
                    })
                    
                    worksheet.conditional_format(1, training_type_col, len(df), training_type_col, {  # type: ignore
                        'type': 'text',
                        'criteria': 'containing',
                        'value': 'SDP',
                        'format': workbook.add_format({'bg_color': '#fff2e6'})  # type: ignore
                    })
                    
                    worksheet.conditional_format(1, training_type_col, len(df), training_type_col, {  # type: ignore
                        'type': 'text',
                        'criteria': 'containing',
                        'value': 'In-house',
                        'format': workbook.add_format({'bg_color': '#e6ffe6'})  # type: ignore
                    })
            except Exception as e:
                # Fallback to simple Excel export if advanced formatting fails
                df.to_excel(output, index=False)
            
            processed_data = output.getvalue()
            
            st.download_button(
                label="⬇️ Download Advanced Excel",
                data=processed_data,
                file_name=f"lna_analysis_advanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Sidebar with navigation
    with st.sidebar:
        st.header("🔧 Navigation")
        
        # Show current status
        if st.session_state.analysis_results is not None:
            st.success(f"✅ Analysis completed!\n{len(st.session_state.analysis_results)} records processed")
            
            if st.button("🗑️ Clear Results"):
                st.session_state.analysis_results = None
                st.session_state.dataset_summary = None
                st.session_state.uploaded_file_name = None
                st.rerun()
        else:
            # Quick sample dataset selector
            st.subheader("🎯 Quick Test")
            st.write("Load a sample dataset instantly:")
            
            sample_options = {
                "Multi-Industry (25 records)": "comprehensive_multi_industry_lna.csv",
                "Niche Competencies (25 records)": "niche_competencies_stress_test.csv", 
                "Large-Scale Training (25 records)": "large_scale_training_scenarios.csv",
                "Small Groups (25 records)": "small_group_edge_cases.csv",
                "Business Mix (25 records)": "business_competencies_mix.csv",
                "Excel Multi-Sheet (75 records)": "multi_sheet_comprehensive_test.xlsx"
            }
            
            selected_sample = st.selectbox(
                "Choose a sample:",
                options=list(sample_options.keys()),
                index=0
            )
            
            if st.button("🚀 Load Sample", type="primary"):
                dataset_path = Path(f"data/test_datasets/{sample_options[selected_sample]}")
                if dataset_path.exists():
                    process_sample_dataset(dataset_path, selected_sample)
                else:
                    st.error(f"Sample dataset not found: {dataset_path}")
        
        st.markdown("---")
        
        # Quick stats if analysis is done
        if st.session_state.dataset_summary is not None:
            st.subheader("📈 Quick Stats")
            summary = st.session_state.dataset_summary
            
            st.metric("Records", summary.total_entries)
            st.metric("Total Trainees", f"{summary.total_trainees:,}")
            
            # Training type breakdown
            st.write("**Training Types:**")
            for training_type, count in summary.training_type_distribution.items():
                percentage = (count / summary.total_entries) * 100
                type_name = training_type.value if hasattr(training_type, 'value') else str(training_type)
                st.write(f"• {type_name}: {count} ({percentage:.1f}%)")
    
    # Main content area - Navigation tabs
    tab1, tab2 = st.tabs(["📁 File Analysis", "🔍 Single Record Analysis"])
    
    with tab1:
        if st.session_state.analysis_results is None:
            # Show file upload section
            file_upload_section()
            
            # Quick start guide
            st.markdown("---")
            st.header("� Quick Start Guide")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("1️⃣ Choose Your Data")
                st.write("Upload your own CSV/Excel file or try our sample datasets to explore different scenarios.")
            
            with col2:
                st.subheader("2️⃣ Analyze Results")
                st.write("View comprehensive visualizations, cost analysis, and detailed training recommendations.")
            
            with col3:
                st.subheader("3️⃣ Export & Share")
                st.write("Download results in CSV, JSON, Excel (.xlsx/.xls), or PDF format for reporting and decision-making.")
            
            # Key features highlight
            st.markdown("---")
            with st.expander("✨ Key Features", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🎯 Intelligent Recommendations:**")
                    st.write("• Automatic training type selection based on group size")
                    st.write("• Niche competency override for specialized skills")
                    st.write("• Priority-based demand scoring")
                    st.write("• Cost-effective solution recommendations")
                
                with col2:
                    st.write("**📊 Comprehensive Analysis:**")
                    st.write("• Interactive visualizations and charts")
                    st.write("• Department and competency breakdowns")
                    st.write("• Cost projections and budget planning")
                    st.write("• Multi-format export (CSV, JSON, Excel .xlsx/.xls)")
            
        else:
            # Show analysis results
            display_summary_metrics()
            
            st.markdown("---")
            
            # Create tabs for different views
            subtab1, subtab2, subtab3, subtab4 = st.tabs(["📊 Visualizations", "📋 Detailed Results", "💾 Export", "ℹ️ Analysis Info"])
            
            with subtab1:
                display_training_distribution()
                display_priority_distribution()
                
                st.markdown("---")
                
                display_competency_analysis()
                
                st.markdown("---")
                
                display_departmental_analysis()
                
                st.markdown("---")
                
                display_cost_analysis()
            
            with subtab2:
                display_detailed_results()
            
            with subtab3:
                display_export_options()
            
            with subtab4:
                if st.session_state.dataset_summary is not None:
                    st.subheader("Analysis Information")
                    
                    summary = st.session_state.dataset_summary
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Dataset Summary:**")
                        st.write(f"• Total Entries: {summary.total_entries}")
                        st.write(f"• Total Trainees: {summary.total_trainees:,}")
                        st.write(f"• Average Trainees: {summary.average_trainees_per_entry:.2f}")
                        st.write(f"• Source File: {st.session_state.uploaded_file_name}")
                    
                    with col2:
                        st.write("**Business Rules Applied:**")
                        st.write("• External Training: ≤10 trainees")
                        st.write("• SDP: 11-50 trainees")  
                        st.write("• In-house Training: >50 trainees")
                        st.write("• Niche competencies → SDP override")
    
    with tab2:
        # Single record analysis is always available
        single_record_analysis()

if __name__ == "__main__":
    main()