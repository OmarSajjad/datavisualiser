import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title('Enhanced CSV Data Dashboard')

# Custom CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #f0f2f6;
    }
    .stTextInput, .stButton, .stSelectbox {
        font-size: 18px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    try:
        # Read the CSV file
        data = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(data.head())

        # Select columns to plot
        columns = data.columns.tolist()
        x_axis = st.selectbox('Select X-axis', columns)
        y_axes = st.multiselect('Select Y-axis', columns)

        # Filter data
        if 'column_name' in data.columns:
            min_value = data['column_name'].min()
            max_value = data['column_name'].max()
            value = st.slider('Filter by column_name', min_value, max_value, (min_value, max_value))
            data = data[(data['column_name'] >= value[0]) & (data['column_name'] <= value[1])]

        # Select plot type
        plot_type = st.selectbox('Select Plot Type', ['Line Plot', 'Scatter Plot', 'Bar Plot'])

        # Option to display multiple graphs
        display_option = st.radio('Display Option', ['Single Graph', 'Multiple Graphs'])

        if x_axis and y_axes:
            if display_option == 'Single Graph':
                fig = go.Figure()
                for y_axis in y_axes:
                    if plot_type == 'Line Plot':
                        fig.add_trace(go.Scatter(x=data[x_axis], y=data[y_axis], mode='lines', name=y_axis))
                    elif plot_type == 'Scatter Plot':
                        fig.add_trace(go.Scatter(x=data[x_axis], y=data[y_axis], mode='markers', name=y_axis))
                    elif plot_type == 'Bar Plot':
                        fig.add_trace(go.Bar(x=data[x_axis], y=data[y_axis], name=y_axis))
                    
                    # Add annotations
                    fig.add_annotation(x=data[x_axis].iloc[0], y=data[y_axis].iloc[0], text='Start', showarrow=True, arrowhead=1)
                    fig.add_annotation(x=data[x_axis].iloc[-1], y=data[y_axis].iloc[-1], text='End', showarrow=True, arrowhead=1)
                
                fig.update_layout(title=f'{", ".join(y_axes)} vs {x_axis}', xaxis_title=x_axis, yaxis_title='Values')
                st.plotly_chart(fig)
            else:
                cols = st.columns(len(y_axes))
                for i, y_axis in enumerate(y_axes):
                    with cols[i]:
                        if plot_type == 'Line Plot':
                            fig = px.line(data, x=x_axis, y=y_axis, title=f'{y_axis} vs {x_axis}')
                        elif plot_type == 'Scatter Plot':
                            fig = px.scatter(data, x=x_axis, y=y_axis, title=f'{y_axis} vs {x_axis}')
                        elif plot_type == 'Bar Plot':
                            fig = px.bar(data, x=x_axis, y=y_axis, title=f'{y_axis} vs {x_axis}')
                        
                        st.plotly_chart(fig)

        # Download filtered data
        csv = data.to_csv().encode('utf-8')
        st.download_button(label="Download data as CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a CSV file.")