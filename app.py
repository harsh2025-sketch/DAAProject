import streamlit as st
import pandas as pd
import numpy as np
from src.benchmarks.benchmark import Benchmark
import time

st.set_page_config(page_title="Structure Showdown", page_icon="🧱", layout="wide")

# Big-O reference for all operations
BIG_O_REFERENCE = {
    "Array: insert_end": "O(1) amortized",
    "Array: insert_front": "O(n)",
    "Array: search": "O(n)",
    "Array: delete": "O(n)",
    "LinkedList: insert_tail": "O(n)",
    "LinkedList: search": "O(n)",
    "LinkedList: delete": "O(n)",
    "BST: insert": "O(log n) avg, O(n) worst",
    "BST: insert_ordered": "O(n) worst case",
    "BST: search": "O(log n) avg, O(n) worst",
    "BST: delete": "O(log n) avg",
    "HashTable: put": "O(1) avg",
    "HashTable: get": "O(1) avg",
    "HashTable: delete": "O(1) avg",
    "Graph: add_edges(line)": "O(1) per edge",
    "Graph: bfs_search(end)": "O(V + E)",
    "Graph: delete_node": "O(degree)",
}

st.title("🧱 Structure Showdown")
st.caption("Performance Analysis & Comparison of Data Structures for Diverse Operations")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

operation_map = {
    # Arrays
    "Array: insert_end": "Array (Python list)",
    "Array: insert_front": "Array (Python list)",
    "Array: search": "Array (Python list)",
    "Array: delete": "Array (Python list)",
    # Linked List
    "LinkedList: insert_tail": "Linked List",
    "LinkedList: search": "Linked List",
    "LinkedList: delete": "Linked List",
    # BST
    "BST: insert": "Binary Search Tree",
    "BST: insert_ordered": "Binary Search Tree (ordered)",
    "BST: search": "Binary Search Tree",
    "BST: delete": "Binary Search Tree",
    # Hash Table
    "HashTable: put": "Hash Table",
    "HashTable: get": "Hash Table",
    "HashTable: delete": "Hash Table",
    # Graph
    "Graph: add_edges(line)": "Graph (Adjacency List)",
    "Graph: bfs_search(end)": "Graph (Adjacency List)",
    "Graph: delete_node": "Graph (Adjacency List)",
}

op = st.sidebar.selectbox("📊 Benchmark Operation", list(operation_map.keys()), index=0)

st.sidebar.markdown("---")
st.sidebar.subheader("Size Configuration")
size_preset = st.sidebar.radio(
    "Range preset",
    ["Small (100-1K)", "Medium (1K-10K)", "Large (10K-50K)", "Custom"],
    index=1,
)

if size_preset == "Small (100-1K)":
    sizes = [100, 250, 500, 750, 1000]
elif size_preset == "Medium (1K-10K)":
    sizes = [1000, 2500, 5000, 7500, 10000]
elif size_preset == "Large (10K-50K)":
    sizes = [10000, 20000, 30000, 40000, 50000]
else:
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        start = st.number_input("start", value=100, min_value=10, step=10)
    with col2:
        stop = st.number_input("stop", value=5000, min_value=100, step=100)
    with col3:
        step = st.number_input("step", value=500, min_value=10, step=10)
    sizes = list(range(int(start), int(stop) + 1, int(step)))

trials = st.sidebar.slider("🔄 Trials per size", min_value=1, max_value=20, value=5)

st.sidebar.markdown("---")
run_button = st.sidebar.button("🚀 Run Benchmark", type="primary", use_container_width=True)
re_run_button = st.sidebar.button("↻ Re-run with same params", help="Re-run the last benchmark with identical parameters", use_container_width=True)

# Last run summary in the sidebar (quick preview + clear)
if st.session_state.get('last_run'):
    with st.sidebar.expander("🕘 Last run summary", expanded=False):
        last = st.session_state['last_run']
        try:
            st.markdown(f"**Operation:** `{last['op']}`")
            st.markdown(f"**Sizes:** {last['sizes']}")
            st.markdown(f"**Trials:** {last['trials']}")
            st.markdown(f"**Duration:** {last['duration']:.3f} s")
            st.markdown(f"**Measurements:** {len(last.get('result_df', []))}")
            if 'result_df' in last and hasattr(last['result_df'], 'head'):
                st.markdown("**Preview (first 5 rows)**")
                st.dataframe(last['result_df'].head(5), use_container_width=True)
        except Exception:
            st.write("(Could not render last run preview)")
        if st.button("🗑️ Clear last run", key="clear_last_run"):
            del st.session_state['last_run']

