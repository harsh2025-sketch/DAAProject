"""
Comparison page for benchmarking multiple operations simultaneously
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.benchmarks.benchmark import Benchmark

def show_comparison_page():
    st.title("🔄 Multi-Operation Comparison")
    st.caption("Compare multiple data structures and operations side-by-side")
    
    # Operation selection
    st.sidebar.header("Select Operations to Compare")
    
    operations = {
        "Array: insert_end": st.sidebar.checkbox("Array: Insert (end)", value=True),
        "LinkedList: insert_tail": st.sidebar.checkbox("LinkedList: Insert (tail)", value=True),
        "BST: insert": st.sidebar.checkbox("BST: Insert (random)", value=True),
        "HashTable: put": st.sidebar.checkbox("HashTable: Put", value=True),
        "Array: search": st.sidebar.checkbox("Array: Search", value=False),
        "LinkedList: search": st.sidebar.checkbox("LinkedList: Search", value=False),
        "BST: search": st.sidebar.checkbox("BST: Search", value=False),
        "HashTable: get": st.sidebar.checkbox("HashTable: Get", value=False),
    }
    
    selected_ops = [op for op, selected in operations.items() if selected]
    
    if len(selected_ops) == 0:
        st.warning("⚠️ Please select at least one operation to compare")
        return
    
    st.sidebar.markdown("---")
    size_preset = st.sidebar.radio(
        "Size range",
        ["Small (100-1K)", "Medium (1K-5K)", "Custom"],
        index=0,
    )
    
    if size_preset == "Small (100-1K)":
        sizes = [100, 250, 500, 750, 1000]
    elif size_preset == "Medium (1K-5K)":
        sizes = [1000, 2000, 3000, 4000, 5000]
    else:
        min_size = st.sidebar.number_input("Min", 100, 100000, 100)
        max_size = st.sidebar.number_input("Max", 100, 100000, 5000)
        num_points = st.sidebar.slider("Points", 3, 10, 5)
        sizes = [int(x) for x in pd.np.linspace(min_size, max_size, num_points)]
    
    trials = st.sidebar.slider("Trials", 1, 10, 3)
    
    if st.sidebar.button("🚀 Run Comparison", type="primary"):
        results = {}
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, op in enumerate(selected_ops):
            status_text.text(f"Running {op}... ({idx + 1}/{len(selected_ops)})")
            progress_bar.progress((idx + 1) / len(selected_ops))
            
            bench = Benchmark(sizes, trials)
            results[op] = bench.run(op)
        
        status_text.text("✅ All benchmarks complete!")
        progress_bar.empty()
        
        # Create comparison visualization
        st.subheader("📊 Performance Comparison")
        
        fig = go.Figure()
        
        for op, df in results.items():
            stats = df.groupby('size')['time_ms'].mean().reset_index()
            fig.add_trace(go.Scatter(
                x=stats['size'],
                y=stats['time_ms'],
                mode='lines+markers',
                name=op,
                line=dict(width=2),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="Execution Time vs Input Size",
            xaxis_title="Input Size (n)",
            yaxis_title="Time (ms)",
            hovermode='x unified',
            height=500,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary table
        st.subheader("📈 Summary Statistics")
        
        summary_data = []
        for op, df in results.items():
            stats = df.groupby('size')['time_ms'].mean()
            summary_data.append({
                'Operation': op,
                'Avg Time (ms)': stats.mean(),
                'Min Time (ms)': stats.min(),
                'Max Time (ms)': stats.max(),
                'Growth Factor': stats.iloc[-1] / stats.iloc[0] if len(stats) > 1 else 1.0
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df = summary_df.sort_values('Avg Time (ms)')
        
        st.dataframe(
            summary_df.style.format({
                'Avg Time (ms)': '{:.4f}',
                'Min Time (ms)': '{:.4f}',
                'Max Time (ms)': '{:.4f}',
                'Growth Factor': '{:.2f}x'
            }).background_gradient(subset=['Avg Time (ms)'], cmap='RdYlGn_r'),
            use_container_width=True
        )
        
        # Rankings
        st.subheader("🏆 Performance Rankings")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Fastest Operations** (by average time)")
            for idx, row in summary_df.head(3).iterrows():
                st.write(f"{idx + 1}. {row['Operation']}: {row['Avg Time (ms)']:.4f} ms")
        
        with col2:
            st.markdown("**Best Scalability** (lowest growth factor)")
            scalability_df = summary_df.sort_values('Growth Factor')
            for idx, row in scalability_df.head(3).iterrows():
                st.write(f"{idx + 1}. {row['Operation']}: {row['Growth Factor']:.2f}x")
        
        # Export all results
        st.markdown("---")
        if st.button("📥 Export All Results"):
            combined_df = pd.concat([df.assign(operation=op) for op, df in results.items()])
            csv = combined_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download Combined CSV",
                data=csv,
                file_name="comparison_results.csv",
                mime="text/csv"
            )
    else:
        st.info("👈 Select operations from the sidebar and click Run Comparison")
        
        st.markdown("---")
        st.markdown("""
        ### How to Use Comparison Mode
        
        1. **Select operations** you want to compare using checkboxes
        2. **Configure size range** (smaller ranges run faster)
        3. **Set number of trials** for statistical reliability
        4. **Run comparison** and analyze results
        
        #### Benefits of Comparison Mode
        - See relative performance across structures
        - Identify fastest operations for your use case
        - Understand scalability differences
        - Make data-driven architecture decisions
        """)

if __name__ == "__main__":
    show_comparison_page()