# Display operation info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📂 Data Structure", operation_map[op])
with col2:
    st.metric("⚡ Operation", op.split(": ")[1])
with col3:
    big_o = BIG_O_REFERENCE.get(op, "N/A")
    st.metric("🎯 Complexity", big_o)

st.markdown("---")

# Display sizes
with st.expander(f"📏 Input sizes to test ({len(sizes)} points)", expanded=False):
    st.write(sizes)

def _execute_benchmark(op_name, sizes_list, trials_count):
    """Run the benchmark and capture result dataframe, stats and logs."""
    logs = []
    start_t = time.perf_counter()
    logs.append(f"Starting benchmark for '{op_name}'")
    logs.append(f"Sizes: {sizes_list}")
    logs.append(f"Trials per size: {trials_count}")
    try:
        bench = Benchmark(sizes=sizes_list, trials=int(trials_count))
        result_df = bench.run(op_name)
        logs.append(f"Raw trials collected: {len(result_df)}")

        stats_df = result_df.groupby('size')['time_ms'].agg([
            ('Mean', 'mean'),
            ('Median', 'median'),
            ('Std Dev', 'std'),
            ('Min', 'min'),
            ('Max', 'max')
        ]).reset_index()

        end_t = time.perf_counter()
        duration = end_t - start_t
        logs.append(f"Benchmark completed in {duration:.3f} seconds")

        return result_df, stats_df, logs, duration
    except Exception as e:
        logs.append(f"Benchmark failed: {e}")
        raise


def _display_results(result_df, stats_df, logs, duration, op_name, sizes_list, trials_count):
    """Display results using the existing UI layout (charts, stats, downloads, insights)."""
    st.success(f"✅ Benchmark completed! {len(result_df)} trials executed successfully.")
    # store last run parameters and results in session state for re-run or inspection
    st.session_state['last_run'] = {
        'op': op_name,
        'sizes': sizes_list,
        'trials': trials_count,
        'result_df': result_df,
        'stats_df': stats_df,
        'logs': logs,
        'duration': duration,
    }

    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualization", "📈 Statistics", "🔢 Raw Data", "💡 Insights"])

    with tab1:
        st.subheader("Performance vs Input Size")
        # Line chart with mean
        chart_df = stats_df[['size', 'Mean']].copy()
        st.line_chart(chart_df.set_index('size'), height=400)
        st.caption("Mean execution time across trials")
        # Bar chart showing min/mean/max
        st.subheader("Range Visualization")
        range_df = stats_df[['size', 'Min', 'Mean', 'Max']].set_index('size')
        st.bar_chart(range_df, height=300)
        st.caption("Min, Mean, and Max times per input size")

    with tab2:
        st.subheader("Statistical Summary")
        display_stats = stats_df.copy()
        display_stats.columns = ['Size', 'Mean (ms)', 'Median (ms)', 'Std Dev (ms)', 'Min (ms)', 'Max (ms)']
        st.dataframe(
            display_stats.style.format({
                'Mean (ms)': '{:.4f}',
                'Median (ms)': '{:.4f}',
                'Std Dev (ms)': '{:.4f}',
                'Min (ms)': '{:.4f}',
                'Max (ms)': '{:.4f}',
            }).background_gradient(subset=['Mean (ms)'], cmap='RdYlGn_r'),
            use_container_width=True
        )
        # Overall metrics
        st.markdown("---")
        st.subheader("Overall Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_time = stats_df['Mean'].mean()
            st.metric("⏱️ Avg Time", f"{avg_time:.4f} ms")
        with col2:
            total_trials = len(result_df)
            st.metric("🔄 Total Trials", total_trials)
        with col3:
            if len(stats_df) > 1:
                growth = stats_df['Mean'].iloc[-1] / stats_df['Mean'].iloc[0]
                st.metric("📈 Growth Factor", f"{growth:.2f}x")
            else:
                st.metric("📈 Growth Factor", "N/A")
        with col4:
            cv = (stats_df['Std Dev'].mean() / stats_df['Mean'].mean()) * 100 if stats_df['Mean'].mean() > 0 else 0
            st.metric("📊 Avg CV", f"{cv:.1f}%")
            st.caption("Coefficient of Variation")

    with tab3:
        st.subheader("Raw Trial Data")
        st.dataframe(result_df, use_container_width=True, height=400)
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Raw Data (CSV)",
                data=csv,
                file_name=f"benchmark_{op_name.replace(':', '_').replace(' ', '_')}_raw.csv",
                mime="text/csv",
            )
        with col2:
            stats_csv = display_stats.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Statistics (CSV)",
                data=stats_csv,
                file_name=f"benchmark_{op_name.replace(':', '_').replace(' ', '_')}_stats.csv",
                mime="text/csv",
            )

    with tab4:
        st.subheader("💡 Insights & Analysis")
        st.markdown(f"""
        **Operation:** `{op_name}`  
        **Data Structure:** `{operation_map[op_name]}`  
        **Expected Complexity:** `{BIG_O_REFERENCE.get(op_name, 'N/A')}`
        """)
        st.markdown("---")
        st.markdown("#### Performance Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Test Configuration:")
            st.write(f"- Sizes tested: {len(sizes_list)} points")
            st.write(f"- Range: {min(sizes_list):,} to {max(sizes_list):,}")
            st.write(f"- Trials per size: {trials_count}")
            st.write(f"- Total measurements: {len(result_df)}")
        with col2:
            st.write("**Results:")
            st.write(f"- Mean time: {stats_df['Mean'].mean():.4f} ms")
            st.write(f"- Std deviation: {stats_df['Std Dev'].mean():.4f} ms")
            if len(stats_df) > 1:
                st.write(f"- Performance growth: {growth:.2f}x")
            st.write(f"- Variability (CV): {cv:.1f}%")
        st.markdown("---")
        st.markdown("#### Interpretation")
        # preserve the existing insights logic
        if "Array: insert_end" in op_name:
            st.success("✅ **Excellent performance**: Python lists use dynamic arrays with amortized O(1) append. Periodic resizing causes occasional spikes.")
        elif "Array: insert_front" in op_name:
            st.warning("⚠️ **Slow operation**: Inserting at the front requires shifting all n elements. Consider using collections.deque for front insertions.")
        elif "Array: search" in op_name:
            st.info("🔍 **Linear search**: Must check each element sequentially. For large datasets, consider sorted arrays + binary search or hash tables.")
        elif "Array: delete" in op_name:
            st.warning("⚠️ **Linear time**: Deletion requires finding the element (O(n)) and shifting remaining elements (O(n)).")
        elif "LinkedList: insert_tail" in op_name:
            st.info("📎 **O(n) traversal**: Must walk entire list to reach tail. Consider keeping a tail pointer for O(1) appends.")
        elif "LinkedList: search" in op_name:
            st.info("📎 **Sequential access**: Poor cache locality makes linked lists slower than arrays for search despite same O(n) complexity.")
        elif "LinkedList: delete" in op_name:
            st.info("📎 **Fast once found**: Deletion is O(1) if you have the node reference, but finding it is O(n).")
        elif "BST: insert_ordered" in op_name:
            st.error("🚨 **Degenerate tree**: Ordered insertions create a linked list (O(n) height). Use AVL/Red-Black trees for guaranteed O(log n).")
        elif "BST: insert" in op_name:
            st.success("🌲 **Balanced performance**: Random insertions keep tree relatively balanced, achieving O(log n) average case.")
        elif "BST: search" in op_name:
            st.success("🌲 **Logarithmic search**: Efficient for sorted data. Unbalanced trees degrade to O(n).")
        elif "BST: delete" in op_name:
            st.info("🌲 **Complex operation**: Deletion requires finding node, handling 3 cases (leaf, 1 child, 2 children).")
        elif "HashTable: put" in op_name:
            st.success("⚡ **Near-constant time**: Hash tables provide O(1) average insertions. Performance depends on load factor and hash function quality.")
        elif "HashTable: get" in op_name:
            st.success("⚡ **Fastest lookup**: O(1) average case makes hash tables ideal for key-value storage and caching.")
        elif "HashTable: delete" in op_name:
            st.success("⚡ **Fast deletion**: O(1) average with separate chaining. Some implementations use tombstones.")
        elif "Graph: add_edges" in op_name:
            st.info("🕸️ **Efficient edge insertion**: Adjacency list provides O(1) edge additions. Adjacency matrix would be O(1) but uses O(V²) space.")
        elif "Graph: bfs_search" in op_name:
            st.info("🕸️ **BFS traversal**: O(V + E) time visits all reachable vertices and edges. Good for shortest path in unweighted graphs.")
        elif "Graph: delete_node" in op_name:
            st.warning("⚠️ **Moderate cost**: Must remove node and update all adjacent nodes. Time proportional to node degree.")

    # show logs panel below tabs
    with st.expander("📝 Benchmark Logs", expanded=False):
        st.markdown("**Execution logs**")
        for line in logs:
            st.text(line)

    return


# handle re-run with same params
if re_run_button and st.session_state.get('last_run'):
    last = st.session_state['last_run']
    op_to_use = last['op']
    sizes_to_use = last['sizes']
    trials_to_use = last['trials']
    with st.spinner(f"⏳ Re-running benchmark for **{op_to_use}** across {len(sizes_to_use)} sizes × {trials_to_use} trials..."):
        try:
            result_df, stats_df, logs, duration = _execute_benchmark(op_to_use, sizes_to_use, trials_to_use)
            _display_results(result_df, stats_df, logs, duration, op_to_use, sizes_to_use, trials_to_use)
        except Exception as e:
            st.error(f"❌ Re-run failed: {e}")
            with st.expander("🐛 Error Details"):
                st.exception(e)
    st.stop()

if run_button:
    with st.spinner(f"⏳ Running benchmark for **{op}** across {len(sizes)} sizes × {trials} trials..."):
        try:
            result_df, stats_df, logs, duration = _execute_benchmark(op, sizes, trials)
            _display_results(result_df, stats_df, logs, duration, op, sizes, trials)
        except Exception as e:
            st.error(f"❌ Benchmark failed: {str(e)}")
            with st.expander("🐛 Error Details"):
                st.exception(e)
        except Exception as e:
            st.error(f"❌ Benchmark failed: {str(e)}")
            with st.expander("🐛 Error Details"):
                st.exception(e)

else:
    st.info("👈 Configure parameters in the sidebar and click **🚀 Run Benchmark** to start analysis.")
    
    st.markdown("---")
    st.markdown("### 📚 About Structure Showdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Features
        - 🔬 **5 Data Structures**: Arrays, Linked Lists, BST, Hash Tables, Graphs
        - 📊 **17 Operations**: Insertion, deletion, search across all structures
        - 📈 **Statistical Analysis**: Mean, median, std dev, min/max
        - 💾 **Export Results**: Download CSV for external analysis
        - 💡 **Learning Tools**: Big-O reference and trade-off explanations
        - 🎨 **Interactive UI**: Streamlit-powered visualization
        """)
    
    with col2:
        st.markdown("""
        #### How to Use
        1. **Select Operation**: Choose what to benchmark
        2. **Configure Sizes**: Pick preset or custom range
        3. **Set Trials**: More trials = better statistics
        4. **Run & Analyze**: Explore results across tabs
        5. **Export Data**: Download for reports or papers
        6. **Learn**: Read insights for each operation
        """)
    
    st.markdown("---")
    st.markdown("### 🎯 Learning Objectives")
    st.markdown("""
    This tool helps you:
    - 📊 **Empirically verify** Big-O complexity through measurement
    - 🔍 **Understand trade-offs** between data structures
    - 💡 **Make informed decisions** about which structure to use
    - 📈 **Visualize performance** scaling with input size
    - 🧪 **Experiment** with different workloads and patterns
    """)
